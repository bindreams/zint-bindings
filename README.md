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

```python
>>> from zint import Symbol, Symbology
>>> x = Symbol()
>>> x.symbology = Symbology.QRCODE
>>> x.encode("https://github.com/bindreams/zint-bindings")
>>> x.outfile = "qrcode.png"
>>> x.print()  # All done!

```

Install the package with:
```sh
pip install zint-bindings
```
Detailed instructions and usage examples are available in the [official documentation](https://zint-bindings.readthedocs.io/en/stable/getting-started.html).

## License
<img align="right" width="150px" height="150px" src="https://www.apache.org/foundation/press/kit/img/the-apache-way-badge/Indigo-THE_APACHE_WAY_BADGE-rgb.svg">

Copyright 2024-2025, Anna Zhukova

This project is licensed under the Apache 2.0 license. The license text can be found at [LICENSE.md](/LICENSE.md).

These bindings are based on the API portion of the Zint project, which is licensed under the BSD 3-clause license. See more information at [src/zint/external/zint/LICENSE](/src/zint/external/zint/LICENSE).
