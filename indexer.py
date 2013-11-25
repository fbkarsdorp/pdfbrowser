import codecs
import os
from os.path import basename, splitext, join, abspath
import re
import sh

from whoosh import index

from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, DATETIME
from whoosh.analysis import StemmingAnalyzer, SimpleAnalyzer

SCHEMA = Schema(id     = ID(stored=True),
                path   = ID(stored=True),
                source = ID(stored=True),
                body   = TEXT(analyzer=SimpleAnalyzer()))

ROOT = 'data'
SRC = 'static/sources'

u = unicode

def fileid(filepath):
    base, ext = splitext(basename(filepath))
    return base

def extract_text_from_pdf(filepath):
    target = fileid(filepath)
    sh.pdftotext(filepath, join(ROOT, target + ".txt"))
    with codecs.open(join(ROOT, target + ".txt")) as infile:
        return infile.read()

if __name__ == '__main__':
    if not os.path.exists('index'):
        os.mkdir('index')

    ix = index.create_in('index', schema = SCHEMA, indexname="pdfs")
    ix = index.open_dir('index', indexname="pdfs")
    writer = ix.writer()

    indexed = set(map(fileid, os.listdir(ROOT)))
    for filename in os.listdir(SRC):
        if fileid(filename) not in indexed and filename.endswith(".pdf"):
            filesrc = abspath(join(SRC, filename))
            filetarget = abspath(join(ROOT, fileid(filename) + ".txt"))
            try:
                writer.add_document(id   = u(fileid(filesrc)), 
                                    path = u(filetarget),
                                    source = u(filesrc),
                                    body = u(extract_text_from_pdf(filesrc), 'latin-1'))
            except (UnicodeDecodeError, IOError):
                print filename
    writer.commit()