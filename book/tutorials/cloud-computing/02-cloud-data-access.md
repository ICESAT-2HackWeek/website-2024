# Cloud Data Access

<br />

## NASA's migration from "on-premise" to cloud

```{image} ./images/DAAC_map_new.jpg
:width: 700px
:align: left
```
<p style="font-size: 10px">image src: https://asf.alaska.edu/about-asf-daac/</p>

NASA has 12 Distributed Active Archive Centers (DAACs). Each DAAC is associated with a few sub-disciplines of Earth science, and those specialties correspond to which missions and data products those DAACs are in charge of. For example, LPDAAC is the land processes DAAC and is in charge of the Harmonized Landsat Sentinel Product (HLS) which is often used for land classification. Up until about 6 years ago (which as it so happens is when I started working with NASA), all NASA Earth Observation archives resided "on-premise" at the data center's physical locations in data centers they manage.

NASA, anticipating the exponential growth in their Earth Observation data archives, started the [Earthdata Cloud](https://www.earthdata.nasa.gov/eosdis/cloud-evolution) intiative. Now, NASA DAACs are in the process of migrating their collections to cloud storage. Existing missions are contributing, but new missions such as NISAR and SWOT are significant drivers to this archival volume growth.


```{image} ./images/archive-growth-FY22.jpg
:width: 900px
:align: center
```
<p style="font-size: 10px">image src: https://www.earthdata.nasa.gov/esds/esds-highlights/2022-esds-highlights</p>

Now, high priority and new datasets are being stored on **cloud object storage**.

<br />

## What is cloud object storage?

Cloud object storage stores and manages unstructured data in a flat structure (as opposed to a hierarchy as with file storage). Object storage is distinguished from a database, which requires software (a database management system) to store data and often has connection limits. Object storage is distinct from local file storage, because you access cloud object storage over a network connection, whereas local file storage is accessed by the central processing unit (CPU) of whatever server you are using.

Cloud object storage is accessible using HTTP or a cloud-object storage protocol, such as AWS' Simple Storage Service (S3). Access over the network is critical because it means many servers can access data in parallel and these storage systems are designed to be infinitely scalable and always available.

[ADD MORE EXPLANATION + EXAMPLE OF S3 PROTOCOL]
[ADD IMAGE OR DIAGRAM]

:::{dropdown} 🏋️ Exercise: Datasets on Earthdata Cloud
:open:

Navigate [https://search.earthdata.nasa.gov](https://search.earthdata.nasa.gov), search for ICESat-2 and answer the following questions:

* Which DAAC hosts ICESat-2 datasets?
* Which ICESat-2 datasets are hosted on the AWS Cloud and how can you tell?
:::


## There are different access patterns, it can be confusing! 🤯

Here are a likely few:
1. Download data from a DAAC to your local machine.
2. Download data from cloud storage to your local machine.
3. Download data from a DAAC to a virtual machine in the cloud (when would you do this?).
4. Login to a virtual machine in the cloud, like cryointhecloud, and access data directly.

```{image} ./images/different-modes-of-access.png
:width: 1000px
:align: center
```

:::{dropdown} Which should you chose and why?
:closed:
  You should use option 4 - direct access. Because S3 is a cloud service, egress (files being download outside of AWS services) is not free.
  **You can only directly access (both partial reading and download) files on S3 if you are in the same AWS region as the data. This is so NASA can avoid egress fees 💸 but it also benefits you because this style of access is much faster.**
  The good news is that cryointhecloud is located in AWS us-west-2, the same region as NASA's Earthdata Cloud datasets!

  Of course, you may still need to access datasets from on-prem servers as well.

  <h3>Caveats</h3>
  <ul>
  <li>Direct S3 access could refer to either copying a whole file using the S3 protocol OR using lazy loading and reading just a portion of the file and the latter usually only performs well for cloud-optimized files.</li>
  <li>Having local file system access will always be faster than reading all or parts of a file over a network, even in region (although S3 access is getting blazingly fast!) You can move data files onto a file system mounted onto a virtual machine, which would result in the fastest access and computation. But before architecting your applications this way, consider the tradeoffs of reproducibility (e.g. you'll have to move the data ever time), cost (e.g. storage volumes can be more expensive than object storage) and scale (e.g. there is usually a volume size limit, except in the case of [AWS Elastic File System](https://aws.amazon.com/efs/) which is even more pricey!).</li>
      
  </ul>
:::

## Cloud vs Local Storage

:::{list-table} Cloud vs Local Storage
:header-rows: 1

*   - Feature
    - Local
    - Cloud
*   - Scalability
    - ❌ limited by physical hardware
    - ✅ highly scalable
*   - Accessibility
    - ❌ access is limited to local network or complex setup for remote access
    - ✅ accessible from anywhere with an internet connection
*   - Collaboration
    - ❌ sharing is hard
    - ✅ sharing is possible with tools for access control
*   - Data backup
    - ❌ risk of data loss due to hardware failure or human error
    - ✅ typically includes redundancy ([read more](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DataDurability.html))
*   - Performance
    - ✅ faster since it does not depend on any network
    - ❌ performance depends on internet speed or proximity to the data
:::


:::{admonition} Takeaways

1. NASA datasets are still managed by DAACs, even though many datasets are moving to the cloud.
2. Users are encouraged to access the data directly in the cloud through AWS services (like cryocloud!)
:::
