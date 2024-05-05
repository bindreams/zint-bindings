# Installation
Zint bindings are available as a package, installable from pip:
```sh
pip install zint-bindings
```

Binary wheels are provided for the most common platforms. If your platform is not supported, pip will build the package from a source distribution.

## Building from source
When building either from this repository, or from a source distribution (sdist) provided by pip, you need the following software apart from Python and pip:
- [Git](https://git-scm.com/)
- any C++ compiler ([MSVC](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022) on Windows) that supports C++17 and a subset of C++20 (concepts)
- [Ninja](https://ninja-build.org/)

::::{note}
On Windows, you will need to run the install command from an "x64 Native Tools Command Prompt" (installed with MSVC) and set the `CMAKE_GENERATOR` environment variable to `Ninja`.

At the moment only the x64 architecture is supported.
::::

After the environment is set up, simply run `pip install`:

::::{tab-set}
:::{tab-item} From pip
Assuming your platform does not have a binary distribution:
```sh
pip install zint-bindings
```
:::
:::{tab-item} From sdist
sdists for particular versions can be downloaded from <https://pypi.org/project/zint/#files>
```sh
pip install zint_bindings-<VERSION>.tar.gz
```
:::
:::{tab-item} From source
You can either clone the project and run the install command from the root directory:
```sh
pip install .
```
or install the project directly from GitHub:
```sh
# A particular tag:
pip install https://github.com/bindreams/zint-bindings/archive/refs/tags/v1.1.0.zip

# From the top of the main branch:
pip install https://github.com/bindreams/zint-bindings/archive/refs/heads/main.zip
```
:::
::::
