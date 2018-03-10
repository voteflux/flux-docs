Frequently Asked Questions
==========================

How do I add a document to FluxDoc?
   #. Try to convert your document into plain text. Where formatting is essential, use sphinx.
   #. For images or video, you can add the files and link them in the plain text.
   #. If you have any problems or difficulty `add an issue <https://github.com/pwhipp/fluxdoc/issues>`_ describing your problem.

   .. warning::

      Avoid the temptation to link word documents, pdfs or spreadsheets if at all possible. Word documents and pdfs can be converted to plain text which makes them searchable and allows their automatic publication in a variety of formats (including html, epub, latex etc.).

      Spreadsheets may be included as CSVs

How do I change a document or the structure of the documents?
   This documentation is a collection of `restructured text files`_ organized and presented using `Sphinx`_.

   Simple corrections and modifications may be made by selecting "Edit on GitHub", substantial changes can be cumbersome. To work with the documentation, you ideally need a local installation and familiarity with:

      - `Git`_
      - `restructured text files`_
      - `Sphinx`_

How do I publish a document change to the website?
   You don't have to. Commits to the master branch on the main repository are automatically published. This process may take a few minutes.

.. _Sphinx: http://sphinx-doc.org/tutorial.html
.. _Git: https://try.github.io/levels/1/challenges/1
.. _restructured text files: http://docutils.sourceforge.net/docs/user/rst/quickstart.html
.. _cheat sheet: http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html