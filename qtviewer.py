#!/usr/bin/env python3.7
"""
Standalone viewer to render jupyter-notebooks files.
Can handle multiple files.
"""
import sys

import nbformat
from nbconvert import HTMLExporter
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView


def notebook_to_html(fname):
    """
    Converts a notebook to html code.

    Parameters
    ----------
    fname : str
        Filename of the jupyter-notebook file

    Returns
    -------
    body : str
        html code of the page
    """
    notebook = nbformat.read(fname, nbformat.NO_CONVERT)

    html_exporter = HTMLExporter()

    (body, resources) = html_exporter.from_notebook_node(notebook)
    return body


class NotebookViewer(QWebEngineView):
    started = pyqtSignal()
    def __init__(self, fname):
        """
        Notebook viewer to render a notebook in a window.
        Parameters
        ----------
        fname : str
            Filename of the jupyter-notebook file.
        """
        super(NotebookViewer, self).__init__()

        self.setHtml(notebook_to_html(fname))
        self.setWindowTitle(fname)

    def show(self):
        # reimplementation
        self.started.emit()
        super(NotebookViewer, self).show()


def main(files):
    """
    Routine to spawn multiple windows per file
    Parameters
    ----------
    files : List[str] or str
    """
    app = QApplication(sys.argv)

    if isinstance(files, str):
        widget = NotebookViewer(files)
        widget.show()
    else:
        widgets = []
        for i, fname in enumerate(files):
            widgets.append(NotebookViewer(fname))
            if i > 0:
                widgets[i - 1].started.connect(widgets[i].show)
        widgets[0].show()

    sys.exit(app.exec_())


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Missing notebook...\nUse:')
        print('python {} notebook.ipynb'.format(sys.argv[0]))
        print('multiple files are possible')
        sys.exit(0)

    main(files=sys.argv[1:])
