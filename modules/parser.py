from typing import Any

from modules.custom_print import print_error, print_warning, print_info
from modules.tools import convert_to_bool


class ParserException(Exception):
	pass


class InvalidArgument(ParserException):
	pass


class MissingArgument(InvalidArgument):
	pass


class InvalidCharacter(ParserException):
	pass


def parse_input(input_string: str) -> list[dict]:
	def get_string_until_char_match(char: str, func_input_string: str, start_index: int = 0) -> (int, str):
		"""
		Iterates over string until a character match is found.
		:param char: The character to stop at
		:param func_input_string: The string to search
		:param start_index: The index to start searching from
		:return: (int, str) => (index of found, string)
		"""
		i: int = start_index
		while i < len(func_input_string):
			if func_input_string[i] == char:
				return i, func_input_string[start_index:i]
			i += 1

		return i, func_input_string[start_index:]

	def get_section_with_name(name: str, current_output: list) -> dict:
		for item in current_output:
			if item["type"] == "section" and item["title"] == name:
				return item
		raise ValueError(f"Section {name} not found")

	def is_section_empty(current_section: list) -> bool:
		for _line in current_section:
			if _line:
				return False
		return True

	output: list[dict] = []
	this_section_name: str = ""
	this_section_content: list[list[dict[str, Any]]] = []
	this_section_settings: dict[str, Any] = {}
	title: str = ""
	description: str = ""
	order: str = ""

	additional_settings: dict[str, Any] = {
		"ignore_closing_section": False,
		"ignore_useless_lines": False,
	}

	chord_buffer: str = ""

	lines = input_string.splitlines()
	for index, line in enumerate(lines):
		if line.startswith('#'):
			continue

		display_line_index: int = index + 1

		this_line_content: list[dict[str, str]] = []

		current_character_index: int = 0
		while current_character_index < len(line):
			current_character: str = line[current_character_index]
			if current_character == "{":
				end_index, string = get_string_until_char_match("}", line, current_character_index + 1)
				current_character_index = end_index + 1

				split_command: list = string.split(" ")
				if split_command[0] == "title":
					if len(split_command) < 2:
						print_error(
							f"Error on line {display_line_index}: Missing required argument for title: [title_name]\n\t(at {line})")
						raise MissingArgument()
					if title != "":
						print_warning(f"Warning on line {display_line_index}: Title is already set. Overwriting.")
					split_command.pop(0)
					title = " ".join(split_command)
				elif split_command[0] == "description":
					if len(split_command) < 2:
						print_error(
							f"Error on line {display_line_index}: Missing required argument for description: [description]\n\t(at {line})")
						raise MissingArgument()
					if description != "":
						print_warning(f"Warning on line {display_line_index}: Description is already set. Appending.")
						description += "\n"
					split_command.pop(0)
					description += " ".join(split_command)
				elif split_command[0] == "order":
					if len(split_command) < 2:
						print_error(
							f"Error on line {display_line_index}: Missing required argument for order: [order_number]\n\t(at {line})")
						raise MissingArgument()
					if order != 0:
						print_warning(f"Warning on line {display_line_index}: Order is already set. Overwriting.")
					split_command.pop(0)
					order = " ".join(split_command)
				elif split_command[0] in ["begin", "beginsection", "section"]:
					if this_section_name != "":
						if not additional_settings["ignore_closing_section"]:
							print_warning(
								f"Warning on line {display_line_index}: Current section ({this_section_name}) wasn't properly closed with {{endsection}}. Manually ending the section.")
						if len(this_section_content) != 0:
							this_section_content.append(this_line_content)
							output.append({
								"type": "section",
								"title": this_section_name,
								"lines": this_section_content,
							})

					this_section_content = []
					this_section_name = " ".join(split_command[1:])
				elif split_command[0] in ["end", "endsection", "sectionend"]:
					if this_section_name == "":
						print_error(
							f"Error on line {display_line_index}: Section was ended without a section starting.\n\t(at {line})")
						raise InvalidArgument()
					this_section_content.append(this_line_content)
					if not is_section_empty(this_section_content):
						output.append({
							"type": "section",
							"title": this_section_name,
							"lines": this_section_content,
							"settings": this_section_settings,
						})
					else:
						try:
							output.append(get_section_with_name(this_section_name, output))
							print_info(f"Info on line {display_line_index}: Re-using section {this_section_name}, since definition was empty.\n\t(at: {line})")
						except ValueError:
							print_warning(f"Warning on line {display_line_index}: Blank section {this_section_name} wasn't defined. Skipping.\n\t(at: {line})")

					this_section_content = []
					this_section_name = ""
					this_section_settings = {}
				elif split_command[0] == "setting":
					if len(split_command) < 2:
						print_warning(f"Warning on line {display_line_index}: Missing required arguments for setting: [setting_name], [setting_value]. Skipping.\n\t(at {line})")
					elif len(split_command) < 3:
						print_warning(f"Warning on line {display_line_index}: Missing required argument for setting: [setting_value]. Skipping.\n\t(at {line})")
					else:
						split_command.pop(0)
						setting_name = split_command.pop(0)
						setting_contents = " ".join(split_command)

						if setting_name == "hidden":
							if this_section_name == "":
								print_error(f"Error on line {display_line_index}: Setting `hidden` can only be used in a section.\n\t(at {line})")
								raise InvalidArgument()
							try:
								this_section_settings["hidden"] = convert_to_bool(setting_contents)
								if not convert_to_bool(setting_contents):
									if not additional_settings["ignore_useless_lines"]:
										print_warning(f"Warning on line {display_line_index}: Setting `hidden` is redundant.\n\t(at {line})")
							except ValueError:
								print_error(f"Error on line {display_line_index}: Invalid argument type. Expected boolean.\n\t(at {line})")
								raise InvalidArgument()

						elif setting_name not in additional_settings:
							additional_settings[setting_name] = setting_contents
							print_warning(f"Warning on line {display_line_index}: {setting_name} isn't a valid setting..\n\t(at {line})")
						elif setting_name == "ignore_closing_section":
							try:
								additional_settings[setting_name] = convert_to_bool(setting_contents)
							except ValueError as e:
								print_warning(f"Warning on line {display_line_index}: {e} (treated as warning).\n\t(at {line})")


				continue

			elif current_character == "[":
				end_index, string = get_string_until_char_match("]", line, current_character_index + 1)
				current_character_index = end_index + 1

				chord_buffer += string
				continue

			this_line_content.append({"char": current_character, "chord": chord_buffer})
			chord_buffer = ""
			current_character_index += 1

		if chord_buffer != "":
			this_line_content.append({"char": "", "chord": chord_buffer})
			chord_buffer = ""

		this_section_content.append(this_line_content)

	if this_section_name != "":
		if not additional_settings["ignore_closing_section"]:
			print_warning(
				f"Warning on line {len(lines) - 1}: Current section ({this_section_name}) wasn't properly closed with {{endsection}}. Manually ending the section.")

		if not is_section_empty(this_section_content):
			output.append({
				"type": "section",
				"title": this_section_name,
				"lines": this_section_content,
				"settings": this_section_settings,
			})
		else:
			try:
				output.append(get_section_with_name(this_section_name, output))
				print_info(f"Info on line {len(lines)}: Re-using section {this_section_name}, since definition was empty")
			except ValueError:
				print_warning(f"Blank section {this_section_name} wasn't defined. Skipping.")

	output.append({
		"type": "title",
		"title": title,
		"description": description,
		"order": order,
	})

	return output


