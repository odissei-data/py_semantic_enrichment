from flask import Flask, render_template, request, jsonify
from ddigen import ddigenerator
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method != "POST":
        return render_template("xml.html")
    else:
        xml = request.form["xml"]

        return render_template('result.html', result=ddigenerator(xml))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
