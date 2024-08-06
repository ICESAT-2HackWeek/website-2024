# Packaging notebook introduction and demo

This notebook demonstrates how powerful packaging your Python code
can be ... even for yourself.

Before we get ahead of ourselves. Let's think about the **WHY**.
You might ask yourself:

- why would I want to package my code?
- can't I just pass around notebooks?
- what's the point of all this?
- what is the meaning of life?

... well, maybe not the last one. But the others are valid questions.

## What is a Python package?

A "package" or officially called a "distribution package" is simply
a directory of Python modules and sub-packages with an `__init__.py` file
that allows for the modular organization of code.
It can be be installed and distributed for use by others.

![Bedroom](https://images.unsplash.com/photo-1630699293259-0b6c08606c62?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)

Let's think about this in a simpler term. We can think of a
package like a room in a house. Say the "bedroom" is a package.
Inside the bedroom, you have a bed, a nightstand, and a closet.

- The bed and nightstand are like *modules* in a package.
- The closet is like a *sub-package* in a package, since there might be other
furniture pieces in a closet like a dresser; some closets can even be a whole room!

### Module

A module is a single file of Python code that can be imported into Python
scripts or other modules,
also known officially as an "import package".
This is the smallest unit of code reuse in Python.
You'll see these as `.py` files.

As example, you can create a `hello_world` module by doing the following:

1. Create a file called `hello_world.py` with the following content:

    ```python
    def say_hello():
        print("Hello, World!")
    ```

2. Then, you can import this module in another Python script or notebook:

    ```python
    from hello_world import say_hello

    say_hello()
    ```

    This will print `Hello, World!` to the console.

This is a simple example of a module, but you can have more complex modules with many functions and classes.

![Bed](https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?q=80&w=3871&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)

Going back to the bedroom analogy, a module is like a single piece of furniture in a room.
For example, a bed is a piece of furniture that we spend most of our life on,
this "bed" might be made up of various parts like a headboard, frame, and mattress.
Each of these parts can be thought of as a function or class in a module.

### Library

A library is a collection of modules and packages that provide specific functionality or a set of related functionalities.
In the Python ecosystem, a library is often used interchangeably with the term "package", and this can be confusing.
For example, [Matplotlib](https://matplotlib.org/) is a plotting library that contains many modules to help you plot data
or [Xarray](http://xarray.pydata.org/en/stable/) is a library that includes several modules and packages to help you work with labeled multi-dimensional arrays.
You can "include" these libraries in your program to add features without reinventing the wheel.

![blueprint](https://images.pexels.com/photos/4792480/pexels-photo-4792480.jpeg)

To make it clear, let's go back to the bedroom analogy.
A library is like a collection of rooms in a house, it is beyond just a single room.
It is the house itself, which contains many rooms.
Different house or even a commercial space might have different purposes and functionalities.

### The Python Terms Hierarchy

Here's a hierarchy of Python terms from smallest to largest to help you understand the relationship between modules, packages, and libraries:

<img src="../../img/code-to-package.png" alt="functions to libraries" width="200"/>

A python package may look like the following:

```console
mypackage/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        submodule1.py
        submodule2.py

```

Within the `mypackage` package and its subpackages, you might import functions from a dependency like `numpy`
within a module file. Once this set of packages is bundled together and distributed,
you'll end up essentially with a library that can be installed and used by others.

This action of bundling your code together into a package or library is called "packaging" your code.

```{note}
For the rest of this tutorial, we'll use the term "package" to refer to a collection of code that can be installed and used by others,
which essentially means a **library**.
```

## Why package your code?

Now you know what it means for a collection of code to be a package.
But there's still the question of why you would want to package your code?

Here are some reasons:

- **Reusability**: you can reuse your code in other projects without having to copy and paste it.
- **Maintainability**: you can maintain your code in a single place and update it without having to update it in multiple places.
- **Collaboration**: you can share your code with others and they can use it without having to understand the internals.
- **Distribution**: you can distribute your code to others and they can install it like any other package.

## The workflow

At this point, hopefully you're convinced that packaging your code is a good idea.
But how do you do it? There are many ways to package your code,
but we'll focus on a simple way to package your code with a best practice workflow recommended by the [Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/),
a working group that maintains a core set of software projects used in Python packaging.

PyPA have a guide called the [Python Packaging User Guide](https://packaging.python.org/),
which is the authoritative resource on how to package, publish, and install Python projects using current tools.
We will follow the guide to package our code, but we'll simplify it a bit to make it easier to understand and more practical for our scientific software development workflow.

Here's an overview of what a full workflow from notebooks to a package looks like:

![Simple packaging](../../img/simple-packaging.png)

With this workflow, let's package a sample python code that we have in the [`sample.ipynb`](./sample.ipynb) notebook into a package called `eggsample`.

The goal is that once this code is packaged,
we can install it, then, from a command line,
we can run the code with a command `eggsample` and it will output on the terminal console, the same output as running the code in the notebook.
Simple enough? Well, let's get started!

## Demo

TODO: Add demo here
