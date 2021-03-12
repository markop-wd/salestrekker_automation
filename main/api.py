from flask import Flask, render_template, Response
from flask_restful import Api, Resource, request, reqparse
import requests
from runner import main_runner

app = Flask(__name__)
api = Api(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class Caller(Resource):

    def get(self):
        # print(request)
        req_args = request.args.getlist('ent')
        # req_args.
        # print(req_args)
        # print(req_args['ent'])
        #testolin = main_runner(ent=req_args['ent'])
        # testolin = {"method": req_args['method'], "ent": req_args['ent']}
        return req_args
            # test = {"something": "something1", "something2": req_args['ent']}
            # return render_template("index.html", user_image="test.png", jsonfile=test)

        # if args['method'] == 'login':
        #     return main_runner(ent=args['ent'])


@app.route("/login.html/login-caller")
def test():

    print(request.args)

    print(request.url)
    print(request.path)
    print(request.url_root)
    print(request.full_path)

    # request.
    # info = requests.get(request.url_root + "/login.html/login")
    # print(info.text)
    return render_template("result.html", graph="screenshots/test.png")


@app.route("/index.html")
def index():

    return render_template("index.html")


@app.route("/login.html")
def login():

    return render_template("login.html")


api.add_resource(Caller, "/login.html/login")

if __name__ == "__main__":
    app.run()
