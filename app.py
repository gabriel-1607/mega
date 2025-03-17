from flask import Flask, render_template, redirect, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
import mysql.connector
import openai

# Initialize Flask app
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mydb = mysql.connector.connect(
    host="gabriel1607.mysql.pythonanywhere-services.com",
    user="gabriel1607",
    password="caquitA2",
    database="gabriel1607$default"
)
db = mydb.cursor()

@app.route("/")
def index():
    return render_template("index.html")

# Login route
@app.route("/login", methods=["POST", "GET"])
def login():

    session.clear()

    if request.method == "POST":
        if request.form.get("username") and request.form.get("password"):
            db.execute("SELECT password from users WHERE username = %s", [request.form.get("username")])
            password = db.fetchall()
            if password and check_password_hash(password, request.form.get("password")):
                db.execute("SELECT id from users WHERE username = %s", [request.form.get("username")])
                id = db.fetchall()
                session["user_id"] = id[0][0]
            else:
                # Return and display error message in html
                return render_template("login.html", message="Wrong password")
        else:
            # Return and display error message in html
            return render_template("login.html", message="Type in all necessary information, please")
    return render_template("login.html")

# Register route
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if request.form.get("username") and request.form.get("email") and request.form.get("password"):
            db.execute("SELECT username from users WHERE username = %s", [request.form.get("username")])
            user = db.fetchall()
            if user[0][0] == request.form.get("username"):
                # Return and display error message in html
                return render_template("register.html", message="Username already exists")
            db.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", [request.form.get("username"), request.form.get("email"), generate_password_hash(request.form.get("password"))])
            mydb.commit()
        else:
            # Return and display error message in html
            return render_template("register.html", message="Type in all necessary information, please")
    return render_template("register.html")

@app.route('/interpret_skills', methods=['POST'])
def interpret_skills():
    user_input = request.form['user_input']

    # Prepare the prompt to ask ChatGPT to interpret the skills mentioned by the user
    prompt = f"Extract the skills from the following description:\n\n{user_input}\n\nList the skills:"

    try:
        # Request to OpenAI API to get the response from GPT-3.5 or GPT-4
        response = openai.Completion.create(
            model="text-davinci-003",  # You can use GPT-4 if available
            prompt=prompt,
            max_tokens=150,
            temperature=0.5
        )

        # Extract the list of skills from the response
        skills = response.choices[0].text.strip()

        return jsonify({'skills': skills})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)