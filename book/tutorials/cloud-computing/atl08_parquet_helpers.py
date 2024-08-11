from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import h5py
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import fsspec
import numpy as np
import shapely
from earthaccess.results import DataGranule
from earthaccess.search import DataGranules
import json
import os
import time
import concurrent

@dataclass
class ParquetTable:
    """Class for interacting with a parquet table"""
    schema: pa.schema
    geometadata: dict
    
    def __init__(self, geometadata_file: str, template_file: str):
        with open(geometadata_file, 'r') as f:
            self.geometadata = json.loads(f.read())
        file = h5py.File(template_file, rdcc_bytes=4*1024*1024)
        self.schema = self.create_pyarrow_schema(file, self.geometadata)

    def create_pyarrow_schema(self, template_file: h5py.File, geometadata) -> pa.schema:
        # TODO: make this configurable
        land_segments_group = template_file["gt1l"]["land_segments"]
        canopy_group = template_file["gt1l"]["land_segments"]["canopy"]
        terrain_group = template_file["gt1l"]["land_segments"]["terrain"]  
        
        land_segment_fields = self.datasets_to_fields(land_segments_group)
        geometry_field = pa.field("geometry", pa.binary(), metadata={
            "encoding": "WKB",
            "geometry_types": "POINT"
        })
        land_segment_fields.append(geometry_field)
        
        timestamp_field = pa.field("timestamp", pa.timestamp('ns'))
        land_segment_fields.append(timestamp_field)
        
        beam_field = pa.field("beam", pa.string())
        land_segment_fields.append(beam_field) 
        
        strength_field = pa.field("strength", pa.string())
        land_segment_fields.append(strength_field) 
        
        
        canopy_fields = self.datasets_to_fields(canopy_group)
        terrain_fields = self.datasets_to_fields(terrain_group)
    
        fields = land_segment_fields + canopy_fields + terrain_fields
    
        metadata = json.dumps(geometadata).encode('utf-8')
        schema = pa.schema(fields, metadata={b"geo": metadata})
        
        return schema

    def result_bbox(self, result: DataGranule):
        points = result["umm"]["SpatialExtent"]["HorizontalSpatialDomain"]["Geometry"]["GPolygons"][0]["Boundary"]["Points"]
    
        longitudes = [point['Longitude'] for point in points]
        latitudes = [point['Latitude'] for point in points]
    
        min_lon, min_lat = min(longitudes), min(latitudes)
        max_lon, max_lat = max(longitudes), max(latitudes)
        bbox = shapely.geometry.box(min_lon, min_lat, max_lon, max_lat)
        return bbox
    
    def results_bounds(self, results: list[DataGranule]):
        union_bbox = self.result_bbox(results[0])
        for result in results:
            bbox = self.result_bbox(result)  
            union_bbox = union_bbox.union(bbox)
        return list(union_bbox.envelope.bounds)
    
    def datasets_to_fields(self, group: h5py.Group):
        fields = []
        for key in group.keys():
            if isinstance(group[key], h5py.Dataset):
                dtype = group[key].dtype
                numpy_dtype = dtype.newbyteorder("=")
                arrow_type = pa.from_numpy_dtype(numpy_dtype)
                fields.append((key, arrow_type))
        return fields
    
    def get_group_chunks(self, group: h5py.Group, offset: int, chunk_size: int) -> list[np.array]:
        chunks = []
        for key in group.keys():
            if isinstance(group[key], h5py.Dataset):
                if len(group[key].chunks) == 1:
                    chunks.append(group[key][offset:offset+chunk_size])
                # Handle variables with land segment chunking
                elif len(group[key].chunks) == 2:
                    chunks.append(group[key][offset:offset+chunk_size, 0])
        return chunks
    
    def chunks_to_tables(self, result: DataGranule, fs: fsspec.filesystem, beam: str, group_schema: pa.schema):
        tables = []
        url = result.data_links(access="direct")[0]
        print(url)
        with fs.open(url, 'rb') as f:
            file = h5py.File(f, rdcc_nbytes=4*1024*1024)
            orientation = file['orbit_info']['sc_orient'][0]
            if orientation == 0 and beam[-1] == "l":
                strength = "strong"
            elif orientation == 1 and beam[-1] == "r":
                strength = "strong"
            elif orientation == 2:
                strength = "degraded"
            else:
                strength = "weak"
    
            GPS_EPOCH = pd.to_datetime('1980-01-06 00:00:00')
            # Not sure why other examples of this were using the value as an array
            atlas_sdp_gps_epoch = file['ancillary_data']['atlas_sdp_gps_epoch'][0]
            
            land_segments_group = file[beam]["land_segments"]
            canopy_group = file[beam]["land_segments"]["canopy"]
            terrain_group = file[beam]["land_segments"]["terrain"] 
    
            chunk_size = land_segments_group["latitude"].chunks[0]
            size = land_segments_group["latitude"].size
            number_of_chunks = (size // chunk_size) + 1
        
            for n in range(number_of_chunks):
                offset = n * chunk_size
                land_segment_chunks = self.get_group_chunks(land_segments_group, offset, chunk_size)
                # Populate geometry field
                geometries = []
                for lat, lon in zip(
                    land_segments_group["latitude"][offset:offset+chunk_size],
                    land_segments_group["longitude"][offset:offset+chunk_size]
                ):
                    point = shapely.Point(lon, lat)
                    point_wkb = shapely.to_wkb(point, flavor="iso")
                    geometries.append(point_wkb)
                land_segment_chunks.append(geometries)
    
                # Important to note that array order append order needs to be the same as the schema fields order.
                timestamps = []
                for delta_time in land_segments_group["delta_time"][offset:offset+chunk_size]:
                    timestamp = GPS_EPOCH + pd.to_timedelta(delta_time+atlas_sdp_gps_epoch, unit='s')
                    timestamps.append(timestamp)
                land_segment_chunks.append(timestamps)
    
                # Add fixed values 
                beam_values = [beam] * len(geometries)
                land_segment_chunks.append(beam_values)
                strength_values = [strength] * len(geometries)
                land_segment_chunks.append(strength_values)
            
            canopy_chunks = self.get_group_chunks(canopy_group, offset, chunk_size)
            terrain_chunks = self.get_group_chunks(terrain_group, offset, chunk_size)
            chunks = land_segment_chunks + canopy_chunks + terrain_chunks
            table = pa.Table.from_arrays(chunks, schema=group_schema)   
            tables.append(table)
        return tables

    def update_schema_geo_metadata(self, results: list[DataGranule]) -> pa.schema:
        """
        Update schema metadata with bounds from the list of granules.
        """
        bounds = self.results_bounds(results)
        
        # Create a copy of geometadata and update the bounds
        updated_geometadata = self.geometadata.copy()
        updated_geometadata["columns"]["geometry"]["bbox"] = bounds
        
        # Update the schema's metadata
        updated_metadata = self.schema.metadata.copy()
        updated_metadata[b"geo"] = json.dumps(updated_geometadata).encode('utf-8')
        
        # Return the schema with updated metadata
        return self.schema.with_metadata(updated_metadata)
    
    def write_results_by_partition(self, results_list: list[DataGranule], fs: fsspec.filesystem, parquet_file): # parquet_file is path or file-like
        results_schema = self.update_schema_geo_metadata(results_list)
        table_writer = pq.ParquetWriter(parquet_file, results_schema)
        beams = ["gt1l", "gt1r", "gt2l", "gt2r", "gt3l", "gt3r"]
        for beam in beams:
            results_tables = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # does it make sense to use the results schema for each table?
                futures = [executor.submit(self.chunks_to_tables, result, fs, beam, results_schema) for result in results_list]
                completed_futures, _ = concurrent.futures.wait(futures) 
                for future in completed_futures:
                    try:
                        results_tables.extend(future.result())
                    except Exception as exception:
                        print(exception) 
                 
                combined_table = pa.concat_tables(results_tables)
                table_writer.write_table(combined_table)
        table_writer.close()
