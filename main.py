from flask import Flask, render_template, redirect, url_for, request, flash
import os
import uuid
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

app = Flask(__name__)
app.config['SECRET_KEY']=str(uuid.uuid4())

data_dir="data"

@app.route("/")
def create_paste():
    return render_template('create_paste.html')

@app.route("/paste", methods=['POST'])
def save_paste():
    title= request.form['title']
    title= os.path.basename(title)
    text= request.form['text']

    if not title:
        title = "Untitled"
    if not text:
        flash("Text is empty")
        return redirect(url_for('create_paste'))

    paste_id = str(uuid.uuid4())
    paste_dir = os.path.join(data_dir, paste_id)
    
    if not os.path.exists(paste_dir):
        os.makedirs(paste_dir)

    paste_file= os.path.join(paste_dir, title)
    print (paste_file)

    with open(paste_file, 'w', newline='\n') as f:
        f.write(text)

    return redirect(url_for('show_paste', paste_id=paste_id, name=title))

@app.route("/show/<paste_id>/<name>")
def show_paste(paste_id, name):
    paste_file = os.path.join(data_dir, paste_id, name)
    if not os.path.exists(paste_file):
        code = ''
        name = 'No such paste'
    else:
        with open(paste_file, newline='\n') as f:
            code= f.read()
            try:
                lexer= guess_lexer_for_filename(name, code)
            except ClassNotFound:
                lexer= get_lexer_by_name('text') 

            formatter = HtmlFormatter(linenos=True, style="colorful")
            code = highlight(code, lexer, formatter)
    return render_template("show_paste.html",code= code, title=name)



if __name__ == "__main__":
    app.run()