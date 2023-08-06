Synopsis
--------

Mimir is a simple, command line based note taking application. Designed
with git syntax and usage in mind, its aim is to provide quick, concise
notes, that can be easily included in the project/directory where they
are created.

Code Example
------------

Mimir can be initialized within any directory. Each mimir instance keep
track of its own notes.

Initialize mimir within a directory:

.. code:: bash

    mimir init

This will create a new directory, .mimir, and a config file,
.mimir/.mimir-config

Delete mimir from a directory:

.. code:: bash

    mimir delete

This deletes the mimir present in the working directory. It will also
delete any config files and all notes.

To create a new note, simply:

.. code:: bash

    mimir This is my brand new note!

Or, to add a new note with tags:

.. code:: bash

    mimir This is a note with a @tag

The note will be added to ``.mimir/mimir_notes.txt``

To show notes:

.. code:: bash

    mimir -s 1
    mimir -s 2

Will show the last one and two notes, respectively.

.. code:: bash

    mimir @tag1
    mimir @tag1 @tag2

If only tags are provided to mimir, it will assume you want to search by
tags, rather than create a new note

Notes can also be searched via date fences:

.. code:: bash

    mimir --since 2010 --until october
    mimir --since june
    mimir --until 2015

Date fences can be mixed with tags and the -s option for more fine
grained searching.

To edit notes:

.. code:: bash

    mimir edit

This will open the mimir notes file in your specified editor (this must
be set in .mimir-config)

All notes in your Mimir notes file can be synced to an Evernote account.
This requires an evernote account, as well as api keys. Instuctions to
acquire these are provided in the app:

.. code:: bash

    mimir sync -- syncs your notes file with the Evernote folder specified in your config file (MimirNotes by default)
    mimir generate_evernote_token -- Walks you through creating an access token for syncing

Finally, you can also view the status of your mimir, view a count of all
tags present, or delete it entirely:

.. code:: bash

    mimir status
    mimir tags
    mimir delete