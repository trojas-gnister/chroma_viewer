# ChromaDB CLI Viewer

A command-line interface tool for viewing and inspecting ChromaDB collections.

## Features

- List all available collections
- View collection details and metadata
- Preview collection contents
- Basic authentication support
- Interactive CLI interface

## Installation

1. Clone the repository
2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the viewer with the following command:

```bash
python chroma_viewer.py --host HOST --port PORT --username USERNAME --password PASSWORD
```

## Interactive Commands

Once connected, you can:

1. List collections - Shows all available collections
2. View collection details - Displays collection information and content preview
3. Exit - Close the viewer
