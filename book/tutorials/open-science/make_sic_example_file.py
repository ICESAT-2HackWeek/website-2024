"""Creates a npy binary file containing December 2022 sea ice 
concentration from NSIDC 0051 that is used as an example in
the ICESat-2 Hackweek 2024 Open Science Tutorial"""

from pathlib import Path

import xarray as xr
import numpy as np

DATAPATH = Path.home() / "Data" / "Sunlight_under_seaice" / "SIC" / "NSIDC-0051" / "raw"
EXAMPLE_PATH = Path("example_data")

# The original files contain mask values in the data arrays
# these are interpretted as concentrations greater than 1 when
# decoded.  decode_cf=False is used to avoid decoding until
# mask values can be removed.
df = xr.open_mfdataset(DATAPATH.glob("*.nc"), 
                       combine="by_coords", 
                       decode_cf=False)

# Set mask values to NaN and scale to convert binary 
# values to floats with range 0. to 1.
datacube = df.F17_ICECON.where(df.F17_ICECON <= 250).values
datacube = datacube * df.F17_ICECON.attrs["scale_factor"]

# Write to file
with open(EXAMPLE_PATH / "sic.202212.npy", "wb") as f:
    np.save(f, datacube)

# Create a mask array
mask = df.F17_ICECON.where(df.F17_ICECON > 250)[0,:,:]
with open(EXAMPLE_PATH / "sic.mask.npy", "wb") as f:
    np.save(f, mask)