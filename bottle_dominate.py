from dominate.tags import *
from bottle import run, route, static_file, get, request
import dominate
import pdfkit
import csv



@route('/')
def index():
    return index_page()


def index_page():
    '''Function for generating HTML page through Python code.'''
    
    doc = dominate.document(title='Home page')
    with doc.head:
        link(rel='stylesheet', href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css')
        script(type='text/javascript', src='https://code.jquery.com/jquery-1.11.3.min.js')
        script(type='text/javascript', src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js')
        script(type='text/javascript', src='serve.js')
    with doc.body:
        with div(id='content', cls='panel panel-default'):
            with table(cls='table'):
                with open('football.csv','r') as f:
                    data = [row for row in csv.reader(f.read().splitlines())]
                with thead(color='green'):
                    with tr():
                        for h in data[0]:
                            th(h)
                with tbody(color='blue'):

                    for row in data[1:]:
                        with tr():
                            for tb in row:
                                td(tb)
        # button('Export to pdf',id='export_1',  cls='btn btn-default')
        input(type='button', id='btnSend', value='Export PDF', cls='btn btn-default')

    return doc.render()
    

@route('/pdf', method='POST')
def pdfit():
    with open('football.csv','r') as f:
        data = [row for row in csv.reader(f.read().splitlines())]
        if request.method == 'POST':
            options = {'page-size':'A4'}
            page = """<html><body>
            <table style="width:100%">
            <thead>
            <tr>
            """
            h = ''
            for i in data[0]:
                h += "<td>%s</td>"%str(i)
            page += (h + '</tr></thead>')

            tb = '<tbody>'
            for row in data[1:]:
                tb += '<tr>'
                for t in row:
                    tb += '<td>%s</td>'% str(t)
                tb += '</tr></tbody>'
            page += tb
            page += '</body></html>'
            print page
            pdfkit.from_string(str(page), 'export_1.pdf', options=options)
            return  'OK'


@get('/<filename:re:.*\.js>')
def javascripts(filename):
    '''Function for setting path of javascript files.'''
    return static_file(filename, root='static/js/')




if __name__ == '__main__':
    run(host='localhost', port=4000, debug=True, reloader=True)
