Save
====

A very simple module to *safely* save data to files in python.

When you choose a path and a name for the file you want to save your
data to, the script checks **if the given file at the given path already
exist**; if so, **it adds an increasing numbering at the end of the file
name** (just before the file extension if there is any) untill it finds
a path+name not taken already.

This prevents from losing data by inadvertently re-writing a file.

Install
-------

``$ pip install save``

Basic usage
-----------

::

    from save import save

    data = 'Hey there'
    save(data, 'my_file.txt')

The safe\_path function
-----------------------

You can import the ``safe_path`` submodule to use with other libraries
or functions. It provides the same functionality as ``save()``.
(Basically the ``save()`` function itself calls ``safe_path()`` to do
the work)

This is an example involving matplotlib:

::

    from matplotlib import pyplot as plt
    from save import safe_path

    plt.plot(range(10))
    plt.savefig(safe_path('my_figure.png'))