#!/usr/bin/env python

from urllib.request import urlopen, Request
from w3lib.encoding import html_to_unicode
# from jinja2 import Template

from pydepta.depta import Depta
from lxml import etree

from flask import Flask, request
app = Flask(__name__)


def transpose(xss):
    """
    transpose a list of lists
    >>> transpose([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]
    """
    return [list(x) for x in zip(*xss)]


def fetch_url(url):
    info = urlopen(Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 \
        Safari/537.36'
    }))
    _, html = html_to_unicode(info.headers.get('content_type'), info.read())
    return html


def region_to_html(region, show_headers=False, show_html=False):
    cells = region.items
    if not cells:
        return ''

    """
    template = Template(
    <!-- pre>{{ metadata }}</pre -->

    res.append('<table border="1">')
    {% if show_headers % }
    <tr>
        {% for tag in col_tags %}
        <th>{{ tag }}</th>
        {% endfor %}
    </tr>
    {% endif %}

    {% for row in cells %}
        {% for cell in row %}
        <td>{{cell}}</td>
        {% endfor %}
    {% endfor %}

    """
    res = []
    '''
    res.append('<!-- pre>%s</pre -->' % (
        json.dumps(region.metadata, sort_keys=True, indent=4,
                   separators=(',', ': ')), ))
    '''

    res.append('<table border="1">')

    '''
    if show_headers:
        res.append("<tr>")
        for tag in col_tags:
            res.append("<th>%s</th>" % (tag, ))
        res.append("</tr>")
    '''

    for row in cells:
        res.append("<tr>")

        for cell in row:
            if show_html:
                res.append("<td>%s</td>" %
                           (etree.tostring(cell.html, pretty_print=True,
                                           encoding='unicode'), ))
            else:
                res.append("<td>%s</td>" % (cell.text, ))

        res.append("</tr>")

    res.append("</table>")
    return '\n'.join(res)


def process_url(url):
    html = fetch_url(url=url)
    depta = Depta()
    regions = depta.extract(html)
    res = []

    for region in regions:
        res.append(region_to_html(region, show_headers=True, show_html=False))

    return """<br/><br/><h3>cells</h3>""".join(res)


def show_home():
    return """<h3>Depta Server</h3>"""


@app.route('/')
def depta():
    url = request.args.get('url')
    if url:
        print('url', url)
        return process_url(url)
    else:
        return show_home()


app.run(host='localhost', port=8888)
