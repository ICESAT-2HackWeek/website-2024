# Cloud-Optimized Data Access

Recall from the introduction that cloud object storage is accessed over the network. Local file storage access will always be faster but there are limitations. This is why the design of file formats in the cloud requires more consideration than local file storage.

## 🏋️ Exercise

:::{dropdown} What are some limitations of local file storage?
:closed:
See the table from the [Cloud Data Access Notebook](./02-cloud-data-access.ipynb)
:::

## Why you should care

Reading ICESat-2 (and other formats which are not cloud optimized) files can be slow! It is nice to know why and possibly advocate for things to be better!

:::{seealso}
1. [Cloud-Optimized HDF5 Files – Aleksandar Jelenak, The HDF Group](https://www.youtube.com/watch?v=bDH59YTXpkc)
2. [HDF at the speed of Zarr - Luis Lopez, Pangeo Showcase](https://docs.google.com/presentation/d/1iYFvGt9Zz0iaTj0STIMbboRKcBGhpOH_LuLBLqsJAlk/edit?usp=sharing) is a presentation all about Cloud-Optimizing ICESat-2 Products
3. A notebook demonstrating how to repack ATL03 product to cloud-optimized (for a subset of datasets): [rechunking_atl03.ipynb](https://gist.github.com/abarciauskas-bgse/8bf4388f8f8989582c807b2451c5cf8c)
:::

## What are we optimizing for and why?

The "optimize" in cloud-optimized is to **minimize data latency** and **maximize throughput** by:

* Making as few requests as possible
* Making even less for metadata, preferably only one
* Using a file layout that simplifies accessing data for parallel reads.

:::{attention} A future without file formats
Some day we won't have to think about file formats. The geospatial software community is working on ways to make all collections appear as logical datasets, so you can query them without having to think about files.
:::

## Anatomy of a structured data file

```{image} ./images/hdf5_structure4.jpg
:width: 500px
```

<p style="font-size:10px">img source: https://www.neonscience.org/resources/learning-hub/tutorials/about-hdf5</p>

A structured data file is composed of two parts: metadata and data. Metadata is information about the data, such as the data shape, data type, the data variables, the data's coordinate system, and how the data is stored, such as chunk shape and compression. Data is the actual data that you want to analyze.

We can optimize this structure for reading from cloud storage.

## How do we accomplish cloud-optimization?

You are probably familiar with the following file formats: HDF5, NetCDF, GeoTIFF. You can actually make any of these formats "cloud-optimized" by:

1. Separate metadata from data and store it contiguously data so it can be read with one request.
2. Store data in chunks, so the whole file doesn't have to be read to access a portion of the data.
3. Make sure chunks of data are not too small, so more data can be fetched with each request.
4. Make sure the chunks are not too large, which means more data has to be transferred and decompression takes longer.
5. Compress these chunks so there is less data to transfer.

:::{note} Lazy loading

**Separating metadata from data supports lazy loading, which is key to working quickly when data is in the cloud.** Libraries, such as xarray, first read the metadata. They defer actually reading data until it's needed for analysis. When a computation of the data is called, libraries use [HTTP range requests](https://http.dev/range-request) to request only the chunks required. This is also called "lazy loading" data. See also [xarray's documentation on lazy indexing](https://docs.xarray.dev/en/latest/internals/internal-design.html#lazy-indexing).

:::

## An analogy

When you lived at home with your parents, everything was right there when you needed it (local file storage). Let's say you're about to move away to college (the cloud), and you are not allowed to bring anything with you. You put everything in your parent's (infinitely large) garage (cloud object storage). Given you would need to have things shipped to you, would it be better to leave everything unpacked? To put everything all in one box? A few different boxes? And what would be the most efficient way for your parents to know where things were when you asked for them?

```{image} ./images/dalle-college.png
:width: 400px
```
<p style="font-size:10px">image generated with ChatGPT 4</p>

:::{attention} Opening Arguments
A few arguments used to open the dataset also make a huge difference, namely with how libraries, such as s3fs and h5py, cache chunks.

For s3fs, use [`cache_type` and `block_size`](https://s3fs.readthedocs.io/en/latest/api.html?highlight=cache_type#s3fs.core.S3File)

For h5py, use [`rdcc_nbytes` and `page_buf_size`](https://docs.h5py.org/en/stable/high/file.html#h5py.File)
:::

:::{admonition} Takeaways

* Understanding file formats may help in diagnosing issues when things are slow.
* You can make files cloud-optimized by separating metadata and storing it contiguously so it can all be read in one request.
* You can use arguments to libraries like s3fs and h5py to support caching.
:::
