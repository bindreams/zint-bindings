:::{toctree}
:hidden:
getting-started.md
Advanced Installation <installation.md>
API Reference <api.md>
License <license.md>
Github Repository <https://github.com/bindreams/zint-bindings>
:::

# Zint Bindings
This project provides Python bindings for [Zint](https://www.zint.org.uk/): a cross-platform open source barcode generating solution.

Features:
- 50+ barcode types;
- Text or binary data encoding;
- Export image to:
	- PNG;
	- BMP;
	- GIF;
	- PCX;
	- TIF;
	- EMF;
	- EPS;
	- SVG;
- Configurable options:
	- Size;
	- Color;
	- Error correction;
	- Rotation;
	- ...and much more depending on the barcode type.

Installation instructions and usage examples are available in [Getting Started](getting-started.md).

## About this project
This project is intended to be a faithful reproduction of the Zint API in Python. As such, it provides functionality not found in any other python package, but at the same time it's not particularly user-friendly. I hope that these bindings can function as a low-level foundation for a more pythonic library for symbol generation.

At the same time, if you experience crashes, exceptions, or other particularly egregious behavior, or if you have an idea for a quality of life improvement that would be easy to implement in the current code framework, feel free to open up an issue.

## License
<img align="right" width="150px" height="150px" src="https://www.apache.org/foundation/press/kit/img/the-apache-way-badge/Indigo-THE_APACHE_WAY_BADGE-rgb.svg">

Copyright 2024, Anna Zhukova

This project is licensed under the Apache 2.0 license ([full text](license.md)).

These bindings are based on the API portion of the Zint project, which is licensed under the BSD 3-clause license. See more information in the [Zint manual](https://www.zint.org.uk/manual/chapter/7).
