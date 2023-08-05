json2cmake
==========

``json2cmake`` converts `JSON compilation
database <http://clang.llvm.org/docs/JSONCompilationDatabase.html>`__
files into `CMake <https://cmake.org/>`__ files. The resulting
``CMakeLists.txt`` file can then be used to recompile the same object
files with less overhead via `Ninja <https://ninja-build.org/>`__, used
as an IDE project file for `CLion <https://www.jetbrains.com/clion/>`__,
or for integration into a larger CMake project.

The output files only include `object
library <https://cmake.org/Wiki/CMake/Tutorials/Object_Library>`__
definitions, as a ``compile_commands.json`` file typically doesn't
contain any linker commands.


