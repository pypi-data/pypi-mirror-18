=============================
Django Remote Submission
=============================

.. image:: https://badge.fury.io/py/django-remote-submission.png
    :target: https://badge.fury.io/py/django-remote-submission

.. image:: https://travis-ci.org/player1537/django-remote-submission.png?branch=master
    :target: https://travis-ci.org/player1537/django-remote-submission

A Django application to manage long running job submission, including starting the job, saving logs, and storing results.

Documentation
-------------

The full documentation is at https://django-remote-submission.readthedocs.org.

Quickstart
----------

Install Django Remote Submission::

    pip install django-remote-submission

Then use it in a project::

    import django_remote_submission

Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.2.0 (2016-11-17)
++++++++++++++++++

* Add django admin interface.
* Add migrations folder.
* Add log policies for submitting tasks.
* Add return value for modified files.

0.1.1 (2016-11-15)
++++++++++++++++++

* Add port number to Server model.
* Add task to submit jobs.
* Add status updates to task.
* Fix unicode error when submitting jobs.
* Fix verbose/related names for models.

0.1.0 (2016-11-08)
++++++++++++++++++

* First release on PyPI.


