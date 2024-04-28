# Getting Started
## Installation
Zint bindings are available to install from pip:
```sh
pip install zint-bindings
```

the `zint` package contains both the compiled bindings, as well as a `pyi` syntax file which should help you in your IDE.

## Basic usage
### Print a QR Code to file
After installation, create a `Symbol` (aka a barcode, qrcode, etc.) and set the necessary parameters to then produce an image on disk:
```python
from zint import Symbol, Symbology

x = Symbol()
x.symbology = Symbology.QRCODE
x.encode("https://github.com/bindreams/zint-bindings")
x.outfile = "qrcode.png"
x.print()  # Will create qrcode.png
```

As you can see, in the Zint philosophy, most arguments both for symbol generation and output, are set as fields in the `Symbol` class.

### Create an in-memory image
Alternatively, you can produce a bitmap buffer in memory, and then load it, for example into a [`PIL.Image`](https://pillow.readthedocs.io/en/stable/reference/Image.html):
```python
...
x.encode("https://github.com/bindreams/zint-bindings")
x.buffer()

# At this point, x.bitmap stores the RGB bitmap image of the QR code
# This memoryview has a similar syntax to a numpy array.
shape = x.bitmap.shape
print(shape)  # -> (width, height, 3)

from PIL import Image
image = Image.frombytes("RGB", (shape[0], shape[1]), x.bitmap, "raw")
image.show()
```

### Color and transparency
You can specify any color for background and foreground using the `Symbol.bgcolor` and `Symbol.fgcolor` properties. When transparency is involved, `Symbol.alphamap` holds the additional alpha channel. Here's how add it to your `PIL.Image`:

```python
...
x.bgcolor = "00000000"  # RGBA Transparent background
x.fgcolor = "FFFF00"    # RGB Yellow foreground

x.encode("https://github.com/bindreams/zint-bindings")
x.buffer()

shape = x.bitmap.shape
print(shape)  # -> (width, height, 3)
alpha_shape = x.alphamap.shape
print(alpha_shape)  # -> (width, height)

from PIL import Image
image = Image.frombytes("RGB", (shape[0], shape[1]), x.bitmap, "raw")
alpha_channel = Image.frombytes("L", (shape[0], shape[1]), x.alphamap, "raw")

image.putalpha(alpha_channel)  # Combine the image and the alpha channel
image.show()
```

### Symbol-specific configuration
Most of the symbols support configuration through the self-explanatory `option_1`, `option_2`, and `option_3` properties. These options do something different for every symbol type. For a particular symbol type (symbology) there is extensive documentation in the original [Zint manual](https://www.zint.org.uk/manual/chapter/6/1). For example, according to the [Datamatrix docs](https://www.zint.org.uk/manual/chapter/6/6), `option_2` can be used to set the desired size of the resulting datamatrix, independent of the size of the input:
:::{note}
The bitmap size is `96 * 2 = 192` because the default `Symbol.scale` of 1 produces dots of 2x2 pixels. You can set `Symbol.scale` to 0.5 to produce pixel-perfect minimal datamatrices.
:::
```python
from zint import Symbol, Symbology

x = Symbol()
x.symbology = Symbology.DATAMATRIX

x.option_2 = 20  # Let's create an enormous 96x96 datamatrix

x.encode("https://github.com/bindreams/zint-bindings")

x.buffer()
print(x.bitmap.shape)  # -> (192, 192, 3)
```

## More information
Most of the configuration possibilites are not covered in this guide. But since Zint Bindings mirrors the original Zint API almost perfectly, you can consult the Zint manual ([general API](https://www.zint.org.uk/manual/chapter/5), [specific symbols](https://www.zint.org.uk/manual/chapter/6/1)).

If there is something mentinoned in the manual, but it's not obvious how to translate that into Python, please feel free to open up an issue.
