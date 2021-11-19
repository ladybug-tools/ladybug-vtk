[![Build Status](https://github.com/ladybug-tools/ladybug-vtk/workflows/CI/badge.svg)](https://github.com/ladybug-tools/ladybug-vtk/actions)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

# ladybug-vtk

Provides methods for translating ladybug-geometry objects to VTK PolyData.

## Installation
```console
pip install ladybug-vtk
```

## QuickStart
```python
import ladybug_vtk

```

## [API Documentation](http://ladybug-tools.github.io/ladybug-vtk/docs)

## Local Development
1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools/ladybug-vtk

# or

git clone https://github.com/ladybug-tools/ladybug-vtk
```
2. Install dependencies:
```console
cd ladybug-vtk
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:
```console
python -m pytest tests/
```

4. Generate Documentation:
```console
sphinx-apidoc -f -e -d 4 -o ./docs ./ladybug_vtk
sphinx-build -b html ./docs ./docs/_build/docs
```
