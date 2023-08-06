structurediff
=======================
structurediff is a tool (a command line wrapper really) that uses `DeepDiff`_
to provide a simple command line utility for 'diffing' (at a structural rather
than line-based level) large YAML and/or JSON files (meaning it can diff YAML
against YAML, or YAML against JSON, or JSON against JSON).

.. _DeepDiff: https://github.com/seperman/deepdiff

structurediff uses the `pyyaml`_ parser for both JSON
and YAML to work around issues with unicode-ification of strings. As a
result structurediff cannot be depended on to differentiate between unicode
and non-unicode types between JSON and YAML.

.. _pyyaml: http://pyyaml.org/

contributing
------------
Just reach out (or submit a patch or merge request). I try to keep an eye
open.

todo
----
This code has no tests. It should have some.

howto
-----
On the command line::

	usage: structurediff [-h] [-d DIFF_VERBOSITY] [-i INDENT_LEVEL] [-v]
						 input1 input2

	positional arguments:
	  input1                initial input
	  input2                input to compare against input1

	optional arguments:
	  -h, --help            show this help message and exit
	  -d DIFF_VERBOSITY, --diff-verbosity DIFF_VERBOSITY
							set the DeepDiff verbose_level, 0-2 (default 1)
	  -i INDENT_LEVEL, --indent-level INDENT_LEVEL
							set the pprint indent spacing (default 2)
	  -v, --verbose         make output verbose_level

In Python (why would you do this? Use DeepDiff instead!)::

	from structurediff import DataComparison, DataFile
	comparison = DataComparison(DataFile(PATH), DataFile(PATH), VERBOSITY)
	print(comparison)
