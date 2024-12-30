import argparse
import sys

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from modules.custom_print import print_info, print_ok, print_error
from modules.parser import convert_file_to_html, ParserException
from modules.resource_path import resource_path

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


def convert_html_to_pdf(html_content, output_path):
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
		    font-size: {options["scale"]}em;
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
	html.write_pdf(output_path, stylesheets=[css, CSS(string="@page { size: A4; margin: 1cm }")], font_config=font_configuration)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description="Create chord charts from score files"
	)

	parser.add_argument(
		"input_file",
		type=str,
		help="Path to the score file"
	)

	parser.add_argument(
		"output_file",
		type=str,
		help="Path to the output PDF file"
	)
	parser.add_argument(
		"--scale", "-s",
		type=float,
		default=0.8,
		help="Scale the PDF text"
	)
	options = vars(parser.parse_args())

	print_info(f"Creating chord charts from {options["input_file"]}")

	try:
		html = convert_file_to_html(options["input_file"])
	except ParserException as e:
		print_error(f"An error occurred while converting input to PDF")
		sys.exit(1)
	except FileNotFoundError:
		print_error(f"Error: could not find input path {options["input_file"]}")
		print_error(f"An error occurred while looking for the file")
		sys.exit(1)

	convert_html_to_pdf(
		insert_content(
			"Score",
			html
		),
		options["output_file"]
	)

	print_ok(f"Wrote PDF to {options["output_file"]}")
