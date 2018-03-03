# from flair_bot import FlairBot as FlairBot 
from flask import Flask, render_template

# set the project root directory as the static folder, you can set others.
app = Flask(__name__)

@app.route("/")
def index():
    # 750 = Number of possible flairs + 1
    listOfFlairNums = [format(x, "04d") for x in range(1, 750)]
    return render_template("index.html", flairlist=listOfFlairNums)

#@app.route("/flairbot")
#def flairbotRoute():
#    print("hello")
#    FlairBot()
#    return "<h1>hi</h1>"

if __name__ == "__main__":
    app.run()