def parse_input_to_html(input_string: str) -> str:
	output: str = ""

	title_block: str = ("<div class='title-block'>"
	                    "<h1>TITLE</h1>"
	                    "<p>DESCRIPTION</p>"
	                    "<div class='order-block'>"
	                    "ORDER"
	                    "</div>"
	                    "</div>")

	parsed_content = parse_input(input_string)

	order_given: bool = False

	for section in parsed_content:
		if section["type"] == "title":
			title_block = title_block.replace("TITLE", section["title"])
			title_block = title_block.replace("DESCRIPTION", section["description"])
			if section["order"] != "":
				title_block = title_block.replace("ORDER", section["order"])
				order_given = True



		elif section["type"] == "section":
			if "hidden" in section["settings"].keys():
				if section["settings"]["hidden"]:
					continue
			output += "<br><div class='section-block'>"
			output += f"<p><strong><u>{section["title"]}</u></strong></p>"
			for line in section["lines"]:
				chord_buffer: str = ""

				chord_line: str = ""
				text_line: str = ""

				for char_item in line:
					if char_item["chord"] == "":
						if chord_buffer == "":
							chord_buffer += " "
					else:
						chord_buffer += char_item["chord"]

					chord_line += chord_buffer[0]
					chord_buffer = chord_buffer[1:]

					text_line += char_item["char"]
				chord_line += chord_buffer

				output += f"<p><strong>{chord_line}</strong></p>"
				output += f"<p>{text_line}</p>"
				output += "<br>"

			output += "</div>"


		else:
			print_error(f"Error: section type {section['type']} was not expected.")

	if not order_given:
		title_block = title_block.replace("ORDER", "")
	return title_block + output

def convert_file_to_html(path: str) -> str:
	with open(path, "r") as file:
		return parse_input_to_html(file.read())
