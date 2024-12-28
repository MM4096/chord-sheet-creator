from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from modules.parser import convert_file_to_html


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
	css = CSS("style.css", font_config=font_configuration)
	html.write_pdf(output_path, stylesheets=[css, CSS(string="@page { size: A4; margin: 0.5cm }")], font_config=font_configuration)


if __name__ == '__main__':
	convert_html_to_pdf(
		insert_content(
			"Score",
			convert_file_to_html("tests/test_input.score"),
		),
		"tests/out.pdf"
	)
