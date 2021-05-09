# Maktabkhooneh Downloader

# Introduction

[Maktabkhooneh](http://maktabkhooneh.org) is great in preparing *massive open online courses* (MOOC) for Persian user -- gathering its courses from  the best universities of IRAN like [Sharif University of Technology](http://sharif.edu). Maktabkooneh has started since 2011.

This script help you to batch download videos for Maktabkhooneh courses.
In order to have access to the video links of any courses you need an account.


# Installing dependencies

You can use the `pip` program to install the dependencies on your own.  They are all listed in the `requirements.txt` file.

To use this method, you would proceed as:

```python
pip install -r requirements.txt
```

To make Firefox work with Python selenium, you need to install the *geckodriver*. The geckodriver driver will start the real firefox browser and supports Javascript.

# Running the script
Refer to `maktabkhooneh-dl --help` for a complete, up-to-date reference on the runtime options supported by this utility.

Run the script to download the materials by providing your Maktabkhooneh account credentials (e.g. email address and  password), the class names, as well as any additional parameters:

```python
coursera-dl -u <user> -p <pass> آموزش-رایگان-تحلیل-هوشمند-تصاویر-زیست-پزشکی-mk1070
```
