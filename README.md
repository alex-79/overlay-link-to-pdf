# INSTALL

## Debian/Ubuntu

```bash
apt-get install python3-reportlab python3-pip python3-progressbar fonts-dejavu
pip3 install pypdf2 --system
pip3 install python-magic --system
```

# USAGE

## For single PDF

```bash
./overlaylink2pdf.py -w 'My watermark' -l https://my.domain.local -s 9 -p top-middle -i ./documents -o ./result --prefix my.domain.local- --validate trustworthy
```

* -i/--input - input file, required
* -o/--output - output file
* -w/--watermark - watermark, required
* -l/--link - link, required
* -s/--font-size - fontsize, default = '0'
* -f/--font - font, default = 'DejaVuSans'
* -c/--color - color, default = '0645AD'
* -p/--position - position watermark, ["top-left", "top-middle", "top-right", "bottom-left", "bottom-middle", "bottom-right"], default = 'top-left'
* --prefix - prefix output file, default = ''
* --validate - validate output file as PDF, ['lazy', 'trustworthy'], default = 'lazy'

## For folder with PDF

```bash
./batch_overlaylink2pdf.py -w 'My watermark' -l https://my.domain.local -s 14 -p bottom-right -i ./documents -o ./result -r --prefix my.domain.local- --validate trustworthy
```

* -i/--input - input folder, default = '.'
* -o/--output - output folder, default = '.'
* -w/--watermark - watermark, required
* -l/--link - link, required
* -s/--font-size - fontsize, default = '0'
* -f/--font - font, default = 'DejaVuSans'
* -c/--color - color, default = '0645AD'
* -p/--position - position watermark, ["top-left", "top-middle", "top-right", "bottom-left", "bottom-middle", "bottom-right"], default = 'top-left'
* -r/--recursive - recursive, default = 'false'
* --prefix - prefix output file, default = ''
* --validate - validate output file as PDF, ['lazy', 'trustworthy'], default = 'lazy'

# NOTE

Script is based on https://forum.ubuntu.ru/index.php?topic=275095.msg2173044#msg2173044