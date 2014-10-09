.. _documenting:

===========
Documenting
===========

This page will give you a brief introduction in writing and extending the documentation with `Sphinx <http://sphinx-doc.org/index.html>`_.
Sphinx automatically creates the documentation for our source code but can be manually extended via `reStructuredText <http://docutils.sourceforge.net/rst.html>`_. The sphinx website features a nice `introduction <http://sphinx-doc.org/index.html>`_ that explains some of the basics. It is advised to read the official documentation and use this guide as a short reference.

Project Structure
-----------------

The sphinx project is located in the ``/docs`` folder of our project. In there are several important components:

  ``conf.py``
    Contains the configuration of our documentation. You should change the versions variables in there for every release!
  ``index.rst``
    This is the root document. It is the top-level document and the first page of our documentation.
  ``make.bat``
    The Makefile for windows users. Use it to build the documentation
  ``_static``
    Contains static files such as style sheets and script files.
  ``_templates``
    Contains templates that can be rendered out to e.g. html-pages
  ``userdoc``
    The usermanual for non-developer. Explains how to use the pipeline in production. This folder contains the rst-files
  ``devdoc``
    A manual for developers. Information for developing and source code documentation. This folder contains the rst-files
  ``_build``
    Contains the built documentation. So here are the rendered html-pages. This should not be version controlled.
    So you should rebuild your documentation at appropriate times.

Building the documentation
--------------------------

This requires you to install the sphinx package. Just run setuptools::

  easy_install -U Sphinx

After the succesful installation you are able to run the ``make.bat`` on windows. Run it with html as argument to render the html-pages in ``_build``::

  make.bat html

The autodoc module will import all modules it documents. Side-effects will be imported as well! Everytime you change the sourcecode, you should run the command again to update the documentation. This is especially important after releases.
Check the :ref:`Advanced Building <advanced_building>` section for apidoc autogeneration and helpful tools. In production you should always follow the advanced building guide.

.. _advanced_building:

Advanced Building
-----------------

The section on toc-trees shows you how to include several rst-files into your doc.
When you write a huge api, you have to create a rst-file for at least each package and let autodoc do the rest of the work.
This can get tedious and developers tend to forget to include their modules and packages.
To work around this problem, sphinx includes a `apidoc <http://sphinx-doc.org/man/sphinx-apidoc.html>`_ script, that generates rst files with autodoc directives automatically by scanning your sourcecode.
This is incredible helpful but also limited. Because there was no way to change the formating, we use a modified version of the script. The script can be found under ``docs/gendoc.py`` and provides the exact same usage.
You should run the script like this::

  python gendoc.py -Tfe -o devdoc/source/ ../jukebox/

For your convenience, there is also a pythonscript that runs gendoc and invokes the make.bat. Just call or doubleclick the script and the doc is updated::

  user@mypc /path/to/Jukebox/docs
  $ updatedoc.py

**Running ``updatedoc.py`` is the usual way of building the doc!**

Gendoc lets you reference your modules in an rst files like in this example::

  :ref:`jukebox.launcher.baselauncher`

But you can also use ``:mod:`` instead of ``:ref:``

The labels for the reference are automatically created by gendoc.

.. Warning:: Using the ``updatedoc.py`` script does delete the content of the apidoc folder. You might loose data! Because we use updatedoc frequently, there is no point in altering files inside the apidoc folder.


Writing reStructuredText
------------------------

To be able to write reStructuredText (short: rst) will be essential for every developer. All articles in the documentation are written in rst. This also includes everything created by the autodoc. So even if you are not writing a section manually, as soon as you contribute source code you should have written some rst already. Every docstring in your python modules (the stuff in triple-quotes) will be collected by the autodoc extension and inserted in our source documentation. These docstrings should therefore be written in rst. You can find information on how to write docstrings :ref:`here <docstrings>`.

