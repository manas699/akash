#!/usr/bin/env python3
"""
Mind Map to Document Converter Agent

This agent converts notebook LM mind maps to various document formats including:
- Word documents (.docx)
- Markdown (.md)
- HTML (.html)
- Plain text (.txt)

Supports both JSON and XML mind map formats from notebook LM.
"""

import json
import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum

try:
    from docx import Document
    from docx.shared import Inches
    from docx.enum.style import WD_STYLE_TYPE
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from bs4 import BeautifulSoup
    import markdown
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)


class OutputFormat(Enum):
    """Supported output formats for mind map conversion."""
    DOCX = "docx"
    MARKDOWN = "md"
    HTML = "html"
    TXT = "txt"


@dataclass
class MindMapNode:
    """Represents a node in the mind map structure."""
    title: str
    content: Optional[str] = None
    children: List['MindMapNode'] = None
    level: int = 0
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


class MindMapParser:
    """Parses mind map data from various formats."""
    
    @staticmethod
    def parse_json(data: Union[str, Dict]) -> MindMapNode:
        """Parse mind map from JSON format."""
        if isinstance(data, str):
            data = json.loads(data)
        
        def create_node(node_data: Dict, level: int = 0) -> MindMapNode:
            title = node_data.get('title', node_data.get('name', 'Untitled'))
            content = node_data.get('content', node_data.get('description', ''))
            
            node = MindMapNode(title=title, content=content, level=level)
            
            # Handle various possible child keys
            children_data = (node_data.get('children', []) or 
                           node_data.get('subtopics', []) or 
                           node_data.get('branches', []))
            
            for child_data in children_data:
                child_node = create_node(child_data, level + 1)
                node.children.append(child_node)
            
            return node
        
        return create_node(data)
    
    @staticmethod
    def parse_xml(xml_content: str) -> MindMapNode:
        """Parse mind map from XML format."""
        soup = BeautifulSoup(xml_content, 'html.parser')
        
        def create_node_from_xml(element, level: int = 0) -> MindMapNode:
            title = (element.get('title') or 
                    element.get('name') or 
                    element.get_text(strip=True) or 
                    'Untitled')
            
            content = element.get('content', '')
            if not content and element.find('content'):
                content = element.find('content').get_text(strip=True)
            
            node = MindMapNode(title=title, content=content, level=level)
            
            # Find child nodes
            child_elements = (element.find_all('child') or 
                            element.find_all('node') or 
                            element.find_all('topic'))
            
            for child_elem in child_elements:
                child_node = create_node_from_xml(child_elem, level + 1)
                node.children.append(child_node)
            
            return node
        
        root_element = soup.find('root') or soup.find('map') or soup.find('mindmap')
        if not root_element:
            # If no specific root, use the first element
            root_element = soup.find()
        
        return create_node_from_xml(root_element)


