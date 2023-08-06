rst2ipynb
=========

This project converts standalone
`reStructuredText <http://docutils.sourceforge.net/rst.html>`_ files
to `Jupyter notebooks <http://jupyter.org/>`_ file.

This is currently achieved by converting to markdown with
`pandoc <http://pandoc.org>`_ and then to a Jupyter notebook using
`notedown <https://github.com/aaren/notedown/>`_, plus some
configuration and tweaks.

Requirements
------------

Python 3 (for proper UTF-8 support in notedown), pandoc, notedown

## Installation

Install `pandoc <http://pandoc.org>`_ and then this module as usual:

    git clone https://github.com/nthiery/rst-to-ipynb.git
    cd rst-to-ipynb
    pip3 install .

pip3 will install the other dependencies as needed.

Caveat: the notedown package on pipy (1.5.0, 2015-10-07) is somewhat
outdated; for better conversion, , it's recommended to install the
latest version from the github repo.

Usage
-----

To convert a reST file ``xxx.rst`` to a Jupyter notebook ``xxx.ipynb``, run:

    rst2ipynb xxx.rst -o xxx.ipynb

Example
-------

- reST document: `all.rst <tests/all.rst>`_
- Produced Jupyter notebook: `all.ipynb <http://nbviewer.ipython.org/github/nthiery/rst-to-ipynb/blob/master/tests/all.ipynb>`_

TODO
----

- [X] Handle Sage's doctests
- [X] Fenced code blocks: fix incompatibility between pandoc output and notedown input.
      Fixed in notedown; see: https://github.com/aaren/notedown/issues/29.
- [ ] Configurability of the default ReST role, in particular to handle maths in Sage's ReST dialect.
      Current status: hardcoded for Sage.
- [ ] Configurability of custom ReST roles, in particular to handle Sage's custom roles
- [ ] Proper argument parsing; escape characters, spaces, ... are not
      yet supported
- [ ] Handle input/output blocks within itemize and other indented constructions
      See https://github.com/aaren/notedown/issues/33


