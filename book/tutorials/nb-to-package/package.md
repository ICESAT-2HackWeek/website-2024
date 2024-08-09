# Packaging Step by Step

In this lesson, we will go through packaging workflow step by step,
this time, we will also go over the recommended structure of a Python
package and the metadata that are required to make an installable "distribution package".
This will allow you to create a package that can be shared with others easily and installed using `pip`.

## Packaging workflow

For your reference, here is a high-level overview of the workflow again that we will be following in this lesson:

![Simple packaging](../../img/simple-packaging.png)

In the previous lesson, we've gone all the way to step 3. However, we will be starting from scratch in this lesson and go through all the steps again, this time following the best practices for packaging.

## Step 1: Write and run code in Jupyter notebooks

This is already done for us.
We have a Jupyter notebook with some code that we want to package, called [`sample.ipynb`](./sample.ipynb) from previous lesson.

```{admonition} Package goals
For simplicity, let's define a few goals for our package:
1. Install our package using `pip`
2. Run our code from the terminal using a command `eggsample`
```

## Step 2: Extract Python code and create modules

We will extract the Python code from the Jupyter notebook and create a 2 Python modules:

1. `eggsellent_cook.py` - contains the bulk of the code, especially the `EggsellentCook` class.
2. `command_line_interface.py` - contains the command line interface (CLI) code since we're going to create a command line tool `eggsample`.

These code files might look like the following:

````{admonition} File: eggsellent_cook.py
:class: note dropdown
```python
import random

condiments_tray = ["pickled walnuts", "steak sauce", "mushy peas"]

class EggsellentCook:
    FAVORITE_INGREDIENTS = ("egg", "egg", "egg")

    def __init__(self):
        self.ingredients = None
        
    def _add_ingredients(self, ingredients):
        spices = ["salt", "pepper"]
        you_can_never_have_enough_eggs = ["egg", "egg"]
        spam = ["lovely spam", "wonderous spam"]
        more_spam = ["splendiferous spam", "magnificent spam"]
        ingredients = spices + you_can_never_have_enough_eggs + spam + more_spam
        return ingredients
    
    def _prep_condiments(self, condiments):
        condiments.append("mint sauce")
        return ("Now this is what I call a condiments tray!",)

    def add_ingredients(self):
        results = self._add_ingredients(
            ingredients=self.FAVORITE_INGREDIENTS
        )
        my_ingredients = list(self.FAVORITE_INGREDIENTS)
        self.ingredients = my_ingredients + results

    def prepare_the_food(self):
        random.shuffle(self.ingredients)

    def serve_the_food(self):
        condiment_comments = self._prep_condiments(
            condiments=condiments_tray
        )
        print(f"Your food. Enjoy some {', '.join(self.ingredients)}")
        print(f"Some condiments? We have {', '.join(condiments_tray)}")
        if any(condiment_comments):
            print("\n".join(condiment_comments))
            
```
````

````{admonition} File: command_line_interface.py
:class: note dropdown
```python
from eggsellent_cook import EggsellentCook

def main():
    cook = EggsellentCook()
    cook.add_ingredients()
    cook.prepare_the_food()
    cook.serve_the_food()
```
````

Once you have created the two modules,
you can test them by running the following command in your terminal:

```bash
python -c "from command_line_interface import main; main()"
```

This should print out a message with the ingredients and condiments for the food.
Essentially, we've imported the `main` function in `command_line_interface` module,
and then run it, all from the terminal.

```{note}
If you're unfamiliar with the `python -c` command, it allows you to run Python code from the terminal.
```

## Step 3: Place Python modules to designated package directory

In the previous lesson, we simply placed the Python modules in a directory called `eggsample`.
It works, but it's not the best practice, and we saw that it was really hard to
share the package with others, so let's do it the right way this time.

