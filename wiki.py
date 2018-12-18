import os
import sys
from pathlib import Path
import os.path
import markdown
import codecs
import glob
import random
import webbrowser
import threading
from random import shuffle

from flask import Flask, redirect, url_for
from flask import render_template
from flask import send_from_directory
from flask import request

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

allowed_upload_extensions = ['jpg', 'png', 'gif', 'bmp', 'jpeg']

class EditForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = PageDownField('content', validators=[DataRequired()])
    submit = SubmitField('submit')

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    submit = SubmitField('submit')

def gen_file_path( wikiname ):
    site_root = os.path.dirname(sys.argv[0])
    return os.path.join(site_root, "wiki", wikiname+".md")

def gen_image_path():
    site_root = os.path.dirname(sys.argv[0])
    return os.path.join(site_root, "wiki", "images" )

def random_file_path():
    site_root = os.path.dirname(sys.argv[0])
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

@app.route("/wiki/search/<keyword>")
def search(keyword):
    keyword = keyword.strip()

    # generate a list of files containing this keyword
    site_root = os.path.dirname(sys.argv[0])
    all_path = glob.glob( os.path.join(site_root, "wiki/*.md") )
    shuffle( all_path )
    file_list = []
    for file in all_path:
        with open(file) as f:
            contents = f.read()
            if keyword in contents:
                file_list.append( file )

    # generate a tmp wiki for this keyword
    def generate_wiki_link( file_path ):
        file_name = Path( file_path )
        entry = file_name.stem
        return '0. [' + entry + '](./' + entry + ')\n'

    generated_markdown = '### ' + keyword + " Collection\n\n ------ \n\n" # <-- header
    for file in file_list:
        generated_markdown += generate_wiki_link( file )

    search_wiki_name = '.search_result_for_' + keyword
    search_result_file_name = './wiki/' + search_wiki_name + '.md'
    with open(search_result_file_name, 'w') as outfile:
        outfile.write( generated_markdown )

    # show generated tmp wiki
    return redirect(url_for('show_wiki', wikiname=search_wiki_name))

@app.route("/wiki/search", methods=["POST", "GET"])
def search_it():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('search', keyword=search_form.search.data))
    return render_template('search.html', search_form=search_form)

@app.route("/wiki/upload", methods=["POST", "GET"])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and ('.' in file.filename) and (file.filename.rsplit('.',1)[1] in allowed_upload_extensions):
            file.save(os.path.join( gen_image_path(), file.filename))
            return redirect(url_for('upload'))
    all_files = os.listdir( gen_image_path() )
    return render_template('upload.html', all_files=all_files)

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
    site_root = os.path.dirname(sys.argv[0])
    #site_root = os.path.realpath(os.path.dirname(__file__))
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

@app.route("/wiki/<wikiname>/home")
def direct_home(wikiname):
    return redirect(url_for('show_wiki', wikiname='home'))

@app.route("/wiki/<wikiname>/random_wiki")
def direct_random(wikiname):
    return redirect(url_for('random_wiki'))

@app.route("/wiki/<wikiname>/search")
def direct_search(wikiname):
    return redirect(url_for('search_it'))

@app.route("/wiki/<wikiname>/upload")
def direct_upload(wikiname):
    return redirect(url_for('upload'))

@app.route('/')
def index():
    return redirect(url_for('show_wiki', wikiname='home') )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def run_app( debug=True, port='8897' ):
    app.run(debug=debug, port=port)


if __name__ == '__main__':
    threading.Thread(target=run_app, args=(False, '8897') ).start()
    webbrowser.open_new( 'http://127.0.0.1:8897' )

