from dominate.tags import *
from bottle import run, route, static_file, get, request, html_escape
import dominate
import pdfkit
import csv
from time import time


@route('/')
def index():
    return index_page()


@route('/premier')
def premier():
    return premier_page()


@route('/invoice')
def invoice():
    return invoice_page()


def index_page():
    doc = dominate.document(title='Home Page')
    with doc.head:
        # CSS
        link(rel='stylesheet', href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css')

        # JS
        script(type='text/javascript', src='https://code.jquery.com/jquery-1.11.3.min.js')
        script(type='text/javascript', src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js')
    with doc.body:
        h1('Bottle Dominate PDF Playground')
        with div(style='margin-top:60px'):
            a('Football', cls='btn btn-default', href='/premier')
            a('Invoice', cls='btn btn-default', href='/invoice')

    return doc.render()


def premier_page():
    """Function for generating HTML page through Python code."""
    
    doc = dominate.document(title='Premier League Table')
    with doc.head:
        # JS <scripts></script>
        script(type='text/javascript', src='https://code.jquery.com/jquery-1.11.3.min.js')
        script(type='text/javascript', src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js')
        script(type='text/javascript', src='pnotify.custom.min.js')
        script(type='text/javascript', src='serve.js')

        # CSS <link>
        link(rel='stylesheet', href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css')
        link(rel='stylesheet', href='pnotify.custom.min.css')
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
    doc = dominate.document(title='List of invoices')
    with doc.head:
        # JS <scripts></script>
        script(type='text/javascript', src='https://code.jquery.com/jquery-1.11.3.min.js')
        script(type='text/javascript', src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js')
        script(type='text/javascript', src='pnotify.custom.min.js')
        script(type='text/javascript', src='serve.js')

        # CSS <link>
        link(rel='stylesheet', href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css')
        link(rel='stylesheet', href='pnotify.custom.min.css')

    with doc.body:
        h1('Invoice List')
        with div(id='content', cls='panel panel-default'):
            with table(cls='table', id='export'):
                with open('invoice.csv', 'r') as f:
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
    if request.is_ajax:
        data = request.body.read()
        options = {'page-size':'A4'}
        page = dominate.document()
        with page.head:
            # CSS
            style("""td, th{text-align: left;}
                     table{width: 100%;}""")
            # JS
            script(type='text/javascript', src='https://code.jquery.com/jquery-1.11.3.min.js')
            script(
                """
                $(document).ready(function(){
                  $('tr:even').css('background-color', '#cfcfcf');
                  $('tr:odd').css('background-color', '#e1e1e1');
                });

                """, type='text/javascript')
        page.body.add(h1('Premier League Championship 2015'))
        page.body.add_raw_string(data)
        name = 'export_' + str(time()) + '.pdf'
        page = page.render()
        print page
        pdfkit.from_string(page, name, options=options)
        return 'OK'


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
    run(host='localhost', port=4000, debug=True, reloader=True)
