# bibfix

Fixes unescaped acronyms in titles in bibtex files by automatically detecting them and optionally parsing them from a specification file.

## Usage

~~~
usage: bibfix [-h] [-e ENCODING] [-i INCLUDE] INFILE OUTFILE

Fixes unescaped acronyms in titles in bibtex files by automatically detecting
them and optionally parsing them from a specification file.

positional arguments:
  INFILE                The bibtex file to process
  OUTFILE               The bibtex file to write to or - for stdout.

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODING, --encoding ENCODING
                        Encoding to use for parsing and writing the bib files
  -i INCLUDE, --include INCLUDE
                        A file with strings to additionally escape. Each line
                        marks a single string to protect with curly braces
~~~

## License

This library is [free software](https://en.wikipedia.org/wiki/Free_software); you can redistribute it and/or modify it under the terms of the [GNU Lesser General Public License](https://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License) as published by the [Free Software Foundation](https://en.wikipedia.org/wiki/Free_Software_Foundation); either version 3 of the License, or any later version. This work is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU Lesser General Public License](https://www.gnu.org/copyleft/lgpl.html) for more details.
