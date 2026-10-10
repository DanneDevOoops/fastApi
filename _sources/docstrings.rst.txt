write docstrings
=================

This document provides simple guidelines for writing docstrings in a Python
codebase. The intention is to ensure that the codebase have clear and concise
developer documentation to enable knowledge sharing of how it currently
works and what we can do while working further with it. There for it is also
important to maintain consistency with quality of all documentation,
docstrings and comments across the entire codebase. Remember this is not
meant to add uppon the work of the developer, but to ease the work of
documenting and sharing knowledge with others and to do so with as minimal
effort as possible.

To enable yourself to write good docstrings, you should be familiar with the
Python docstring conventions, which are described in the

Autodoc extension
------------------

To mark a member as **private**, include ``:meta private:`` in its
docstring Info field:

.. code-block:: python

    def my_function(my_arg, my_other_arg):
        """blah blah blah

        :meta private:
        """

To mark a member as **public**, include ``:meta public:`` in its docstring
Info field, even if its name starts with an underscore:

.. code-block:: python

    def _my_function(my_arg, my_other_arg):
        """blah blah blah

        :meta public:
        """


Extlinks extension
-------------------

The sphinx.ext.extlinks extension helps you create short aliases for
frequently used external websites, making your documentation cleaner and
easier to maintain.

1. Configure Aliases in `conf.py`:

First, you need to define your link aliases in the conf.py file. This is
done by adding or modifying the extlinks dictionary. Each entry in the
dictionary maps an alias name to a tuple containing the base URL (with %s
as a placeholder for the specific part of the link) and a caption string
(also using %s).


.. code-block:: python
    :caption: Example in conf.py

    extlinks = {
        'issue': ('https://github.com/your-repo/issues/%s', 'Issue #%s'),
        'user': ('https://github.com/%s', 'GitHub User %s')
    }

In this example:

'issue' is an alias for linking to GitHub issues.
'user' is an alias for linking to GitHub user profiles.

2. Use Aliases in your Docstrings (.rst files):

Once configured, you can use these aliases as roles in your .rst files.

.. code-block:: rst
    :caption: Example usage in an .rst file

    For more details, see :issue:123.
    This feature was contributed by :user:DMoest.

This will render as:

A link to https://github.com/your-repo/issues/123 with the text "Issue #123".
A link to https://github.com/DMoest with the text "GitHub User DMoest".
Custom Link Text:

You can also provide custom link text:

.. code-block:: rst

    See :issue:this important bug report <456>.

This will link to https://github.com/your-repo/issues/456 but display the
text "this important bug report".

Detecting Hardcoded Links:

Sphinx can also help you find places where you've used a full URL instead
of an alias. Enable this by setting extlinks_detect_hardcoded_links = True
in your conf.py.

.. code-block:: python
    :caption: Example in conf.py

    extlinks_detect_hardcoded_links = True

This will generate warnings during the documentation build if it finds
hardcoded links that could be replaced by one of your defined extlinks
aliases.



Graphviz extension
-------------------

The sphinx.ext.graphviz extension allows you to embed Graphviz diagrams
directly into your documentation.

To include a Graphviz diagram, use the graphviz directive. You can either
write the Graphviz code (using the dot language) directly within the
directive or link to an external .dot file.

Embedding Graphviz code directly:

.. code-block:: rst

    .. graphviz::

      digraph my_diagram {
         "Step 1" -> "Step 2";
         "Step 2" -> "Step 3";
      }


Linking to an external .dot file:

If you have a diagram defined in a separate file (e.g., my_diagram.dot),
you can include it like this:

.. code-block:: rst

    .. graphviz:: my_diagram.dot

    Common Options:

    You can customize the appearance and behavior of the graph using options:
    :alt: text: Provides alternative text for the graph (e.g., for screen readers).
    :align: left|center|right: Sets the horizontal alignment of the graph.
    :caption: text: Adds a caption below the graph.
    :layout: layout_engine: Specifies the Graphviz layout engine (e.g., dot,
    neato, fdp). Defaults to dot.

Example with options:

.. code-block:: rst

    .. graphviz:: :align: center :caption: A simple process flow.


  digraph process_flow {
     A -> B -> C;
  }

The graph directive is a shorthand for creating simple, undirected graphs:

.. code-block:: rst

    .. graph:: my_simple_graph :caption: A basic undirected graph.


  node1 -- node2;
  node2 -- node3;

This is equivalent to:

.. code-block:: rst

    .. graphviz:: :caption: A basic undirected graph.
      graph my_simple_graph {
         node1 -- node2;
         node2 -- node3;
      }


Inheritance Diagrams extension
-------------------------------

The sphinx.ext.inheritance_diagram extension allows you to automatically
generate and embed inheritance diagrams (class hierarchies) in your
documentation. These diagrams are rendered using Graphviz.

Basic Usage:

To include an inheritance diagram, use the inheritance-diagram directive
followed by one or more class or module names.

.. code-block:: rst

    .. inheritance-diagram:: my_module.MyClass another_module.AnotherClass my_module

    .. inheritance-diagram:: MyClassInCurrentModule

    If a class name is unqualified (e.g., MyClassInCurrentModule), it's
    assumed to be in the module currently being documented.

    Common Options:


    :parts: integer: Controls how much of the fully qualified class name is
    displayed.
    A positive integer (e.g., :parts: 1) shows that many parts from the
    right (e.g., only the class name).
    A negative integer (e.g., :parts: -1) removes that many parts from the
    left (e.g., if all classes start with my_project.lib., :parts: -2 would
    remove my_project.lib.).
    :private-bases:: If present, includes base classes whose names start
    with an underscore (e.g., _MyPrivateBaseClass).
    :caption: text: Adds a caption below the diagram.
    :top-classes: classA, classB.SubClass: Specifies a comma-separated list
    of class names. The diagram will not show ancestors above these
    specified classes.
    :include-subclasses:: If present, any subclasses of the specified
    classes will also be included in the diagram.

Examples:

1. Diagram for a specific class, showing only class names:

.. code-block:: rst

    .. inheritance-diagram:: my_module.MyClass
    :parts: 1 :caption: Inheritance for MyClass

2. Diagram for all classes in a module, stopping at specific base classes:

.. code-block:: rst

    .. inheritance-diagram:: my_module
    :top-classes: my_module.BaseClassA, another_module.BaseClassB
    :caption: Module hierarchy up to BaseClassA and BaseClassB

3. Diagram for a class and all its subclasses:

.. code-block:: rst

    .. inheritance-diagram:: my_module.ParentClass
    :include-subclasses:
    :caption: ParentClass and all its descendants