There are two different layouts that you will commonly see
within the Python packaging ecosystem:
[src and flat layouts.](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
we will be using the **src/** layout for creating your Python package.
This layout is recommended in the
[PyPA packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

Okay, let's create the following directory structure, placing the Python modules in the `src/eggsample` directory:

```console
eggsample_repo
├── src                               ┐
│   └── eggsample                     │
│       ├── __init__.py               │ Package source code
│       ├── command_line_interface.py │
│       └── eggsellent_cook.py        ┘
```

````{admonition} Commands hints
:class: hint dropdown

```bash
# Create the directory structure
mkdir -p eggsample_repo/src/eggsample

# Create the __init__.py file
touch eggsample_repo/src/eggsample/__init__.py

# Move the Python modules to the src/eggsample directory
mv eggsellent_cook.py command_line_interface.py eggsample_repo/src/eggsample
```
````

At this point, we essentially have the same directory structure as before,
but this time we have followed the best practice layout for Python packages.
We now have a repository directory `eggsample_repo` with a `src/eggsample` directory
containing the Python modules.

We're now ready to move on to the next step.

## Step 4: Add Python package metadata

In order to make our package installable using `pip`, we need to add some metadata to our package.

Currently if you try to pip install the repository directory `eggsample_repo`, you will get an error:

```bash
pip install ./eggsample_repo
```

````{error}
`ERROR: Directory './eggsample_repo' is not installable. Neither 'setup.py' nor 'pyproject.toml' found.`
````

As you can see, `pip` is looking for either a `setup.py` or `pyproject.toml` file in the repository directory.
We will be using the `pyproject.toml` file to store the metadata for our package, as it is the modern way to store metadata for Python packages. See below about the `pyproject.toml` file.

### About the pyproject.toml file

Every modern Python package should include a `pyproject.toml` file. If your project is pure Python and you're using a `setup.py` or `setup.cfg` file to describe its metadata, you should consider migrating your metadata and build information to a `pyproject.toml` file.

If your project isn’t pure-python, you might still require a `setup.py` file to build the non Python extensions. However, a `pyproject.toml` file should still be used to store your project’s metadata.

```{admonition} What happened to setup.py & how do i migrate to pyproject.toml?
:class: note
Prior to August 2017, Python package metadata was stored either in the `setup.py` file or a `setup.cfg` file. In recent years, there has been a shift to storing Python package metadata in a much more user-readable `pyproject.toml` format. Having all metadata in a single file:

- simplifies package management,
- allows you to use a suite of different [build backends](https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-build-tools.html#build-back-ends) such as (flit-core, hatchling, pdm-build), and
- aligns with modern best practices.
```

Source: https://www.pyopensci.org/python-package-guide/package-structure-code/pyproject-toml-python-package-metadata.html#about-the-pyproject-toml-file

### Create a pyproject.toml file

Let's create a `pyproject.toml` file in the repository directory `eggsample_repo` with the following content:

````{admonition} File: pyproject.toml
:class: note

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "eggsample"
version = "0.1.0"
description = "The eggsample from an eggsellent cook"
requires-python = ">= 3.10"
```
````

The above `pyproject.toml` file contains the following tables:

- `[build-system]` table - It allows you to declare which build backend you use and which other dependencies are needed to build your project.
  - `build-backend`: In our case, we've set our `build-backend` to be [hatchling](https://pypi.org/project/hatchling/), which is the current recommended build backend for Python packages as it is extensible, standards compliant, and easy to use.
  - `requires`: In order to use `hatchling`, we'd need to specify this in the `requires` field. To ensure that the build frontend knows to install this dependency before building the package
- `[project]` table - It contains the metadata for your project, such as the name, version, and description.
  - `name`: The name of the package, in our case, `eggsample`.
  - `version`: The version of the package, in our case, `0.1.0`.
  - `description`: A short description of the package.
  - `requires-python`: The Python version required to run the package. In our case, `>= 3.10`, which means that the package requires Python 3.10 or later.

  For an extensive list of fields that can be included in the `[project]` table, see the [Project Core Metadata](https://packaging.python.org/en/latest/specifications/core-metadata/). We will be adding more metadata to this file in later steps and lessons.

At this point, you should have the following directory structure:

```console
eggsample_repo
├── pyproject.toml              ] Package metadata and build configuration
└── src
    └── eggsample
        ├── __init__.py
        ├── command_line_interface.py
        └── eggsellent_cook.py
```

## Step 5: Install the package

Now that we have added the metadata to our package, we can install it using `pip`:

```bash
pip install -e ./eggsample_repo
```

The `-e` flag is used to install the package in "editable" mode, which means that any changes you make to the package will be reflected in the installed package without having to reinstall it.
This is useful during development when you are actively working on the package.
For a regular installation, you can omit the `-e` flag.

```{note}
`pip` is an example of a build [frontend](https://packaging.python.org/en/latest/glossary/#term-Build-Frontend) that allows us to "install" our package using the build backend that we've specified in the `pyproject.toml` file.

Another build frontend that we will use for package distribution is [build](https://build.pypa.io/en/stable/index.html), which is a is a [PEP 517](https://peps.python.org/pep-0517/) compatible Python package builder. It provides a CLI to build packages, as well as a Python API.
```

Once you've installed the package, you should be able to import the `eggsample` package in Python:

```python
import eggsample
```

That seems to have worked! We've successfully installed our package using `pip`.

We can also see the installed package using the following command:

```bash
pip list | grep eggsample
```

This results in the following output: `eggsample  0.1.0`.
This confirms that our package has been installed successfully and is available for use, with version `0.1.0`.

## Step 6: Create `eggsample` command line tool

We have officially gone through the packaging workflow and have successfully installed our package using `pip`. Congratulations! 🎉

We still haven't fully met our package goals,
which were to run our code from the terminal using a command `eggsample`.

### Run the `main` function in the terminal

First, let's try to run the `main` function again from the `command_line_interface` module,
but this time, we will import from `eggsample.command_line_interface`:

```bash
python -c "from eggsample.command_line_interface import main; main()"
```

````{error}
```console
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/.../.../eggsample/command_line_interface.py", line 1, in <module>
    from eggsellent_cook import EggsellentCook
ModuleNotFoundError: No module named 'eggsellent_cook'
```
````

Oh no! We're getting a `ModuleNotFoundError` for `eggsellent_cook`.
I thought we had everything set up correctly and that the package was installed successfully.
This is a common issue that arises when you're working with packages and modules in this way.
Essentially, the `eggsellent_cook` module is not being found because there is no `eggsellent_cook`
package or module anywhere in the Python path.

There is however an `eggsample.eggsellent_cook` module, which is the correct path to the module.
So let's replace the import statement in `command_line_interface.py` with the correct path:

````{admonition} File: command_line_interface.py
```python
# Old import statement
# from eggsellent_cook import EggsellentCook

# New import statement
from eggsample.eggsellent_cook import EggsellentCook
```
````

Now, let's try running the `main` function again:

```bash
python -c "from eggsample.command_line_interface import main; main()"
```

```console
Your food. Enjoy some egg, egg, wonderous spam, salt, magnificent spam, splendiferous spam, egg, lovely spam, pepper, egg, egg
Some condiments? We have pickled walnuts, steak sauce, mushy peas, mint sauce
Now this is what I call a condiments tray!
```

### Create `scripts` sub-table in `pyproject.toml`

We have successfully run the `main` function from the terminal.
However, we still haven't met our package goals, which were to run our code from the terminal using a command `eggsample`. To call the long command for `python -c` is not user-friendly and not the best way to run a command line tool.

Within the `[project]` table in the `pyproject.toml` file, we can add a `[project.scripts]` sub-table to specify the command line tools that we want to create.

Let's add the following to the `pyproject.toml` file:

````{admonition} File: pyproject.toml
```toml
[project.scripts]
eggsample = "eggsample.command_line_interface:main"
```
````

Once you've added the `[project.scripts]` sub-table to the `pyproject.toml` file, you need to re-install the package again using `pip` since we've made changes to the metadata. The rule of thumb is that whenever you make changes to the metadata, you need to re-install the package.:

```bash
pip install -e ./eggsample_repo
```

Now, you should be able to run the `eggsample` command from the terminal:

```bash
eggsample
```

```console
Your food. Enjoy some magnificent spam, pepper, salt, egg, egg, egg, wonderous spam, splendiferous spam, lovely spam, egg, egg
Some condiments? We have pickled walnuts, steak sauce, mushy peas, mint sauce
Now this is what I call a condiments tray!
```

## Step 7: Share your package

Congratulations! You've successfully created a Python package that can be shared with others easily and installed using `pip`.
To share your package with others at this stage, you can [push your repository to GitHub](#create-push-github),
and then others can install your package using the following command:

```bash
pip install git+https://github.com/lsetiawan/simple_eggsample.git
```

The above example points to a GitHub repository `simple_eggsample` that we've created from the steps above.
You can replace this with your own GitHub repository URL or your neighbor's repository URL if you're feeling generous.

Notice that we're using the `git+` protocol to install the package from a Git repository.
This is a common way to install packages from a Git repository using `pip` and is useful when you want to install a package that is not available on the Python Package Index (PyPI), however it does **require you to have `git` already installed in your system to work**.
See this [blog](https://pythonassets.com/posts/how-to-pip-install-from-a-git-repository/) for a quick overview of the feature of `pip install git+`.

````{admonition} Creating and Pushing to GitHub
:class: tip dropdown
:name: create-push-github

If you're unfamiliar with creating a GitHub repository and pushing your code to GitHub, you can follow the steps below:

1. In the upper-right corner of any page, select `+`, then click **New repository** to create a new remote repository on GitHub.
2. In the "Repository name" box, type `eggsample_repo`.
3. In the "Description" box, type a short description. For example, type "This repository is for practicing packaging Python code".
4. Select **Public**.
5. Click **Create repository**. *Note: There are other options you can select, but for now, we'll keep it simple and select the default options.*
6. You now should have a new repository on GitHub.
To connect your local repository to the remote repository,
first, we'll need to initialize git in the `eggsample_repo` directory:

    ```bash
    git init
    ```
7. Next, we'll add the remote repository URL:

    ```bash
    git remote add origin https://github.com/<username>/eggsample_repo.git
    ```

    Replace `<username>` with your GitHub username.

8. Because we've started running the package, you might find a `__pycache__` directory in your source code.
This is simply a cache directory created by Python to store compiled bytecode files.
You can add this to your `.gitignore` file, which tells Git to ignore this directory:

    ```bash
    echo "__pycache__" >> .gitignore
    ```

9. Now, you can add all the files to the staging area, commit the changes, and push the code to the remote repository:

    ```bash
    git add .
    git commit -m "Initial commit"
    git push origin main
    ```
````

## Summary

Let's summarize what we've done in this lesson:

- We've extracted the Python code from the Jupyter notebook and created two Python modules: `eggsellent_cook.py` and `command_line_interface.py`.
- We've placed the Python modules in the `src/eggsample` directory, following the best practice layout for Python packages.
- We've added metadata to our package by creating a `pyproject.toml` file in the repository directory `eggsample_repo`.
- We've installed the package using `pip` and verified that it was installed successfully.
- We've created a command line tool `eggsample` that runs the `main` function from the `command_line_interface` module.

At the very core, now you've learned how to package your Python code into a Python package that can be shared with others easily and installed using `pip`.
This is a significant milestone in your Python journey, and you should be proud of yourself for reaching this point.
In the next lesson we will go over adding more supplemental files to your package,
so that you can have a more complete package that can be shared and published for community use.
