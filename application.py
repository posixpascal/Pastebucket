# Python Pastebucket Webserver
# Build on: Flask
# Developed on: Mac
# Developed using TextMate, Coda, Transmit and Python.
# DJango Release is coming soon.

import sqlite3
import datetime
import random
import string
import os
import time

# Flask Modules
from flask import Flask
from flask import render_template
from flask import g
from flask import session
from flask import url_for
from flask import request
from flask import abort
from flask import flash
from flask import redirect
from flask import Response
from flask import send_file
# My own Modules
from utils import FormParser

# Pygments Modules
from pygments import highlight
from pygments.lexers import (get_lexer_by_name, get_lexer_for_filename, get_lexer_for_mimetype)
from pygments.formatters import HtmlFormatter
from pygments.formatters import ImageFormatter
from pygments.formatters import RtfFormatter
from pygments.formatters import NullFormatter
from pygments.styles import get_style_by_name

# Standard Modules
from contextlib import closing


def convert(rtf, pdf):
    pipe = os.popen("sh rtf2pdf.sh %s %s"%(rtf, pdf), "r")
    




# Configuration
DATABASE = "database.db"
SECRET_KEY = "193r193h9sf0afa"
KEY_RANGE = [3,15]

def randomletters():
	return "".join(random.sample(string.letters+string.digits, random.randint(KEY_RANGE[0],KEY_RANGE[1])))

# Setup Flask Environment	
app = Flask(__name__)
app.config.from_object(__name__)

# Index Page
@app.route("/")
def index():
	return render_template('index.html')
	


# Create new Paste Page
@app.route("/paste/create")
def new():
	return render_template("new_paste.html")	


# Convert to Image
@app.route("/paste/img/<id>.png")
def paste_img_all(id):
	data = query_db("select * from pastes where id = ?", [id], one=True)
	try: Lexer = get_lexer_by_name(data["syntaxhighlight"].lower())
	except: Lexer = get_lexer_by_name("python")

	return Response(highlight(data["text"], Lexer, ImageFormatter(linenos=True)), mimetype="image/png")

	
	
	
	
# Show selected Page (view.html)	
@app.route("/paste/view/<id>")
def paste_view_all(id):
	data = query_db("select * from pastes where id = ?", [id], one=True)
	try: Lexer = get_lexer_by_name(data["syntaxhighlight"].lower())
	except: Lexer = get_lexer_by_name("python")
	
	return render_template("view.html", data=data, HtmlFormatter=HtmlFormatter, highlight=highlight(data["text"], Lexer, HtmlFormatter(linenos=False, cssclass="highlight")))





# Convert to RTF
@app.route("/paste/rtf/<id>.rtf")
def paste_rtf_all(id):
	data = query_db("select * from pastes where id = ?", [id], one=True)
	try: Lexer = get_lexer_by_name(data["syntaxhighlight"].lower())
	except: Lexer = get_lexer_by_name("python")
	return Response(highlight(data["text"], Lexer, RtfFormatter()), mimetype="application/rtf")


# Convert to RAW .txt
@app.route("/paste/raw/<id>.txt")
def paste_raw_all(id):
	data = query_db("select * from pastes where id = ?", [id], one=True)
	try: Lexer = get_lexer_by_name(data["syntaxhighlight"].lower())
	except: Lexer = get_lexer_by_name("python")
	return Response(highlight(data["text"], Lexer, NullFormatter()), mimetype="text/plain")




@app.route("/imprint")
def impressum():
	return render_template('impressum.html')







# Add new Paste.	
@app.route("/paste/add.do", methods=["POST"])
def new_paste():
	f = FormParser.new(request.form)
	title = f.get('title', "Untitled")
	paste = f.get('paste', "")
	syntax_highlight = f.get('syntax_highlight', None)
	private = f.get('private', 0)
	if title != None and paste != "" and syntax_highlight != None and private != None:
		id = randomletters()
		while query_db('select * from pastes where id = ?', [id], one=True) is not None:
			id = randomletters()
		
		g.db.execute("insert into pastes (id, title, text, private, syntaxhighlight, ip, date) values (?,?,?,?,?,?,?)", [id, title, paste, private, syntax_highlight, request.environ["REMOTE_ADDR"], datetime.datetime.now().strftime("%d.%m.%Y - %H:%M")])
		g.db.commit()
		return redirect("/paste/view/%s" % (id))	
	else: return "False"
	

@app.route("/ajax/harald/ask", methods=["POST"])
def harald_ask():
	return "PDF Datei wird erstellt."


@app.route("/ajax/harald/pdfw", methods=["POST"])
def harald_pdfw():
	f = FormParser.new(request.form)
	id = f.get('id', '0')
	data = query_db("select * from pastes where id = ?", [id], one=True)
	try: Lexer = get_lexer_by_name(data["syntaxhighlight"].lower())
	except: Lexer = get_lexer_by_name("python")
	with open(os.path.join("static","pdf",id + ".rtf"), "w") as rtfc:
		rtfc.write(highlight(data["text"], Lexer, RtfFormatter()))
	
	if not os.path.isfile("rtf2pdf.sh"): return "Fehler! Harald nicht gefunden."
	convert(os.path.join("static","pdf", id + ".rtf"), os.path.join("static","pdf", id + ".pdf"))
	return "Ready"


@app.route("/ajax/pdf;<id>")
def id_to_pdf(id):
	return render_template('pdf/start_pdf.html', pdfk={'id':id})

# Do the Ajax Magic
@app.route("/ajax/search", methods=["POST", "GET"])
def ajax_search():
	f = query_db("SELECT * FROM pastes WHERE title LIKE ? LIMIT 4 OFFSET ?", ["%"+FormParser.new(request.form).get('q',"0")+"%", 4*int(FormParser.new(request.form).get('page','0'))])
	if f == []: return "Keine Treffer auf Seite %s" % (str(int(FormParser.new(request.form).get('page','0'))+1))
	else:
		string = ""
		for match in f: # teffer
			for key in match: # dictionary treffer
				if key == "title": string += "<a style='text-decoration:none;' href='/paste/view/%s'><div class='smatch'><b>Titel</b>: %s<br/><b>ID</b>: %s<br /><b>Sprache</b>: %s<br /><i>%s</i></div></a><br />" % (match["id"], match[key], match["id"], match["syntaxhighlight"], match['text'][:40])
		return string + "<br /><br />Seiten: <a href='#x_page_back' id='back'>&laquo;</a> %s <a href='#x_page_forward' id='next'>&raquo;</a><input type='hidden' id='pageid' name='pageid' value='%s'>" % (str(int(FormParser.new(request.form).get('page',"0")) + 1), FormParser.new(request.form).get('page','0'))



	
# Database PreConfiguration
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])
	
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('database.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

def query_db(query, args=(), one=False):
	cur = g.db.execute(query, args)
	rv = [dict((cur.description[idx][0], value)
		for idx, value in enumerate(row)) for row in cur.fetchall()]
	return (rv[0] if rv else None) if one else rv



# Secure Database Connection
@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response


			
if __name__ == "__main__":
	# Run Application
	app.secret_key = "]*\xb5\x8f\x1e\xe8\x05N\xd2\xa3\xaf\x94\x98h\x01M"
	try: app.run(debug=False, host="62.141.46.251")
	except: app.run(debug=True)