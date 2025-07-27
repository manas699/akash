# Mind Map to Document Converter Agent

A powerful Python agent that converts notebook LM mind maps to various document formats including Word documents (.docx), Markdown (.md), HTML (.html), and plain text (.txt).

## Features

- **Multiple Input Formats**: Supports JSON, XML, and plain text mind map formats
- **Multiple Output Formats**: Convert to Word documents, Markdown, HTML, or plain text
- **Hierarchical Structure**: Preserves mind map hierarchy in all output formats
- **Auto-Detection**: Automatically detects input format and output format from file extensions
- **Rich Formatting**: Generates well-formatted documents with proper headings and structure
- **Command-Line Interface**: Easy-to-use CLI for batch processing and automation

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python mind_map_converter.py input_file output_file
```

The output format is automatically detected from the file extension:

```bash
# Convert JSON mind map to Word document
python mind_map_converter.py examples/sample_mindmap.json output.docx

# Convert XML mind map to Markdown
python mind_map_converter.py examples/sample_mindmap.xml output.md

# Convert text mind map to HTML
python mind_map_converter.py examples/sample_mindmap.txt output.html
```

### Advanced Usage

You can explicitly specify the output format using the `--format` or `-f` flag:

```bash
python mind_map_converter.py input.json output.doc --format docx
python mind_map_converter.py input.xml report --format html
```

### Supported Formats

#### Input Formats
- **JSON** (.json): Structured JSON with nested objects
- **XML** (.xml): XML format with hierarchical elements
- **Text** (.txt): Plain text with indentation-based hierarchy

#### Output Formats
- **Word Document** (.docx): Professional document format
- **Markdown** (.md): GitHub-flavored markdown
- **HTML** (.html): Web-ready HTML with embedded CSS
- **Plain Text** (.txt): Simple text format with indentation

## Input Format Examples

### JSON Format
```json
{
  "title": "Main Topic",
  "content": "Description of the main topic",
  "children": [
    {
      "title": "Subtopic 1",
      "content": "Description of subtopic 1",
      "children": [
        {
          "title": "Sub-subtopic",
          "content": "More detailed information"
        }
      ]
    }
  ]
}
```

### XML Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<mindmap>
  <root title="Main Topic" content="Description">
    <node title="Subtopic 1" content="Description">
      <child title="Sub-subtopic" content="Details" />
    </node>
  </root>
</mindmap>
```

### Text Format
```
Main Topic
- Subtopic 1
  - Sub-subtopic 1
  - Sub-subtopic 2
- Subtopic 2
  - Another sub-subtopic
```

## Examples

The `examples/` directory contains sample mind map files in different formats:

- `sample_mindmap.json`: Artificial Intelligence overview
- `sample_mindmap.xml`: Project Management methodology
- `sample_mindmap.txt`: Web Development fundamentals

Try converting these examples:

```bash
# Convert AI overview to Word document
python mind_map_converter.py examples/sample_mindmap.json ai_overview.docx

# Convert project management to HTML
python mind_map_converter.py examples/sample_mindmap.xml project_management.html

# Convert web development to Markdown
python mind_map_converter.py examples/sample_mindmap.txt web_dev.md
```

## API Usage

You can also use the converter programmatically:

```python
from mind_map_converter import MindMapConverter, OutputFormat

# Create converter instance
converter = MindMapConverter()

# Convert mind map
converter.convert(
    input_path="input.json",
    output_path="output.docx",
    output_format=OutputFormat.DOCX
)
```

## Output Examples

### Word Document (.docx)
- Professional formatting with proper headings
- Hierarchical structure using Word's heading levels
- Centered title and well-organized content

### Markdown (.md)
- GitHub-flavored markdown with proper heading hierarchy
- Clean, readable format perfect for documentation
- Compatible with most markdown processors

### HTML (.html)
- Complete HTML document with embedded CSS
- Responsive design that looks good on all devices
- Professional styling with proper typography

### Plain Text (.txt)
- Simple indented structure
- Easy to read and parse
- Compatible with any text editor

## Error Handling

The converter includes comprehensive error handling:

- **File not found**: Clear error message when input file doesn't exist
- **Invalid format**: Helpful messages for unsupported file formats
- **Parse errors**: Detailed information about JSON/XML parsing issues
- **Permission errors**: Clear guidance when files can't be written

## Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`:
  - python-docx (for Word document generation)
  - beautifulsoup4 (for XML parsing)
  - lxml (for XML processing)
  - markdown (for HTML generation)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Support

If you encounter any issues or have questions, please open an issue on the project repository.
