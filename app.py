from flask import Flask , render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")



@app.route('/about')
def about():
    frompython = "hasnain from python file"
    list = [1,3,4,5]
    return render_template("about.html" , about = frompython , list = list)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)