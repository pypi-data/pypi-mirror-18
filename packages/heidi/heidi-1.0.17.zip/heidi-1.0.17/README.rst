ReadLess 
==========

A python module for conversation and text summarization and much more
exciting features.

*Features* provided by this module:

-  **Text Segmentation** using:

   -  **TextTiling** with **Block Score**
   -  **TextTiling** with **Vocabulary introduction**
-  **Conversational summarization** using:

   -  **Cluster Rank**
-  **Text summarization** using :

   -  **TextRank**
   -  **Random**

Installation
------------

Make sure you have `Python`_ 2.7/3.3+ and `pip`_\ (`Windows`_, `Linux`_)
installed. Run simply (preferred way):

.. code:: sh

    $ [sudo] pip install readless

Or for the latest version in development:

.. code:: sh

    $ [sudo] pip install git+git://github.com/adichat/read-less.git

ReadLess API
------------

You can use readless like a library in your project.

For quickly summarizing a conversation using ClusterRank algorithm:

.. code:: python

    # -*- coding: utf8 -*-

    from readless.Summarization import clusterrank
    summarizer = clusterrank.ClusterRank()
    pathToFile = "C:/conversation.in"
    summary = summarizer.summarizeFile(pathToFile)

For segmenting a text using TextTiling algorithm:

.. code:: python

    # -*- coding: utf8 -*-

    from readless.Segmentation import texttiling
    segmentation = texttiling.TextTiling()
    pathToFile = "C:/conversation.in"
    segmentedText = segmentation.segmentFile(pathToFile)

For a detailed list of other API functionalities, see `**ReadLess
Documentation**`_.

Contributions
-------------

All contributions are welcomed. This module is in development and there
are several scopes of improvement. Tests are to be implemented along
with other Summarization algorithms with support for web page
summarization. For upcoming features, see `Future developments`_.

`LICENSE`_
~~~~~~~~~~~~

.. _Python: http://www.python.org/
.. _pip: https://crate.io/packages/pip/
.. _Windows: http://docs.python-guide.org/en/latest/starting/install/win/
.. _Linux: http://docs.python-guide.org/en/latest/starting/install/linux/
.. _**ReadLess Documentation**: 
.. _Future developments: 
.. _LICENSE: https://github.com/AdiChat/Read-Less/blob/master/LICENSE