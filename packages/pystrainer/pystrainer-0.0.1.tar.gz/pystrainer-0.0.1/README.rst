Strainer: Fast Functional Serializers
=====================================

.. image:: https://img.shields.io/pypi/v/pystrainer.svg
    :target: https://pypi.python.org/pypi/pystrainer

Strainer is a different take on serialization and validation in python.
It utilizes a functional style over inheritance.

An example of Strainer, the example has been borrowed from `Marshmallow <https://marshmallow.readthedocs.io/en/latest/>`_

.. code-block:: python

    artist_serializer = create_serializer(
      field('name')
    )

    album_schema = create_serializer(
      field('title'),
      field('release_date'),
      child('artist', serializer=artist_serializer)
    )

    class Artist(object):
        def __init__(self, name):
            self.name = name

    class Album(object):
        def __init__(self, title, release_date, artist):
            self.title = title
            self.release_date = release_date
            self.artist = artist

    bowie = Artist(name='David Bowie')
    album = Album(
        artist=bowie,
        title='Hunky Dory',
        release_date=date(1971, 12, 17)
    )

    simple_data = album_schema.to_representation({}, album)

    pprint.pprint(simple_data)

    # {'artist': {'name': 'David Bowie'},
    #  'release_date': datetime.date(1971, 12, 17),
    #  'title': 'Hunky Dory'}


Installation
------------

To install Strainer, simply:

.. code-block:: bash

    $ pip install pystrainer
    ✨🍰✨

Satisfaction, guaranteed.

Documentation
-------------

Fantastic documentation is available at http://docs.python-requests.org/, for a limited time only.


How to Contribute
-----------------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. There is a `Contributor Friendly`_ tag for issues that should be ideal for people who are not very familiar with the codebase yet.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

.. _`the repository`: http://github.com/kennethreitz/requests
.. _AUTHORS: https://github.com/kennethreitz/requests/blob/master/AUTHORS.rst
.. _Contributor Friendly: https://github.com/kennethreitz/requests/issues?direction=desc&labels=Contributor+Friendly&page=1&sort=updated&state=open
