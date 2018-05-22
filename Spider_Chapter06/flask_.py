from flask import Flask
app=Flask(__name__)

'''
@app.route("/blog/<int:postID>")
def show_int(postID):
    return "blog number %d" % postID


@app.route("/blog/<float:float_id>")
def show_float(float_id):
    return "float %f" % float_id
'''

@app.route("/flask")
def hello():
    return "Hello World"


@app.route("/python/")
def world():
    return "World"

if __name__ == "__main__":
    json = {"lll":"fff"}
    for j in json:
        print("{}_cookies".format(j))