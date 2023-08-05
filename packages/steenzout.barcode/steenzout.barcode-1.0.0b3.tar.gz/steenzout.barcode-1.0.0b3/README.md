# steenzout.barcode

[![pypi](https://img.shields.io/pypi/v/steenzout.barcode.svg)](https://pypi.python.org/pypi/steenzout.barcode/)
[![Build Status](https://travis-ci.org/steenzout/python-barcode.svg?branch=master)](https://travis-ci.org/steenzout/python-barcode)
[![Code Health](https://landscape.io/github/steenzout/python-barcode/master/landscape.svg?style=flat)](https://landscape.io/github/steenzout/python-barcode/master)
[![Coverage Status](https://coveralls.io/repos/github/steenzout/python-barcode/badge.svg?branch=master)](https://coveralls.io/r/steenzout/python-barcode)
[![Requirements Status](https://requires.io/github/steenzout/python-barcode/requirements.svg?branch=master)](https://requires.io/github/steenzout/python-barcode/requirements/?branch=master)
[![Documentation Status](https://readthedocs.org/projects/python-steenzout-barcode/badge/?version=latest)](http://python-steenzout-barcode.readthedocs.io/en/latest/?badge=latest)

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)][license]
[![Project Stats](https://www.openhub.net/p/python-steenzout-barcode/widgets/project_thin_badge.gif)](https://www.openhub.net/p/python-steenzout-barcode/)

This repository is a fork of:
- [viivakoodi][viivakoodi]
- [pyBarcode][pyBarcode]

This library provides the ability to create bar codes.

The bar codes are created as SVG objects.


## Installation

```
$ pip install steenzout.barcode
```


## Bar codes

- EAN-8
- EAN-13
- UPC-A
- JAN
- ISBN-10
- ISBN-13
- ISSN
- Code 39
- Code 128
- PZN


## Usage

```
>>> from steenzout import barcode
>>> barcode.PROVIDED_BARCODES
[u'code39', u'code128', u'ean', u'ean13', u'ean8', u'gs1', u'gtin',
 u'isbn', u'isbn10', u'isbn13', u'issn', u'jan', u'pzn', u'upc', u'upca']
>>> EAN = barcode.get_barcode_class('ean13')
>>> EAN
<class 'barcode.ean.EuropeanArticleNumber13'>
>>> ean = EAN(u'5901234123457')
>>> ean
<barcode.ean.EuropeanArticleNumber13 object at 0x00BE98F0>
>>> fullname = ean.save('ean13_barcode')
>>> fullname
u'ean13_barcode.svg'
# Example with PNG
>>> from barcode.writer import ImageWriter
>>> ean = EAN(u'5901234123457', writer=ImageWriter())
>>> fullname = ean.save('ean13_barcode')
u'ean13_barcode.png'
# New in v0.4.2
>>> from StringIO import StringIO
>>> fp = StringIO()
>>> ean.write(fp)
# or
>>> f = open('/my/new/file', 'wb')
>>> ean.write(f) # PIL (ImageWriter) produces RAW format here
# New in v0.5.0
>>> from barcode import generate
>>> name = generate('EAN13', u'5901234123457', output='barcode_svg')
>>> name
u'barcode_svg.svg'
# with file like object
>>> fp = StringIO()
>>> generate('EAN13', u'5901234123457', writer=ImageWriter(), output=fp)
>>>
```

Now open ean13_barcode
[svg|png] in a graphic app or simply in your browser and
see the created barcode. That's it.


## Commandline

```
$ pybarcode{2,3} create "My Text" outfile
New barcode saved as outfile.svg.

$ pybarcode{2,3} create -t png "My Text" outfile
New barcode saved as outfile.png.

Try `pybarcode -h` for help.
```


## Links

- [Code 39](https://en.wikipedia.org/wiki/Code_39)
- [Code 128](https://en.wikipedia.org/wiki/Code_128)
- [EAN](https://en.wikipedia.org/wiki/International_Article_Number_(EAN))
- [ISBN](https://en.wikipedia.org/wiki/International_Standard_Book_Number)
- [ISSN](https://en.wikipedia.org/wiki/International_Standard_Serial_Number)
- [JAN](https://en.wikipedia.org/wiki/International_Article_Number_(EAN)#Japanese_Article_Number)
- [UPC](https://en.wikipedia.org/wiki/Universal_Product_Code)


[license]:  https://raw.githubusercontent.com/steenzout/python-barcode/steenzout/LICENSE    "MIT license"
[pyBarcode]:    https://bitbucket.org/whitie/python-barcode "barcode"
[viivakoodi]:   https://github.com/kxepal/viivakoodi    "viivakoodi"
