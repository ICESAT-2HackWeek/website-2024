# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Machine Learning with ICESat-2 data
#
# A machine learning pipeline from point clouds to photon classifications.
#
# Reimplementation of
# https://github.com/YoungHyunKoo/IS2_ML/blob/main/01_find_overlapped_data.ipynb

# %% [markdown]
# ```{admonition} Learning Objectives
# By the end of this tutorial, you should be able to:
# - Convert ICESat-2 point cloud data into an analysis/ML-ready format
# - Recognize the different levels of complexity of ML approaches and the
#   benefits/challenges of each
# - Learn the potential of using ML for ICESat-2 photon classification
# ```

# %% [markdown]
# ## Part 0: Setup

# %%
import geopandas as gpd
import h5py
import icepyx as ipx
import s3fs
import torch

# %% [markdown]
# ## Part 1: Convert ICESat-2 data into ML-ready format
#
# Steps:
# - Access using icepyx
# - Filter to only strong beams
# - Subset to 6 data variables only
#
# TODO: copy Table 1 from Koo et al., 2023 paper

# %%
# Set up spatiotemporal query for ATL07 sea ice product
region_ross = ipx.Query(
    product="ATL07",
    spatial_extent=[-180, -78, -140, -70],
    date_range=["2018-09-15", "2019-03-31"],
    version="006",
)

# %%
region_ross.visualize_spatial_extent()

# %%
s3links = region_ross.avail_granules(cloud=True)
# s3links

# %%
# Authenticate using NASA EarthData login; enter your user id and password when prompted
credentials = region_ross.s3login_credentials
credentials

# %%
s3 = s3fs.S3FileSystem(
    key=credentials["accessKeyId"],
    secret=credentials["secretAccessKey"],
    token=credentials["sessionToken"],
)

# %%
# the first index, [0], gets us into the list of s3 urls
# the second index, [1], gets us the second entry in that list.
s3url = s3links[0][1]
s3url

# %%
s3file = s3.open(s3url, mode="rb")

# %%
# %%time
atl_file = h5py.File(name=s3file, mode="r")
atl_file.keys()

# %% [markdown]
# ### Get strong beams only
#
# Ref: https://github.com/ICESAT-2HackWeek/strong-beams

# %%
# orientation - 0: backward, 1: forward, 2: transition
orient = atl_file["orbit_info"]["sc_orient"][:]
if orient == 0:
    strong_beams = ["gt1l", "gt2l", "gt3l"]
elif orient == 1:
    strong_beams = ["gt3r", "gt2r", "gt1r"]
strong_beams

# %%
for beam in strong_beams:
    print(beam)

# %% [markdown]
# Data variables to use:
#   1. `photon_rate`: photon rate
#   2. `hist_w`: width of the photon height distribution
#   3. `background_r_norm`: background photon rate
#   4. `height_segment_height`: relative surface height
#   5. `height_segment_n_pulse_seg`: number of laser pulses
#   6. `hist_mean_h` - `hist_median_h`: difference between mean and median height
#
# TODO link to data dictionary

# %%
gdf = gpd.GeoDataFrame(
    data={
        "photon_rate": atl_file[f"{beam}/sea_ice_segments/stats/photon_rate"][:],
        "hist_w": atl_file[f"{beam}/sea_ice_segments/stats/hist_w"][:],
        "background_r_norm": atl_file[
            f"{beam}/sea_ice_segments/stats/background_r_norm"
        ][:],
        "height_segment_height": atl_file[
            f"{beam}/sea_ice_segments/heights/height_segment_height"
        ][:],
        "height_segment_n_pulse_seg": atl_file[
            f"{beam}/sea_ice_segments/heights/height_segment_n_pulse_seg"
        ][:],
        "hist_mean_h": atl_file[f"{beam}/sea_ice_segments/stats/hist_mean_h"][:],
        "hist_median_h": atl_file[f"{beam}/sea_ice_segments/stats/hist_median_h"][:],
    },
    geometry=gpd.points_from_xy(
        x=atl_file[f"{beam}/sea_ice_segments/longitude"][:],
        y=atl_file[f"{beam}/sea_ice_segments/latitude"][:],
    ),
    crs="OGC:CRS84",
)
print(f"Total number of rows: {len(gdf)}")

# %%
gdf

