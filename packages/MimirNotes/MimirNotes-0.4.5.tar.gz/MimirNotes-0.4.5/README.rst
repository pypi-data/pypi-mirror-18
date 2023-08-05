Mimir
=====

Mimir is a simple, small, command line note taking utility. Its intended function is to allow you to take a quick note
whenever you need to, and then get out of the way. Mimir can be used anywhere, as it allows you to create a mimir in any
directory (which allows for multiple mimirs in use at any given time). It can also be configured with a global instance.

Usage
-----

Mimir has a simple subset of commands for usage.

To initialize mimir in a directory::

    mimir init

This will create a .mimir directory, with a config file, as well as a notes file.

To begin taking notes in a directory containing a mimir::

    mimir This is a test note.

You can also create notes using an editor by simply typing::

    mimir

To view your mimir notes::

    mimir -s 2

Where s is the number of notes you wish to view.

To view your notes by tag::

    mimir @tag1 @tag2

If only tags are provided, mimir assumes you want to search by those tags.

Notes can also be searched via date fences::

    mimir --since 2010 --until october
    mimir --since june
    mimir --until 2015

Date fences can be mixed with tags and the -s option for more fine grained searching.

You can also edit your notes::

    mimir edit

(To edit notes, you will need to set the `editor` config variable in .mimir/.mimir_config, mimir will warn you if this is
not set)

Finally, you can also view the status of your mimir, view a count of all tags present, or delete it entirely::

    mimir status
    mimir tags
    mimir delete
