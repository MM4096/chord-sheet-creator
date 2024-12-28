import argparse

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from modules.custom_print import print_info, print_ok, print_error
from modules.parser import convert_file_to_html, ParserException


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
	css_contents = '''
		@font-face {
		    font-family: "JetBrains Mono";
		    src: url("fonts/JetBrainsMono-Regular.woff2");
		}
		
		@font-face {
		    font-family: "JetBrains Mono";
		    font-weight: bold;
		    src: url("fonts/JetBrainsMono-ExtraBold.woff2");
		}
		
		@font-face {
		    font-family: "JetBrains Mono";
		    font-style: italic;
		    src: url("fonts/JetBrainsMono-Italic.woff2");
		}
		
		@font-face {
		    font-family: "JetBrains Mono";
		    font-weight: bold;
		    font-style: italic;
		    src: url("fonts/JetBrainsMono-BoldItalic.woff2");
		}
		
		body {
		    font-family: "JetBrains Mono", monospace;
		    white-space: pre;
		    font-size: 0.8em;
		}
		
		.title-block {
		    border: 1px solid #333333;
		    * {
		        margin: 10px;
		    }
		}
		
		.section-block {
		    line-height: 1em;
		    margin: 0;
		    padding: 0;
		    * {
		        margin: 0;
		        padding: 0;
		    }
		}
	'''
	css = CSS(string=css_contents, font_config=font_configuration)
	html.write_pdf(output_path, stylesheets=[css, CSS(string="@page { size: A4; margin: 0.5cm }")], font_config=font_configuration)


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

	print_info(f"Creating chord charts from {parser.parse_args().input_file}")

	try:
		html = convert_file_to_html(parser.parse_args().input_file)
	except ParserException as e:
		print_error(f"An error occurred while converting input to PDF")
		exit(1)
	except FileNotFoundError:
		print_error(f"Error: could not find input path {parser.parse_args().input_file}")
		print_error(f"An error occurred while looking for the file")
		exit(1)

	convert_html_to_pdf(
		insert_content(
			"Score",
			html
		),
		parser.parse_args().output_file
	)

	print_ok(f"Wrote PDF to {parser.parse_args().output_file}")
