# Runescape Helper

A helper application for Runescape 3, compatible with Silicon Mac computers.

This application provides various plugins to assist with gameplay, such as timers for boss abilities.

## Installation

```bash
pip install runescape_helper
```

## Usage
```python
from runescape_helper import Application
from runescape_helper.plugins import CroesusHelper

app = Application()
croesus_helper = CroesusHelper()
app.load_plugin(croesus_helper)
app.start()
```

## Development
This project is in early development, we welcome contributions. Please see the open issues for a list of proposed 
features (and known issues).

## Copyright
Copyright (c) 2023 Max. See LICENSE for details.