import sys
import nbformat
from nbconvert import HTMLExporter
from http.server import BaseHTTPRequestHandler,HTTPServer
import webbrowser


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


def LoadInDefaultBrowser(html):
    """
    Load html in default browser.

    Parameters
    ----------
    html : str or bytes
        html code

    """
    if not isinstance(html, bytes):
        html = html.encode()
    class myHandler(BaseHTTPRequestHandler):
        """
        Hanndle any incoming request from a browser
        """
        # Handler for the GET requests
        def do_GET(self):
            print   ('Get request received')
            self.send_response(200)
            self.send_header(b'Content-type','text/html')
            self.end_headers()
            # Send the html message
            self.wfile.write(html)
            return

    try:
        # Create a web server and define the handler to manage the
        # incoming request
        server = HTTPServer(('', 0), myHandler)
        print ('Started httpserver : http://127.0.0.1:{}'.format(server.server_port))
        webbrowser.open('http://127.0.0.1:{}'.format(server.server_port))
        # Wait forever for incoming http requests
        #server.serve_forever()
        server.handle_request()
    except KeyboardInterrupt:
        print ('^C received, shutting down the web server')
        server.socket.close()


def main(files):
    """
    Routine to spawn multiple windows per file
    Parameters
    ----------
    files : List[str] or str
    """

    if isinstance(files, str):
        LoadInDefaultBrowser(notebook_to_html(files))
    else:
        for fname in files:
            LoadInDefaultBrowser(notebook_to_html(fname))


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Missing notebook...\nUse:')
        print('python {} notebook.ipynb'.format(sys.argv[0]))
        print('multiple files are possible')
        sys.exit(0)
    main(files=sys.argv[1:])