|image0| |Code Health| |Code Climate|

Python SDK for Cisco IMC
========================

-  Apache License, Version 2.0 (the "License")

Documentation
-------------

https://ciscoucs.github.io/imcsdk\_docs/

Installation
------------

The SDK can be installed using any of ways below

>From pip:
~~~~~~~~~

Installs the last released version

::

        pip install imcsdk


>From github:
~~~~~~~~~~~~

Installs the latest top of the tree development version

::

        # Install pip (skip if pip is already available):
        wget https://bootstrap.pypa.io/get-pip.py
        python get-pip.py

        git clone https://github.com/ciscoucs/imcsdk.git
        cd imcsdk
        make install


Community:
----------

-  We are on Slack - slack requires registration, but the ucspython team
   is open invitation to anyone to register
   `here <https://ucspython.herokuapp.com>`__

.. |image0| image:: https://ucspython.herokuapp.com/badge.svg
   :target: https://ucspython.herokuapp.com
.. |Code Health| image:: https://landscape.io/github/CiscoUcs/imcsdk/master/landscape.svg?style=flat
   :target: https://landscape.io/github/CiscoUcs/imcsdk/master
.. |Code Climate| image:: https://codeclimate.com/github/CiscoUcs/imcsdk/badges/gpa.svg
   :target: https://codeclimate.com/github/CiscoUcs/imcsdk


=======
History
=======

0.9.1.0 (2016-11-25)
--------------------
* Support for C3260 platform
* Supports every Managed Object exposed by IMC upto version 2.0(13e)
* Support to invoke APIs on individual server modules in case of C3260 platform
* Support for TLSv1.1/v1.2 and fallback to TLSv1 for older versions
* Support to filter out non-applicable properties based on the C-series platform
* Validation of Managed Object version with the C-series version for better error-handling 

0.9.0.3 (2016-08-25)
--------------------
* Added APIs layer to the sdk

0.9.0.1 (2016-08-25)
--------------------
* Fixed an issue with pip install

0.9.0.0 (2016-08-25)
--------------------
* Python SDK for IMC rack server management and related automation
* Supports every Managed Object exposed by IMC
* APIs for CRUD operations simplified
* Runtime memory usage is reduced
* Nosetests for unit testing
* Samples directory for more real world use cases
* Integrating the sphinx framework for documentation
* PEP8 Compliance


