from . import bp as app

@app.route("/")
def index():
    return "Hi!"