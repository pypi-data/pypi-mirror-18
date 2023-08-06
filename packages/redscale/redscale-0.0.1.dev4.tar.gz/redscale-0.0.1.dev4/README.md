RedScale
========

RedScale is set of tools for managing OpenStack clouds.

Installation
------------

To install redscale on your system, run the following command:

    sudo pip install redscale

RedScale Tools
--------------

### CID (Can I deploy?)

cid will let you know if you have enough resources to deploy on your cloud.

You can use it by speciying how many resources you plan to use::

    cid --memory 4 --cpu 2

Or by specifying the flavor and amount of nodes you'll deploy::

    cid --flavor m1.large --amount 3

Add a new tool
--------------

### Requirements

* Must have a parser. This parser should be part of the class attributes

* Must be described here in the readme or any other type of doc inside this repository


How to contribute?
------------------

Using pull requests :)
If you are adding a new app, make sure it answers all the requirements listed above.
