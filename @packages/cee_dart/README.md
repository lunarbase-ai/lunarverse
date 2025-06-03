# CEE DART Navigator

A Python package for biological pathway analysis and evidence integration.

## Installation

```bash
pip install -e .
```

## Features

- Evidence integration from multiple sources
- gProfiler integration for pathway analysis
- PharmGKB integration for drug-gene interactions
- CIVIC integration for clinical evidence
- Likely Related Paths (LRP) analysis
- Graph-based analysis tools

## Usage

```python
from cee_dart_navigator import agents, core, utils

# Example usage with gProfiler
from cee_dart_navigator.agents.gprofiler import main as gprofiler
# Your code here

# Example usage with LRP
from cee_dart_navigator.core.lrp import graph, comparison
# Your code here
```

## Development

1. Clone the repository
2. Install development dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`

## License

MIT License 