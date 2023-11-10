import azure.functions as func
import logging

from db import File,Strtype,select_file,insert_file,delete_file
import blob
from flask import Flask, request, redirect
from flask import render_template
#app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
flask_app = Flask(__name__)
app = func.WsgiFunctionApp(app=flask_app.wsgi_app,http_auth_level=func.AuthLevel.ANONYMOUS)

@flask_app.route("/hello")
def hello():
    return "Hello. This HTTP triggered function executed successfully."

# #@app.route(route="pastebin")
# def main(req: func.HttpRequest,context: func.Context) -> func.HttpResponse:
#     return func.WsgiMiddleware(Flask.wsgi_app).handle(req,context)
#     logging.info('Python HTTP trigger function processed a request.')

@flask_app.route("/")
def index():
    return render_template("index.html",files=select_file(10))

@flask_app.route("/upload", methods = ["POST"]) 
def upload():
    file = request.files.get("file")
    file.con
    url  = blob.upload(file.filename,file)
    #print(type(file))
    sqlfile = File(name=file.filename[:10],type = Strtype.url ,value=url)
    insert_file(sqlfile)
    return redirect("/")

@flask_app.route("/text", methods = ["POST"])
def text():
    text = request.form.get("text")
    file = File(name=text[:10],type = Strtype.plain ,value=text)
    insert_file(file)
    return redirect("/")

@flask_app.route("/delete/<int:id>")
def delete(id:int):
    #file = File(id=id)
    # we current do not delete file in blob , only row in mysql is deleted
    delete_file(id)
    return redirect("/")

