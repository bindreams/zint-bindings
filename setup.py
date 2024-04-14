import os
import re
import shutil
import subprocess as sp
import sys
from pathlib import Path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())
        # self.extra_objects = ["zlib1.dll", "libpng16.dll"]


class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:
        print(self.get_ext_fullpath(ext.name))

        env = os.environ.copy()
        # env["ZINT_BINDINGS_TARGET_DIRECTORY"] = str(
        #     Path(self.get_ext_fullpath(ext.name)).parent
        # )

        shutil.rmtree("build")
        sp.run(["cmake", "--preset", "windows"], check=True, env=env)
        sp.run(["cmake", "--build", "build"], check=True)


# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup(
    name="zint",
    version="0.1.0",
    description="A test project using pybind11 and CMake",
    ext_modules=[CMakeExtension("zint")],
    cmdclass={"build_ext": CMakeBuild},
)
