from flask import render_template, jsonify
from flask import request, session
from flask import redirect
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app import app
from app import db
from app.models import Account, Comment, Utilities, Guides

@app.route('/')
def index():
    if "authorize" not in session:
        session["authorize"] = False
    return render_template("index.html")

@app.route('/community')
def community():
    if session["authorize"] != False:
        return render_template("community.html")
    else:
        return redirect("/singup")

@app.route('/utilites')
def utilites():
    return 'Utilites'

@app.route('/utilites/<n>')
def util_spec(n):
    return 'Utilite: %s' %str(n)

@app.route('/site_structure')
def site_structure():
    return render_template("site_structure.html")

@app.route('/guides')
def guides():
    return 'Guides'

@app.route('/guides/<id>')
def guid_spec(id):
    return 'Guide: %s' %id

@app.route('/account')
def account():
    if "authorize" not in session:
        session["authorize"] = False
    if session["authorize"] != False:
        return render_template("account.html")
    else:
        return redirect("/singup")

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = request.json
        if not data:
            return jsonify({"status": False})
        nickname = data.get("nickname")
        passwd = data.get("password")
        get = db.select(Account).where(Account.nickname == nickname)
        account = db.session.execute(get)
        account = account.scalars().first()
        if account == None:
            validate = False
        else:
            validate = check_password_hash(account.hash_passwd, passwd)
        if validate:
            session["nickname"] = account.nickname
            session["authorize"] = True
        return jsonify({"status": validate})
    else:
        return render_template("login.html")

@app.route('/singup', methods=["GET","POST"])
def singup():
    if request.method == "POST":
        data = request.json
        if not data:
            return jsonify({"nickname":False,"email":False})
        n = db.select(Account.nickname)
        e = db.select(Account.email)
        nicks = db.session.execute(n)
        emails = db.session.execute(e)
        nall = nicks.fetchall()
        eall = emails.fetchall()
        nn = data.get("nickname")
        el = data.get("email")
        nick = (nn,) not in nall
        email = (el,) not in eall
        if nick and email:
            pw = data.get("password")
            new_account = Account(nickname = nn,email = el,
            hash_passwd=generate_password_hash(pw))
            db.session.add(new_account)
            db.session.commit()
            session["nickname"] = nn
            session["authorize"] = True
        return jsonify({"nickname":nick,"email":email})
    else:
        return render_template('singup.html')

@app.route('/logout')
def logout():
    session["nickname"] = None
    session["authorize"] = False
    return redirect("/")

@app.route('/help')
def help():
    return 'Help'

#Api

@app.route('/api/commentaries/<tag>')
def api_comment(tag):
    commentw = Comment.query.filter(Comment.tag=="community").all()
    comment = []
    for i in commentw:
        a = {
            "nickname": i.author.nickname,
            "text": i.text,
            "time": i.time.replace(microsecond=0).isoformat() +"Z"
        }
        comment.append(a)
    return jsonify(comment)

@app.route('/api/comentate/<tag>', methods=["POST"])
def api_commentate(tag):
    data = request.json
    author = Account.query.filter(Account.nickname == session["nickname"]).first()
    new = Comment(author_id = author.id,text = data["text"],tag = tag)
    db.session.add(new)
    db.session.commit()
    return "", 200

@app.route('/api/utilities/home')
def api_util_home():
    return jsonify("{'utilities': ['metasploit','nmap']}")

@app.route('/api/utilities/specific/<top>')
def api_util_specific(top):
    return jsonify("{'top':'%s'}"%top)

@app.route('/api/guides/home')
def api_guides_home():
    return jsonify("{'guides': null}")

@app.route('/api/account', methods=["GET","POST"])
def api_account():
    if request.method == "POST":
        return jsonify({"nickname":session["nickname"]})
    else:
        get = db.select(Account).where(Account.nickname == session["nickname"])
        account = db.session.execute(get)
        account = account.scalars().first()
        return jsonify({"nickname": account.nickname,"email": account.email,"comments_count":account.comments.count()})