class DocumentGenerator:
    """Generates documents in various formats from mind map data."""
    
    def __init__(self, mind_map: MindMapNode):
        self.mind_map = mind_map
    
    def to_docx(self, output_path: str) -> None:
        """Convert mind map to Word document format."""
        doc = Document()
        
        # Add title
        title = doc.add_heading(self.mind_map.title, 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        if self.mind_map.content:
            doc.add_paragraph(self.mind_map.content)
        
        def add_node_to_doc(node: MindMapNode):
            """Recursively add nodes to document."""
            if node.level > 0:  # Skip root node as it's already added as title
                # Add heading based on level (max level 6 for Word)
                heading_level = min(node.level, 6)
                doc.add_heading(node.title, heading_level)
                
                if node.content:
                    doc.add_paragraph(node.content)
            
            for child in node.children:
                add_node_to_doc(child)
        
        for child in self.mind_map.children:
            add_node_to_doc(child)
        
        doc.save(output_path)
    
    def to_markdown(self, output_path: str) -> None:
        """Convert mind map to Markdown format."""
        lines = []
        
        # Add title
        lines.append(f"# {self.mind_map.title}\n")
        
        if self.mind_map.content:
            lines.append(f"{self.mind_map.content}\n")
        
        def add_node_to_md(node: MindMapNode):
            """Recursively add nodes to markdown."""
            if node.level > 0:  # Skip root node
                # Add heading with appropriate level
                heading_prefix = "#" * min(node.level + 1, 6)
                lines.append(f"{heading_prefix} {node.title}\n")
                
                if node.content:
                    lines.append(f"{node.content}\n")
            
            for child in node.children:
                add_node_to_md(child)
        
        for child in self.mind_map.children:
            add_node_to_md(child)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def to_html(self, output_path: str) -> None:
        """Convert mind map to HTML format."""
        # First convert to markdown, then to HTML
        md_content = []
        
        # Add title
        md_content.append(f"# {self.mind_map.title}\n")
        
        if self.mind_map.content:
            md_content.append(f"{self.mind_map.content}\n")
        
        def add_node_to_md(node: MindMapNode):
            """Recursively add nodes to markdown."""
            if node.level > 0:  # Skip root node
                heading_prefix = "#" * min(node.level + 1, 6)
                md_content.append(f"{heading_prefix} {node.title}\n")
                
                if node.content:
                    md_content.append(f"{node.content}\n")
            
            for child in node.children:
                add_node_to_md(child)
        
        for child in self.mind_map.children:
            add_node_to_md(child)
        
        # Convert markdown to HTML
        md_text = '\n'.join(md_content)
        html_content = markdown.markdown(md_text)
        
        # Wrap in complete HTML document
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.mind_map.title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #333;
            margin-top: 1.5em;
        }}
        h1 {{
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
    
    def to_txt(self, output_path: str) -> None:
        """Convert mind map to plain text format."""
        lines = []
        
        # Add title
        lines.append(self.mind_map.title.upper())
        lines.append("=" * len(self.mind_map.title))
        lines.append("")
        
        if self.mind_map.content:
            lines.append(self.mind_map.content)
            lines.append("")
        
        def add_node_to_txt(node: MindMapNode):
            """Recursively add nodes to text."""
            if node.level > 0:  # Skip root node
                # Add indentation based on level
                indent = "  " * (node.level - 1)
                lines.append(f"{indent}- {node.title}")
                
                if node.content:
                    content_indent = "  " * node.level
                    lines.append(f"{content_indent}{node.content}")
                    lines.append("")
            
            for child in node.children:
                add_node_to_txt(child)
        
        for child in self.mind_map.children:
            add_node_to_txt(child)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


class MindMapConverter:
    """Main converter class that orchestrates the conversion process."""
    
    def __init__(self):
        self.supported_input_formats = ['.json', '.xml', '.txt']
        self.supported_output_formats = list(OutputFormat)
    
    def detect_input_format(self, file_path: str) -> str:
        """Detect the format of the input file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Try to detect JSON
        try:
            json.loads(content)
            return 'json'
        except json.JSONDecodeError:
            pass
        
        # Try to detect XML
        if content.startswith('<') and content.endswith('>'):
            try:
                BeautifulSoup(content, 'html.parser')
                return 'xml'
            except:
                pass
        
        # Default to text format
        return 'txt'
    
    def parse_input_file(self, file_path: str) -> MindMapNode:
        """Parse the input file and return a mind map structure."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        file_format = self.detect_input_format(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if file_format == 'json':
            return MindMapParser.parse_json(content)
        elif file_format == 'xml':
            return MindMapParser.parse_xml(content)
        else:
            # For text format, create a simple structure
            lines = content.strip().split('\n')
            root = MindMapNode(title=lines[0] if lines else "Mind Map")
            
            for line in lines[1:]:
                line = line.strip()
                if line:
                    # Simple parsing: count leading spaces/tabs for hierarchy
                    level = len(line) - len(line.lstrip())
                    title = line.strip('- ').strip()
                    child = MindMapNode(title=title, level=level + 1)
                    root.children.append(child)
            
            return root
    
    def convert(self, input_path: str, output_path: str, output_format: OutputFormat) -> None:
        """Convert mind map from input file to specified output format."""
        print(f"Parsing input file: {input_path}")
        mind_map = self.parse_input_file(input_path)
        
        print(f"Converting to {output_format.value} format...")
        generator = DocumentGenerator(mind_map)
        
        if output_format == OutputFormat.DOCX:
            generator.to_docx(output_path)
        elif output_format == OutputFormat.MARKDOWN:
            generator.to_markdown(output_path)
        elif output_format == OutputFormat.HTML:
            generator.to_html(output_path)
        elif output_format == OutputFormat.TXT:
            generator.to_txt(output_path)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        print(f"Conversion completed: {output_path}")


def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Convert notebook LM mind maps to various document formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mind_map_converter.py input.json output.docx
  python mind_map_converter.py input.xml output.md
  python mind_map_converter.py input.json output.html --format html
  python mind_map_converter.py input.txt output.txt
        """
    )
    
    parser.add_argument('input', help='Input mind map file (JSON, XML, or TXT)')
    parser.add_argument('output', help='Output document file')
    parser.add_argument(
        '--format', '-f',
        choices=[fmt.value for fmt in OutputFormat],
        help='Output format (auto-detected from file extension if not specified)'
    )
    
    args = parser.parse_args()
    
    # Determine output format
    if args.format:
        output_format = OutputFormat(args.format)
    else:
        # Auto-detect from file extension
        ext = Path(args.output).suffix.lower().lstrip('.')
        try:
            output_format = OutputFormat(ext)
        except ValueError:
            print(f"Error: Cannot determine output format from extension '.{ext}'")
            print(f"Supported formats: {[fmt.value for fmt in OutputFormat]}")
            sys.exit(1)
    
    # Perform conversion
    try:
        converter = MindMapConverter()
        converter.convert(args.input, args.output, output_format)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()