import argparse
import os
import sys

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from modules.custom_print import print_info, print_ok, print_error
from modules.parser import convert_file_to_html, ParserException
from modules.resource_path import resource_path
from os.path import join, isfile, isdir, splitext, basename

from modules.watcher import watch

options: dict = {
}


def insert_content(title, content) -> str:
	return f'''
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
	    <title>{title}</title>
	</head>
	<body>
	    {content}
	</body>
	</html>
	'''


def convert_html_to_pdf(html_content, output_path, this_options):
	font_configuration = FontConfiguration()
	html = HTML(string=html_content)
	css_contents = f'''
		@font-face {{
		    font-family: "JetBrains Mono";
		    src: url("{resource_path("fonts/JetBrainsMono-Regular.woff2")}");
		}}
		
		@font-face {{
		    font-family: "JetBrains Mono";
		    font-weight: bold;
		    src: url("{resource_path("fonts/JetBrainsMono-ExtraBold.woff2")}");
		}}
		
		@font-face {{
		    font-family: "JetBrains Mono";
		    font-style: italic;
		    src: url("{resource_path("fonts/JetBrainsMono-Italic.woff2")}");
		}}
		
		@font-face {{
		    font-family: "JetBrains Mono";
		    font-weight: bold;
		    font-style: italic;
		    src: url("{resource_path("fonts/JetBrainsMono-BoldItalic.woff2")}");
		}}
		
		body {{
		    font-family: "JetBrains Mono", monospace;
		    white-space: pre;
		    font-size: {this_options["scale"]}em;
		}}
		
		.title-block {{
		    border: 1px solid #333333;
		    * {{
		        margin: 10px;
		    }}
            margin-top: 0 !important;
		}}
		
		.section-block {{
		    line-height: 1em;
		    margin: 0;
		    padding: 0;
		    break-inside: avoid;
		    * {{
		        margin: 0;
		        padding: 0;
		    }}
		}}
	'''
	# Use css_contents for autofill-ing paths
	css = CSS(string=css_contents, font_config=font_configuration)
	html.write_pdf(output_path, stylesheets=[css, CSS(string="@page { size: A4; margin: 1cm }")],
	               font_config=font_configuration)


def parse_files(this_options):
	print(this_options)
	files_to_convert: list = []
	if isdir(this_options["input_path"]):
		files_to_convert = [join(this_options["input_path"], i) for i in os.listdir(this_options["input_path"]) if
		                    isfile(join(this_options["input_path"], i))]
	else:
		files_to_convert.append(this_options["input_path"])

	try:
		for index, file in enumerate(files_to_convert):
			output_file_location: str = this_options["output_path"]
			if output_file_location == "" or isdir(output_file_location):
				# output_file_location = os.path.splitext(file)[0] + ".pdf"
				output_file_name = basename(file).split(".")[0] + ".pdf"
				output_file_location = join(output_file_location, output_file_name)

			printstr: str = f"Converting {file} to pdf"
			if len(files_to_convert) > 1:
				printstr += f" ({index + 1}/{len(files_to_convert)})"
			print(printstr)
			html = convert_file_to_html(file)

			convert_html_to_pdf(
				insert_content(
					"Score",
					html
				),
				output_file_location,
				this_options
			)

			print_ok(f"Wrote PDF to {output_file_location}")

	except ParserException as e:
		print_error(f"An error occurred while converting input to PDF")
		sys.exit(1)
	except FileNotFoundError:
		print_error(f"Error: could not find input path {this_options["input_path"]}")
		print_error(f"An error occurred while looking for the file")
		sys.exit(1)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description="Create chord charts from score files"
	)

	parser.add_argument(
		"input_path",
		type=str,
		help="Path to the score file or a directory that contains score files."
	)

	parser.add_argument(
		"--watch", "-w",
		type=bool,
		default=False,
		help="Whether to watch the given file/directory for changes, and compile automatically on change."
	)

	parser.add_argument(
		"--output-path", "-o",
		type=str,
		help="Path to the output PDF file. Defaults to the input file's name, but with a .pdf extension",
		default=""
	)
	parser.add_argument(
		"--scale", "-s",
		type=float,
		default=0.8,
		help="Scale the PDF text"
	)
	options = vars(parser.parse_args())

	if options["watch"]:
		if not os.path.isdir(options["input_path"]):
			print_error(f"Error: input path {options["input_path"]} is not a directory.\n\tWhen using --watch, input_path must be a directory.")
			sys.exit(1)
		watch(options["input_path"], options)
	else:
		parse_files(options)

	print_ok("Done")
