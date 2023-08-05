Documentation: http://pybinding.site/

v0.8.1 | 2016-11-11

* Structure plotting functions have been improved with better automatic scaling of lattice site
  circle sizes and hopping line widths.

* Fixed Brillouin zone calculation for cases where the angle between lattice vectors is obtuse
  ([#1](https://github.com/dean0x7d/pybinding/issues/1)). Thanks to
  [@obgeneralao (Oliver B Generalao)](https://github.com/obgeneralao) for reporting the issue.

* Fixed a flaw in the example of a phosphorene lattice (there were extraneous t5 hoppings).
  Thanks to Longlong Li for pointing this out.

* Fixed missing CUDA source files in PyPI sdist package.

* Revised advanced installation instructions: compiling from source code and development.



