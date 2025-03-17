from flask import Flask, render_template
import openai
import mysql.connector

# Initialize Flask app
app = Flask(__name__)

# Conexión con la base de datos MySQL
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

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/", methods=["POST", "GET"])
def register():
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST", "GET"])
def register():
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