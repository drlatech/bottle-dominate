# Bottle Dominate  PDF Playground

This is not real project, it is more playground where I tried to make some combination with **bottle framework** and **dominate**
library to avoid using HTML templates. So you are writing only Python code for all, models, controllers and views.
I didn't consider about performance and efficiency because, at the moment, I don't think that this will have mass usage.
The other thing is playing with various PDF generator libraries, such as **pdfkit**, **xhtml2pdf**, **PyPDF** and some other.
I based on those which generates PDF from HTML.

For those who finds it interesting and want try to involve, feel free to fork and try to improve it better than me.
Requirements:

```bash
pip install bottle dominate pdfkit PyPDF2 xhtml2pdf geraldo reportlab
```

### Small example of usual Web application for every Web Framework

```python
from dominate.tags import *
from dominate import document
from bottle import get, post, request, run

@get('/')
@post('/')
def index():
    """
    Function for returning index page view (home page).
    :return: html: str - generated html
    """
    if request.POST:
        name = request.forms.get('name')
        surname = request.forms.get('surname')
        resp = dominate.document(title='POST DATA')
        with resp.body:
            h1('Welcome {} {}'.format(name, surname))
            h1('Happy learning')
        return resp.render()
    else:
        return index_page()

def index_page():
    """Function for generating index HTML page
       :return: HTML page
    """
    doc = base_page()
    doc.title = 'Home Page'
    with doc.body:
        h1('Bottle Dominate PDF Playground')
        with div(style='margin-top:60px'):
            # a('Football', cls='btn btn-default', href='/premier')
            # a('Invoice', cls='btn btn-default', href='/invoice')

            with form(method='POST', action='/'):
                with div(id='fname'):
                    label('First name')
                    input(type='text', name='name')
                with div(id='lname'):
                    label('Last name')
                    input(type='text', name='surname')
                input(type='submit', cls= 'btn btn-info', value='Show full name')

    return doc.render()


def base_page():
    """
    Basic template for all pages.
    It includes all headers, styles, footer and other stuff.
    It will be passed to other specific views which will add to DOM, things that every of these views show.
    :return: object of <dominate.document> class
    """
    doc = dominate.document()
    with doc.head:
        # CSS
        link(rel='stylesheet', href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css')

        # JS
        script(type='text/javascript', src='https://code.jquery.com/jquery-1.11.3.min.js')
        script(type='text/javascript', src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js')
    return doc

if __name__ == '__main__':
    run(host='localhost', port='5000')
```
Save this as *app.py* and start it in terminal from path where script is located.

```shell
mint@linux~$ python app.py
```
After starting script, open this address on web browser: *localhost:5000* and play with it.
