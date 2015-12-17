from dominate.tags import *
import dominate
from bottle import run, route, static_file, get, request, response
import csv
from time import time
import os
# PDF manipulation libraries
import pdfkit


@route('/')
def index():
    """
    Function for returning index page view (home page).
    :return: html: str - generated html
    """
    return index_page()


@route('/premier')
def premier():
    """
    Function for returning premier page view.
    :return: html: str - generated html
    """
    return premier_page()


@route('/invoice')
def invoice():
    """
    Function for returning invoice page view.
    :return: html: str - generated html
    """
    return invoice_page()


def base_page():
    """
    Basic template for all pages.
    It includes all headers, styles, footer and other stuff.
    It will be passed to other specific views which will add to DOM, things that every of these views show.
    :return: object of <dominate.document> class
    """
    doc = dominate.document(title='Home Page')
    with doc.head:
        # CSS
        link(rel='stylesheet', href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css')
        link(rel='stylesheet', href='jquery.pnotify.default.css')

        # JS
        script(type='text/javascript', src='https://code.jquery.com/jquery-1.11.3.min.js')
        script(type='text/javascript', src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js')
        script(type='text/javascript', src='jquery.pnotify.min.js')
        script(type='text/javascript', src='serve.js')
    return doc


def index_page():
    """Function for generating index HTML page
       :return: HTML page
    """
    doc = base_page()
    with doc.body:
        h1('Bottle Dominate PDF Playground')
        with div(style='margin-top:60px'):
            # a('Football', cls='btn btn-default', href='/premier')
            # a('Invoice', cls='btn btn-default', href='/invoice')
            input(type='button', cls= 'btn btn-info', id='premier', value='Football')
            input(type='button', cls= 'btn btn-info', id='invoice', value='Invoice')

    return doc.render()


def premier_page():
    """Function for generating premier HTML page
       :return: HTML page
    """
    doc = base_page()
    with doc.body:
        h1('Premier League Championship 2015')
        with div(id='content', cls='panel panel-default'):
            with table(cls='table', id='export'):
                with open('football.csv', 'r') as f:
                    data = [row for row in csv.reader(f.read().splitlines())]
                with thead():
                    with tr():
                        for h in data[0]:
                            th(h)
                with tbody():
                    for row in data[1:]:
                        with tr():
                            for tb in row:
                                td(tb)
        input(type='button', id='btnSend', value='Export PDF', cls='btn btn-default')

    return doc.render()
    

def invoice_page():
    """
    Function for generating invoice HTML page
    :return: HTML page
    """
    doc = base_page()
    with doc.body:
        h1('Invoice List')
        with div(id='content', cls='panel panel-default'):
            with table(cls='table', id='export'):
                with open('table.csv', 'r') as f:
                    data = [row for row in csv.reader(f.read().splitlines())]
                with thead():
                    with tr():
                        for h in data[0]:
                            th(h)
                with tbody():
                    for row in data[1:]:
                        with tr():
                            for tb in row:
                                td(tb)
        input(type='button', id='btnSend', value='Export PDF', cls='btn btn-default')

    return doc.render()


@route('/pdf', method='POST')
def pdf_it():
    """
    Function for generating PDF from HTML and some options which are defined in this function. Function is taking AJAX
    POST data that represents html <table> generated in view and append it in <body> block.
    :return: name: str - name of generated PDF file
    """
    if request.is_ajax:
        # POST data
        data = request.body.read()
        # Options of PDF
        options = {'page-size': 'A4',
                   'orientation': 'Landscape'
        }
        page = dominate.document('PDF Export')
        with page.head:
            # CSS
            style("""td, th{text-align: left;}
                     table{width: 100%;}
                     tr{
                        page-break-inside: avoid;
                     }
                  """
            )
            # JS
            script(type='text/javascript', src='https://code.jquery.com/jquery-1.11.3.min.js')
            script(
                """
                $(document).ready(function(){
                  $('tr:even').css('background-color', '#cfcfcf');
                  $('tr:odd').css('background-color', '#e1e1e1');
                });

                """, type='text/javascript')

        page.body.add_raw_string(data)
        name = 'export_' + str(time()) + '.pdf'
        page = page.render()
        # Change directory to tmp for storing PDFs.
        try:
            os.mkdir('tmp')
        except OSError:
            # Passing exceptions is really bad habit, but in this case it is not necessary to process it, because it is
            # raised if folder already exists, so this doesn't mean anything, and checking for folder existing with
            # trying to make it is more important thing.
            pass
        path = 'tmp/' + name
        pdfkit.from_string(page, path, options=options)
        return name


@route('/showpdf/<name>')
def show_pdf(name):
    """
    Function for returning PDF file as response which is generated in pdf_it function. It is necessary to setup headers
     from response to make it appropriate PDF response.
    :param name: str - name of the generated PDF that should be shown inline or as a attachment.
    :return: PDF file
    """
    response.set_header('Content-type', 'application/pdf')
    response.set_header('Content-Disposition', 'inline;filename={}'.format(name))
    path = 'tmp/' + name
    pdf = file(path, 'rb')
    return pdf


@get('/<filename:re:.*\.js>')
def javascripts(filename):
    """Function for setting path of javascript files.
       :param filename: name of local .js file.
    """
    return static_file(filename, root='static/js/')


@get('/<filename:re:.*\.css>')
def csss(filename):
    """Function for setting path of css files.
       :param filename: name of local .css file.
    """
    return static_file(filename, root='static/css/')


if __name__ == '__main__':
    run(host='localhost', port=4000, debug=True, reloader=True, server='diesel')
