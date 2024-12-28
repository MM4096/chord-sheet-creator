import re
from tkinter import Tk, Text, END

cached_text: str = ""
COLORS: dict[str: str] = {
	"normal": "#ffffff",
	"background": "#282828",
	# orange
	"brackets": "#eb4034",
	# green
	"keywords": "#859900"
}
COLOR_SCHEME: list[list] = [
	# Keywords
	[r'(?<=[ \[\]{}])(title|begin|beginsection|section|end|endsection)', COLORS["keywords"]],
	[r'[\(\)\{\}]', COLORS["brackets"]],
]

def select_all(event=None):
	textarea.tag_add("sel", "1.0", "end")
	return "break"

def search_regex(pattern, text, groupid=0):
	matches = []

	text = text.splitlines()
	for i, line in enumerate(text):
		for match in re.finditer(pattern, line):
			matches.append(
				(f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
			)

	return matches


def edit_changed(event=None):
	global cached_text

	# If actually no changes have been made stop / return the function
	if textarea.get('1.0', END) == cached_text:
		return

	# Remove all tags so they can be redrawn
	for tag in textarea.tag_names():
		textarea.tag_remove(tag, "1.0", "end")

	# Add tags where the search_re function found the pattern
	i = 0
	for pattern, color in COLOR_SCHEME:
		for start, end in search_regex(pattern, textarea.get('1.0', END)):
			textarea.tag_add(f'{i}', start, end)
			textarea.tag_config(f'{i}', foreground=color)

			i += 1

	cached_text = textarea.get('1.0', END)


if __name__ == "__main__":
	root = Tk()
	root.geometry("800x600")
	textarea = Text(
		root,
		background=COLORS["background"],
		foreground=COLORS["normal"],
		insertbackground=COLORS["normal"],
		relief="flat",
	)
	textarea.pack(
		fill="both",
		expand=True
	)
	textarea.insert("end", "{title My New Song}")
	textarea.bind("<KeyRelease>", edit_changed)
	textarea.bind("<Control-a>", select_all)

	edit_changed()
	root.mainloop()
