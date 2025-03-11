from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_db, register_user, login_user, save_paper, get_papers

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.secret_key = "your_secret_key"  # Required for session management

# Initialize Database
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if register_user(username, password):
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        else:
            flash("Username already exists. Try a different one.", "danger")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if login_user(username, password):
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("research_list"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        abstract = request.form["abstract"]
        username = session["user"]
        
        save_paper(username, title, author, abstract)
        flash("Research paper uploaded successfully!", "success")
        return redirect(url_for("research_list"))

    return render_template("upload.html")

@app.route("/research_list")
def research_list():
    if "user" not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for("login"))

    username = session["user"]
    papers = get_papers(username)
    
    return render_template("research_list.html", papers=papers)

if __name__ == "__main__":
    app.run(debug=True)
