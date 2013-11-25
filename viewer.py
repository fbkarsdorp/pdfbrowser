import codecs
from os.path import splitext, basename, join
from flask import Flask, request, jsonify, make_response, render_template
import whoosh
from whoosh import index
from whoosh import qparser

def search(query):
    ix = whoosh.index.open_dir('index', indexname="pdfs")
    with ix.searcher() as searcher:

        def _search(query):
            query = qparser.QueryParser("body", ix.schema).parse(query)
            return searcher.search(query, limit=20)

        def htmlize(hits):
            html = ''
            for hit in hits:
                fileid = hit['id']
                filesource = join("static/sources", basename(hit['source']))
                filepath = hit['path']
                with codecs.open(splitext(filepath)[0] + ".txt", encoding='latin-1') as fileobj:
                    filecontents = fileobj.read()
                html += "<div id='match'><span id='idee'><a href='%s' target='_blank'>%s</a></span></br><span id='text'>%s</span></div>" % (
                    filesource, fileid, hit.highlights("body", text=filecontents))
            return html

        return htmlize(_search(query))



app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def api():
    return jsonify({'html': search(request.form['q'].strip())})

@app.route('/')
def index():
    return render_template('index.html', title='PDF viewer')

if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=8000,use_reloader=True,threaded=True)


