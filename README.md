# Chord Chart Creator
Create beautiful chord charts for any song!

![Demonstration of Converted PDF](documentation/images/demo_pdf.png)

*Joy to the World, Verse 1 and Interlude 1, rendered*

# Usage
```
usage: chord-chart-creator [-h] [--watch WATCH] [--output-path OUTPUT_PATH] [--scale SCALE] input_file
```

### `input-file` (required)
The path to the input path or directory.
If a directory is given, all files in that directory are converted non-recursively, **_even if it isn't a score file_**.


See [Syntax](#syntax) for the syntax of this file.

### `--output-file` or `-o`
Output location of the rendered PDF.

If `--output-file` is not given, or is a directory, the resulting file is stored in `cwd/output_if_directory/input_file(noextention).pdf`

For example:
```text
chord-chart-creator ./scores --output-file ./output
```
will convert files as follows:
```text
cwd
├─ scores
|  ├─- a.score
|  ├─- asdf.someotherextension
|  ├─- hi_there
|  └─- text_file.txt
|
├─ output
|  ├─ a.pdf
|  ├─ asdf.pdf
|  ├─ hi_there.pdf
|  └─ text_file.pdf
```

### `-s` or `--scale`
Text scale on the rendered PDF (default: `0.8`)

### `-w` or `--watch`
If set to `True`, the program doesn't exit, but compiles all source files in `input_file` (which must be a directory) everytime a file is edited. 

### `-h`
Help menu. Use with any other arguments to get their description.


# Syntax
Files are read from top to bottom.

Lines beginning with a `#` (hashtag) are ignored as comments.

Characters are rendered on the **main line** unless wrapped in special characters, where they act as functions.

## Functions
### Chords
Chords are wrapped in square brackets (`[ ]`). Anything in square brackets are treated as chords and are written on the **top line** above the character that immediately follows it.

As an example, the text `[G]Joy` is rendered as:
```text
G
Joy
```
And `[Em]King` is rendered as:
```text
Em
King
```

Square brackets can contain *any text*, not necessarily chords. The interlude of Joy to the World, seen in the introduction, is written like this:
```text
{begin Interlude}
[G C D G | C D Em . | Gsus/C . . .]
{end}
```

### Title
A title can be specified by using `{title <your-title-here>`, and defaults to ` ` (an empty string)

### Description
A description can be specified using `{description <your-description-here>}`.

### Section
Sections define a group of words and chords, such as a verse, chorus or bridge.

Sections start with `{begin <name>}`, `{section <name>}` or `{startsection <name>}`, and finish with `{end}`, `{sectionend}` or `{endsection}`.

If you don't end a section, a warning will be printed unless `ignore_closing_section` is set to `True`.

#### Defined sections
If you've already created a section (i.e. `Interlude`), you can create another empty section with the same name to copy the previous section over.

For example, the following file:
```text
{begin Interlude}
[G C D G | C D Em . | Gsus/C . . .]
{end}

{begin Other Section}
...Other Irrelevant Text...
{end}

{begin Interlude}
{end}
```
renders as follows:
```text
Interlude
G C D G | C D Em . | Gsus/C . . .

Other Section
...Other Irrelevant Text...

Interlude
G C D G | C D Em . | Gsus/C . . .
```
Note that if a section with the same name wasn't defined before usage, a warning is displayed.


### Settings
Settings, as a general template, are defined using `{setting <name> <value>}`.
A detailed table of all settings is given below:

| Setting Name             | Type   | Default Value | Description                                                                                                      |
|--------------------------|--------|---------------|------------------------------------------------------------------------------------------------------------------|
| `ignore_closing_section` | `bool` | `False`       | Ignore sections without a matching `end` tag (Don't warn)                                                        |
| `ignore_useless_lines`   | `bool` | `False`       | Ignores warnings generated by lines with no effect (i.e. `{setting hidden false}`)                               |
| `hidden`                 | `bool` | `False`       | **Affects only a single section** Toggles visibility for a section. If not used in a section, an error is thrown |