# %% [markdown]
# ### Save to GeoParquet

# %% [markdown]
# Let's save the ATL07 photon data to a GeoParquet file so we don't have to run all the
# download and filtering code above again.

# %%
gdf.to_parquet(
    path="ATL07_photons.gpq", compression="zstd", schema_version="1.0.0-beta.1"
)

# %% [markdown]
# ```{note} To compress or not?
# When storing your data, note that there is a tradeoff in terms of compression and read
# speeds. Uncompressed data would typically be fastest to read (assuming no network
# transfer) but result in large file sizes. We'll choose Zstandard (zstd) as the
# compression method here as it is typically faster to read (compared to the default
# 'snappy' compression codec), and still compresses well into a small file size.
# ```

# %%
# Load GeoParquet file back into geopandas.GeoDataFrame
gdf = gpd.read_parquet(path="ATL07_photons.gpq")

# %%

# %% [markdown]
# ## Part 2: Choosing a Machine Learning algorithm

# %% [markdown]
# ### Moving data from CPU to GPU
#
# Machine learning models are compute intensive, and typically run on specialized
# hardware called Graphical Processing Units (GPUs) instead of ordinary CPUs. Depending
# on your input data format (images, tables, audio, etc), and the machine learning
# library/framework you'll use (e.g. Pytorch, Tensorflow, RAPIDS AI CuML, etc), there
# will be different ways to transfer data from disk storage -> CPU -> GPU.
#
# For this exercise, we'll be using [PyTorch](https://pytorch.org), and do the following
# data conversions:
#
# [`geopandas.GeoDataFrame`](https://geopandas.org/en/v1.0.0/docs/reference/api/geopandas.GeoDataFrame.html) ->
# [`pandas.DataFrame`](https://pandas.pydata.org/pandas-docs/version/2.2/reference/api/pandas.DataFrame.html) ->
# [`torch.Tensor`](https://pytorch.org/docs/2.4/tensors.html#torch.Tensor) ->
# [torch `Dataset`](https://pytorch.org/docs/2.4/data.html#torch.utils.data.Dataset) ->
# [torch `DataLoader`](https://pytorch.org/docs/2.4/data.html#torch.utils.data.DataLoader)

# %%
# Select data variables from DataFrame that will be used for training
df = gdf[
    [
        "photon_rate",
        "hist_w",
        "background_r_norm",
        "height_segment_height",
        "height_segment_n_pulse_seg",
        "hist_mean_h",
        "hist_median_h",
    ]
]
tensor = torch.tensor(data=df.values)  # convert pandas.DataFrame to torch.Tensor
assert tensor.shape == torch.Size([54053, 7])  # (rows, columns)
dataset = torch.utils.data.TensorDataset(tensor)  # turn torch.Tensor into torch Dataset
dataloader = torch.utils.data.DataLoader(  # put torch Dataset in a DataLoader
    dataset=dataset,
    batch_size=128,  # mini-batch size
    shuffle=True,
)

# %% [markdown]
# PyTorch's [`DataLoader`](https://pytorch.org/docs/2.4/data.html#torch.utils.data.DataLoader)
# is a convenient container to hold tensor data, and makes it easy for us to iterate
# over mini-batches using a for-loop.)

# %%
for batch in dataloader:
    minibatch: torch.Tensor = batch[0]
    assert minibatch.shape == (128, 7)
    assert minibatch.device == torch.device("cpu")  # Data is on CPU

    minibatch = minibatch.to(device="cuda")  # Move data to GPU
    assert minibatch.device == torch.device("cuda:0")  # Data is on GPU now!

    break

# %%

# %% [markdown]
# ## Part 3: Training the neural network
#
# Use multi-layer perceptron with:
# - 2 hidden layers, 50 nodes each
# - tanh activation function
# - final layer with 3 nodes, for 3 surface types (open water, thin ice, thick/snow-covered ice)
# - Adam optimizer

# %%

# %%

# %% [markdown]
# ## References
# - Koo, Y., Xie, H., Kurtz, N. T., Ackley, S. F., & Wang, W. (2023).
#   Sea ice surface type classification of ICESat-2 ATL07 data by using data-driven
#   machine learning model: Ross Sea, Antarctic as an example. Remote Sensing of
#   Environment, 296, 113726. https://doi.org/10.1016/j.rse.2023.113726


# %%
