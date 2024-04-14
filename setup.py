import os
import shutil
import subprocess as sp
from pathlib import Path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())


class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:
        extension_path = Path.cwd() / self.get_ext_fullpath(ext.name)
        extension_dir = extension_path.parent.resolve()

        env = os.environ.copy()
        env["ZINT_BINDINGS_TARGET_DIR"] = str(extension_dir)

        if Path("build").exists():
            shutil.rmtree("build")
        sp.run(["cmake", "--preset", "windows"], check=True, env=env)
        sp.run(["cmake", "--build", "build"], check=True)


setup(
    name="zint",
    version="0.1.0",
    description="A test project using pybind11 and CMake",
    ext_modules=[CMakeExtension("zint")],
    cmdclass={"build_ext": CMakeBuild},
)
