import os
import os.path
import markdown
import codecs
import glob
import random

from flask import Flask, redirect, url_for
from flask import render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from flask_pagedown.fields import PageDownField
from flask_pagedown import PageDown

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

pagedown = PageDown( app )

markdown_extensions=[ 'fenced_code', 'abbr', 'attr_list', 'def_list', 'footnotes', 'tables', 'def_list', 'admonition', 'meta', 'nl2br', 'sane_lists', 'smarty', 'toc', 'wikilinks' ]

class EditForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = PageDownField('content', validators=[DataRequired()])
    submit = SubmitField('submit')

def gen_file_path( wikiname ):
    site_root = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(site_root, "wiki", wikiname+".md")

def random_file_path():
    site_root = os.path.realpath(os.path.dirname(__file__))
    all_path = glob.glob( os.path.join(site_root, "wiki/*.md") )
    random_index = random.randint(0, len(all_path)-1)
    selected = all_path[random_index]
    full_file_name = (selected.split('/'))[-1]
    file_name = full_file_name[:len(full_file_name)-3] # remove '.md' extension
    return (selected, file_name)

def save_wiki( wikiname, content ):
    file_path = gen_file_path(wikiname)
    file = codecs.open(file_path, "w", "utf-8")
    file.write(content)
    file.close()

def read_wiki( wikiname ):
    file_path = gen_file_path(wikiname)
    content = ''
    if os.path.isfile(file_path):
        f = open(file_path, 'rt', encoding='utf-8', errors='replace')
        content = f.read()
    return content

@app.route("/wiki/random_wiki")
def random_wiki():
    file_path, wikiname = random_file_path()
    converted_html = markdown.markdown_from_file( file_path, output_format='html5', extensions=markdown_extensions )
    return render_template('wiki.html', converted_html=converted_html, wikiname=wikiname )

@app.route("/wiki/new_wiki", methods=("GET","POST"))
def new_wiki():
    content = 'Edit wontent with [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-CheatsheetC).'
    title = 'New Name'
    form = EditForm(title=title, content=content)
    if form.validate_on_submit():
        title, content = form.title.data, form.content.data
        title = title.replace(' ', '_')
        save_wiki( title, content )
        return redirect(url_for('show_wiki', wikiname=title))
    return render_template('edit.html', title=title, content=content, form=form, wikiname=title)

@app.route('/wiki/<wikiname>')
def show_wiki(wikiname):
    file_path = gen_file_path(wikiname)
    if os.path.isfile(file_path):
        converted_html = markdown.markdown_from_file( file_path, output_format='html5', extensions=markdown_extensions )
        return render_template('wiki.html', converted_html=converted_html, wikiname=wikiname )
    else:#404 here
        return "Error: " + file_path + " does not exist!"

def save_wiki( wikiname, content ):
    site_root = os.path.realpath(os.path.dirname(__file__))
    file_path = os.path.join(site_root, "wiki", wikiname+".md")
    file = codecs.open(file_path, "w", "utf-8")
    file.write(content)
    file.close()

@app.route("/wiki/<wikiname>/edit", methods=("GET","POST"))
def edit(wikiname):
    content = read_wiki(wikiname)
    title = wikiname.replace('_', ' ')
    form = EditForm(title=title, content=content)
    if form.validate_on_submit():
        title, content = form.title.data, form.content.data
        title = title.replace(' ', '_')
        save_wiki( title, content )
        return redirect(url_for('show_wiki', wikiname=wikiname))
    return render_template('edit.html', title=title, content=content, form=form, wikiname=wikiname)

@app.route('/')
def index():
    return redirect(url_for('show_wiki', wikiname='home') )

if __name__ == '__main__':
    #app.run(host= '0.0.0.0',debug=True, port='8893')
    #app.run(debug=True, port='8893')
    app.run(debug=True, port='8893')