Here is a short reference to rst. A more extensive guide can be found `here <http://sphinx-doc.org/rest.html>`_ or `here with html-comparisons <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_. You can also use the ``Show Source``-Button in the sidebar, if you ever wonder how the current page is written in rst.

TOC-Trees
+++++++++

The toctree directive inserts table of contents at the current location. In the body of the toctree you can specify names of rst documents (relative or absolute). The toctree will also include all toctrees of these documents until a certain maxdepth is reached (you can ommit the maxdepth option to have unlimited depth). The root document (``index.rst`` in the ``doc/`` directory) contains the first toctree. All documents have to be in either that toctree or in toctrees of included documents. If they are not included, sphinx will warn you at build-time and you will not find the document rendered.
Here is a basic example of a toctree::

  .. toctree::
     :maxdepth: 2
     :numbered:

     intro
     userdoc
     This is the devdoc! <devdoc>

This could be the top-level toctree. After the ``.. toctree::`` directive you can specify a few options. ``:maxdepth:`` will include subtrees only to a certain depth. ``:numbered:`` will make the table numbered.

Sections
++++++++

Longer texts can be broken up into sections with **headings**. A section will automatically appear in the appropriate toctree. To write a section heading you have to underline (optional overline too) it with non-alphanumeric characters: ``= - ` : ' " ~ ^ _ * + # < >``
It does not matter what character you take. Sphinx will automatically figure out what level of section it is. That way you can define subsections if you choose a different character than before. In our documentation we use **=** for top-level headings, **-** for 2. level and **+** or something else for 3. level.
The underline should always have at least as many characters as the above headline. After the underline follows an empty line and then the section content.
You have to insert an empty line before a new section two.

Source Code
+++++++++++

To display sourcecode end you current paragraph with a double colon. Then write a new indented paragraph with the source code. So now follows a litte bit of rst source code that will not be rendered and displayed in monospaced font::

  Check out my awesome sourcecode::

    print "Hello world!"
    if bar():
        foo('python is awesome')

Links
++++++++++

Sphinx allows for quite a few ways to deploy links in your documentation. One way to link between different locations in the documentation (also across files) is to write::

  :ref:`somdetext <label-name>`

  .. _label-name:

  text paragraph or section after a label. this will be shown if you click on the 'sometext'-link in the documentation

Python objects like modules can be referenced as well. To reference to :mod:`jukeboxcore.constants` use::

  :mod:`jukeboxcore.constants`

Hyperlinks to websites like this `one <https://www.python.org/>`_ work like this::

  `one <https://www.python.org/>`_

Viewdoc is an extension for sphinx that allows a link to a python object in the source code::

  this will link to a python function in my source :func:`jukeboxcore.main.init`
  this will link to a module :mod:`jukeboxcore.main`
  this will link to a variable :data:`jukeboxcore.constants.DEFAULT_LOGGING_LEVEL`
  this will link to a class :class:`jukeboxcore.plugins.JB_Plugin`

.. _docstrings:

Docstrings
----------

Docstrings are **very important**! All of our source code should have docstrings. This applies for packages, modules, classes, functions, methods, public and private members etc. Docstrings are written in triple quotes in the source code and describe the object above.
The most common docstring you will write is for a function or method. Here is a template::

  def foo(self, arg1, arg2, kwarg1=None, kwarg2=False):
      """ Do foo and return the bar

      A much more detailed description on how this function works and what it does.
      Give examples on how to use it and explain your code a little too.

      :param arg1: just a random parameter description
      :type arg1: object
      :param arg2: another description for the second argument
      :type arg2: int
      :param kwarg1: Optional - specify a keyword argumnt for fun
      :type kwarg1: str|unicode
      :param kwarg2: Optional - If True, some stuff happens in the function, default is False
      :type kwarg2: bool
      :returns: the bar of foo
      :rtype: Bar
      :raises: ValueError, IndexError, MyOwnLittleError
      """
      pass

This structure can be adapted for the rest of python objects. Always start with a very short one-line description, an emptyline and then a detailed description. To make the creation of parameter docstrings faster there are also yasnippets for emacs, which create them automatically.
For more information have a look at these `examples <https://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example>`_ and the official syntax `markup documentation <http://sphinx-doc.org/markup/desc.html>`_.
