from tempfile import mkstemp
from shutil import move, copyfile
from fnmatch import fnmatch
from datetime import date
from ntpath import basename
import os
import sys
import getopt

def replace(file_path, pattern, subst):
	#Create temp file
	fh, abs_path = mkstemp()
	with open(abs_path,'w') as new_file:
		with open(file_path) as old_file:
			for line in old_file:
				new_file.write(line.replace("{{"+pattern+"}}", subst))
	os.close(fh)
	#Remove original file
	os.remove(file_path)
	#Move new file
	move(abs_path, file_path)

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def get_text(file):
	with open(file, "r") as filename:
		text = filename.read()
	return text

def copy_over(src, dest, resfile, ignored=None):
	if not resfile == None:
		resname = basename(resfile)
	if os.path.isdir(src):
		if not os.path.isdir(dest):
			os.makedirs(dest)
		if resfile != None and os.path.isdir(dest):
			copyfile(resfile, dest + "/" + resname)
		files = os.listdir(src)
		for f in files:
			if f not in ignored:
				copy_over(os.path.join(src, f), os.path.join(dest, f), resfile, ignored)
	else:
		copyfile(src, dest)

def get_relative_template(sourcefile, template, base_dir=None):
	correct = template
	if "{{BASEDIR}}" in template:
		if base_dir != None:
			directory = base_dir
		else:
			num = sourcefile.count("\\")
			directory = ""
			if num > 1:
				directory += (num-1) * "../"
		correct = template.replace("{{BASEDIR}}", directory)
	elif "{{DATE}}" in template:
		current_date = date.today().strftime("%B %d, %Y")
		correct = template.replace("{{DATE}}", current_date)
	return correct

def usage():
	print("Welcome to Stitcher!")
	print("-t\t--templatedir\tPath to template directory (Is current directory if directory is not supplied)")
	print("-s\t--srcdir\t\tPath to source directory (Is '../src' if not supplied")
	print("-r\t--resourcefile\tPath to resource file. Resource file will be copied to all destination folders.")
	print("-o\t--outdir\t\tPath to output directory (Is '../dist' if not supplied\n")
	print("-v\t--verbose\t\tHave verbose output.\n")
	print("-b\t--basedir\t\tSet BASDIR inside of .TEMPLATE files (Normally dynamically set to 'outdir'\n")
	print("-f\t--filetype\t\tSet filetype for files to check for template calls (Is '.html' normally)")
	print("-h\t--help\t\t\tPrint help")

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hb:r:t:s:o:v", ["help", "verbose", "templatedir=", "srcdir=", "outdir=", "resourcefile=", "basedir="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	destination = '../dist'
	source = '../src'
	templates = '.'
	file_type = ".html"
	verbose = False
	resourcefile = None
	base_dir = None
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit(2)
		elif opt in ("-t", "--templatedir"):
			templates = arg
		elif opt in ("-o", "--outdir"):
			destination = arg
		elif opt in ("-s", "--srcdir"):
			source = arg
		elif opt in ("-v", "--verbose"):
			verbose = True
		elif opt in ("-r", "--resourcefile"):
			resourcefile = arg
		elif opt in ("-b", "--basedir"):
			base_dir = arg
		elif opt in ("-f", "--filetype"):
			file_type = arg
		else:
			print("Unexpected option '" + opt + "'!")
			usage()
			sys.exit(2)

	print("Building...")

	if destination == '':
		print("No output directory supplied!")
		usage()
		sys.exit(2)
	if source == '':
		print("No source directory supplied!")
		usage()
		sys.exit(2)

	copy_over(source, destination, resourcefile, ["Blog-Adder.jar", "Game Adder.jar", "project"])

	templates = templates.strip(' ')
	if verbose:
		print("Getting templates from '"+templates+"'")

	for templatefile in find_files(templates, '*.TEMPLATE'):
		template = get_text(templatefile)
		templatename = templatefile.strip(".TEMPLATE\\").upper()
		templatename = templatename.rsplit('\\', 1)[-1]
		if verbose:
			print("\t-"+templatename)
		for filename in find_files(destination, '*' + file_type):
			if verbose:
				print("\t\t"+"Building '"+filename+"'")
			full_templ = get_relative_template(filename, template, base_dir)
			replace(filename, templatename, full_templ)
	print("Done!")

if __name__ == "__main__":
    main(sys.argv[1:])