from flask import Flask
app = Flask(__name__)
# import jsonify

@app.route("/api/<request: string>")
def hello(request):
    print(request*3)
    return "Hello World!"
