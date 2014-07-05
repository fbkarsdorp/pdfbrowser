import codecs
import os
from os.path import basename, splitext, join, abspath
import re
import subprocess

from whoosh import index

from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED, DATETIME
from whoosh.analysis import StemmingAnalyzer, SimpleAnalyzer

from config import ROOT, SRC, DATA, PDFTOTEXT_PATH

SCHEMA = Schema(id     = ID(stored=True),
                path   = ID(stored=True),
                source = ID(stored=True),
                body   = TEXT(analyzer=SimpleAnalyzer()))

u = unicode

def fileid(filepath):
    base, ext = splitext(basename(filepath))
    return base

def extract_text_from_pdf(filepath):
    target = fileid(filepath)
    subprocess.call([PDFTOTEXT_PATH, filepath, join(DATA, target + ".txt")])
    with codecs.open(join(DATA, target + ".txt")) as infile:
        return infile.read()

if __name__ == '__main__':
    if not os.path.exists(os.path.join(ROOT, 'index')):
        os.mkdir(os.path.join(ROOT, 'index'))
        ix = index.create_in(os.path.join(ROOT, 'index'), schema = SCHEMA, indexname="pdfs")

    if not os.path.exists(DATA):
        os.mkdir(DATA)

    if not os.path.exists(SRC):
        os.mkdir(SRC)        

    ix = index.open_dir(os.path.join(ROOT, 'index'), indexname="pdfs")
    writer = ix.writer()
    indexed = set(map(fileid, os.listdir(DATA)))
    for filename in os.listdir(SRC):
        if fileid(filename) not in indexed and filename.endswith(".pdf"):
            filesrc = abspath(join(SRC, filename))
            filetarget = abspath(join(DATA, fileid(filename) + ".txt"))
            try:
                writer.add_document(id   = u(fileid(filesrc)), 
                                    path = u(filetarget),
                                    source = u(filesrc),
                                    body = u(extract_text_from_pdf(filesrc), 'latin-1'))
            except (UnicodeDecodeError, IOError):
                print filename
    writer.commit()
