Lambpack
========

Creates Python 2.7 packages for AWS Lambda, installing requirements and setting
build-time variables.

Bare minimum
------------

Lambpack’s purposely minimal - it only packages functions. No uploading,
no publishing, no aspirations to become a framework.

Command-line example
--------------------

Given a directory ``my-function`` containing:

* ``index.py`` with a `handler(event, context)`_ function.
* An optional ``requirements.txt`` listing required packages.

Run the following to get ``packaged.zip``, ready for upload to AWS
Lambda:

.. code:: shell

    $ pip install lambpack
    $ lambpack my-function packaged.zip index.handler --env DEBUG=yes --env MY_OTHER_FLAG=123

Your function can access the ``--env`` variables via ``os.environ``.

API example
-----------

As above, but via the API:

.. code:: shell

    import lambpack

    lambpack.to_zip(
        path="my-function",
        dest="packaged.zip",
        handler="index.handler",
        env={
            "ENV": "prod"
        }
    )

See ``src/lambpack/packager.py`` for more info.

.. _`handler(event, context)`: http://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
