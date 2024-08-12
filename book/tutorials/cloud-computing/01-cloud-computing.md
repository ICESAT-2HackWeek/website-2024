# What is cloud computing?

<br />

**Cloud computing is compute and storage as a service.** The term "cloud computing" is typically used to refer to commercial cloud service providers such as Amazon Web Services, Google Cloud Platform, and Microsoft Azure. These cloud service providers all offer a wide range of computing services, only a few of which we will cover today, via a pay-as-you-go payment structure.

```{image} ./images/AWS_OurDataCenters_Background.jpg
:width: 600px
:clear: both
```

<p style="font-size: 10px;">image src: https://aws.amazon.com/compliance/data-center/data-centers/</p>

>Cloud computing is the on-demand delivery of IT resources over the Internet with pay-as-you-go pricing. Instead of buying, owning, and maintaining physical data centers and servers, you can access technology services, such as computing power, storage, and databases, on an as-needed basis from a cloud provider like Amazon Web Services (AWS). ([source](https://aws.amazon.com/what-is-cloud-computing/))

This tutorial will focus on AWS services and terminology, but Google Cloud and Microsoft Azure offer the same services.

:::{dropdown} 🏋️ Exercise: How many CPUs and how much memory does your laptop have? And how does that compare with hub.cryocloud?</h3>
:open:
If you have your laptop available, open the terminal app and use the appropriate commands to determine CPU and memory.

<div style="float:left; padding: 30px;">

| Operating System (OS) | CPU command                                                                       | Memory Command             |
|-----------------------|-----------------------------------------------------------------------------------|----------------------------|
| MacOS                 | <code>sysctl -a \| grep hw.ncpu</code>                                            | <code>top -l 1 \| grep PhysMem</code> |
| Linux (cryocloud)     | <code>lscpu \| grep "^CPU\(s\):"</code>                                              | <code>free -h</code>       |    
| Windows               | https://www.top-password.com/blog/find-number-of-cores-in-your-cpu-on-windows-10/ |                            |
</div>

Now do the same but on hub.cryointhecloud.com.

Tip: When logged into cryocloud, you can click the ![kernel usage icon](./images/tachometer-alt_1.png) icon on the far-right toolbar.
:::

**What did you find?** It's possible you found that your machine has **more** CPU and/or memory than cryocloud!

:::{dropdown} So why would we want to use the cloud and not our personal computers?
:closed:
  1. Because cryocloud has all the depedencies you need.
  2. Because cryocloud is "close" to the data (more on this later).
  3. Because you can use larger and bigger machines in the cloud (more on this later).
  4. **Having the dependencies, data, and runtime environment in the cloud can simplify reproducible science.**
:::

:::{admonition} Takeaways

* The cloud allows you to access many computing and storage services over the internet. Most cloud services are offered via a "pay as you go" model.
* Hubs like cryointhecloud provide a virtual environment which simplifies reproducible science. You should use them whenever you can!
:::
