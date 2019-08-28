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
        Filename of the jupyter notebook file

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
            Filename of the jupyter notebook file.
        """
        super(NotebookViewer, self).__init__()

        self.setHtml(notebook_to_html(fname))
        self.setWindowTitle(fname)

    def show(self):
        # reimplementation
        self.started.emit()
        super(NotebookViewer, self).show()


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Missing notebook...\nUse:')
        print('python {} notebook.ipynb'.format(sys.argv[0]))
        print('multiple files are possible')
        sys.exit(0)

    app = QApplication(sys.argv)
    widgets = []
    for i,fname in enumerate(sys.argv[1:]):
        widgets.append(NotebookViewer(fname))
        if i > 0:
            widgets[i-1].started.connect(widgets[i].show)
    widgets[0].show()
    sys.exit(app.exec_())
