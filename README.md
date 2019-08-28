# standalone_nbviewer
Standalone viewer for jupyter-notebooks
* spawns own window -> `qtviewer.py`
* renders in default browser -> `browser.py`


## requirements
* gerneral: 
    * `python3.7` (not tested with older versions)
    * `QT 5.13.0`
* python:
    * `nbformat` 
    * `nbconvert` 
    * `PyQt5 5.13.0` (`qtviewer.py`)
    * `PyQtWebEngine` (`qtviewer.py`)

## qtviewer.py
Standalone qt viewer for jupyter-notebook files
* requirements: 
    * `nbformat` (read jupyter-notebooks)
    * `nbconvert` (converts them to html)
    * `PyQt5` (rendering)
    * `PyQtWebEngine` (rendering)
    
## browser.py
Renders jupyter-notebook files in the default browser
* requirements: 
    * `nbformat` (read jupyter-notebooks)
    * `nbconvert` (converts them to html)
    