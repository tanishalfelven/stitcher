# stitcher #
A Templating-Engine

__stitcher__ is a program that allows the user to define `.TEMPLATE`'s, and apply these
templates to files with __template directives__. A __template directive__ is the name of a template file
with double '`{`'s.

For example, you have a template `header.TEMPLATE`, and you want to apply it to a file. In the file,
you would add a ``{{HEADER}}`` call, that point in code would be replaced by all of the text inside of
the `header.TEMPLATE`.

###Command Line Options###
```
-t  --templatedir   Path to template directory (Is current directory if directory is not supplied)
-s  --srcdir        Path to source directory (Is '../src' if not supplied
-r  --resourcefile  Path to resource file. Resource file will be copied to all destination folders.
-o  --outdir        Path to output directory (Is '../dist' if not supplied
-v  --verbose       Have verbose output.
-b  --basedir       Set BASDIR inside of .TEMPLATE files (Normally dynamically set to 'outdir')
-f  --filetype      Set filetype for files to check for template calls (Is '.html' normally)
-h  --help          Print help
```

Stitcher can be run with:
```
python stitcher.py
```
Make sure that you have Python 3+ installed.

Basic Example build:
```
python stitcher.py -t "dist-templates" -o "dist" -s "src"
Template    Dir: "/dist-templates"
Output      Dir: "/dist"
Source      Dir: "/src"
```

Please fork and make changes!
