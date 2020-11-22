from flask import Flask , render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)