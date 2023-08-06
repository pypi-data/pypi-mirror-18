PathinBy
========
What is PathinBy
----------------

PathinBy is a tiny tool (used as a command line app or a Python module),
that converts your directory structure into a nice formatted tree to use in your blog posts or other illustrations.

*You need Python 2.7+ or Python 3.x to run this module*

How to use
^^^^^^^^^^
Imagine you have a directory structure like this:

.. image:: http://i.imgur.com/BlW8YHn.png
   :height: 263 px
   :width: 614 px

**As a Python module**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

  >>> import pathinby
  >>> tree = pathinby.create_path('Cats')
  >>> print ('\n'.join(tree))


Here we've passed the directory name as an argument, there are also other arguments you can use to customize the behavior of the module, you can change those "|" and "-\|" and specify an output file. Check function documentation in the source code for more details of the usage.

*create_path()* returns an array to give more freedom of use in different situations.

This gives the output:

.. code::

  |-Big
  | |-Simba.bcat
  |-Sylvester.cat
  |-Tom.cat

|

**As a commend line tool**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code::

  $ pathinby -s Cats

This will traverse the "Cats" directory and print the contents tree to the terminal window, so running this command prints out the same directory tree like above.

the directory name can be a full or a relative path, like we did here.

By default, pathinby will do its work on the current directory if no directory is specified, in this case we specified "Cats".

The *s* option means "*show*", prints the output to the terminal.

Other option is

  -o {path to file} -> writes the output to the specified file

Use **pathinby -h** anytime for help on using the command.
