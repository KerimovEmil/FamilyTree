# Client JavaScript

This directory contains client-side scripts used by the interactive views:

- `topola-bundle.min.js`: Self-contained, minified bundle containing the [PeWu/topola](https://github.com/PeWu/topola) layout engine (Relatives, Hourglass, Ancestors, Descendants) and D3 Zoom & Pan. No external npm dependencies are required at runtime.
- `interactive_graph.js`: Interactive graph controller that initializes the SVG canvas, handles view projection switching, autocomplete person searching, smooth D3 zooming/panning, and node action popovers.
