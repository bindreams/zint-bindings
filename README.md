# Zint Bindings
This project provides Python bindings for [Zint](https://www.zint.org.uk/): a cross-platform open source barcode generating solution.

This package is currently able to encode data in over 50 barcode symbologies (types of barcode), for each of which it is possible to translate that data from either UTF-8 (Unicode) or a raw 8-bit data stream. The image can be rendered as either a Portable Network Graphic (PNG) image, Windows Bitmap (BMP), Graphics Interchange Format (GIF), ZSoft Paintbrush image (PCX), Tagged Image File Format (TIF), Enhanced Metafile Format (EMF), as Encapsulated PostScript (EPS), or as a Scalable Vector Graphic (SVG). Many options are available for setting the characteristics of the output image including the size and colour of the image, the amount of error correction used in the symbol and the orientation of the image.

```python
>>> from zint import Symbol, Symbology
>>> x = Symbol()
>>> x.symbology = Symbology.QRCODE
>>> x.encode("https://github.com/bindreams/zint-bindings")
>>> x.outfile = "qrcode.png"
>>> x.print()  # All done!

```

This project does does not provide API documentation, but the interface very closely resembles the original Zint API ([docs](https://zint.org.uk/manual/chapter/5)) and syntax highlighting will take you the rest of the way.

## Install
You can install zint via pip:
```
pip install zint
```

Binary wheels are provided for the most common platforms. If your platform is not supported, pip will build the package from a source distribution.
<details>
  <summary>Building from source</summary>

When building either from this repository, or from a source distribution (sdist) provided by pip, you need the following software apart from Python and pip:
- [Git](https://git-scm.com/)
- any C++ compiler ([MSVC](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022) on Windows) that supports C++17 and a subset of C++20 (concepts)
- [Ninja](https://ninja-build.org/)

On Windows, you will need to run the install command from an "x64 Native Tools Command Prompt" (installed with MSVC) and set the `CMAKE_GENERATOR` environment variable to `Ninja`.
</details>

## License
<img align="right" width="150px" height="150px" src="https://www.apache.org/foundation/press/kit/img/the-apache-way-badge/Indigo-THE_APACHE_WAY_BADGE-rgb.svg">

Copyright 2024, Anna Zhukova

This project is licensed under the Apache 2.0 license. The license text can be found at [LICENSE.md](/LICENSE.md).

These bindings are based on the API portion of the Zint project, which is licensed under the BSD 3-clause license. See more information at [src/zint/external/zint/LICENSE](/src/zint/external/zint/LICENSE).
