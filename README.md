[![Build Status](https://github.com/ladybug-tools/ladybug-display/workflows/CI/badge.svg)](https://github.com/ladybug-tools/ladybug-display/actions)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Python 2.7](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-270/) [![IronPython](https://img.shields.io/badge/ironpython-2.7-red.svg)](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8/)

# ladybug-display

A library that assigns basic display attributes to ladybug-geometry objects
(color, line weight, line type, etc). It also extends several core Ladybug objects
with methods to translate them to a VisualzationSet (Sunpath, WindRose, etc.).

## Installation
```console
pip install ladybug-display
```

## QuickStart
```python
import ladybug_display

```

## [API Documentation](http://ladybug-tools.github.io/ladybug-display/docs)

## Local Development
1. Clone this repo locally
```console
git clone git@github.com:ladybug-tools/ladybug-display

# or

git clone https://github.com/ladybug-tools/ladybug-display
```
2. Install dependencies:
```console
cd ladybug-display
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

3. Run Tests:
```console
python -m pytest tests/
```

4. Generate Documentation:
```console
sphinx-apidoc -f -e -d 4 -o ./docs ./ladybug_display
sphinx-build -b html ./docs ./docs/_build/docs
```
