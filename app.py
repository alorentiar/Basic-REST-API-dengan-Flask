#import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS 

#import lib sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import os

#inisiasi object
app = Flask(__name__)

#inisiasi object flask_restful
api = Api(app)

#inisiasi object flask_cors
CORS(app)

#inisiasi object flask sqlalchemy
db = SQLAlchemy(app)

#config database 
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir,"db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# Membuat database model
class ModelDatabase(db.Model):
    #membuat field/kolom
    id = db.Column(db.Integer,primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

#inisiasi variabel kosong bertype dictionary
identitas = {} #global variable, dictionary = json

#create database
db.create_all()


#membuat class Resource 
class ContohResource(Resource):
        #metode get dan post
        def get(self):
            #response = {"msg":"Halo semua, ini ujicoba restful pertamaku"}
            #menampilkan data dari database sqlite
            query = ModelDatabase.query.all()

            #loop pada model database
            identitas = [
                {
                    "nama":data.nama, 
                    "umur":data.umur,
                    "alamat":data.alamat
                } 
                for data in query
            ]

            response    = {
                "Code" : 200,
                "msg"  : "Query data sukses",
                "data" : identitas
            }
            return identitas, 200

        #method mmenyimpan data
        def post(self):
            dataNama = request.form["nama"]
            dataUmur = request.form["umur"]
            dataAlamat = request.form["alamat"]
            
            #masukkan data ke database model
            model = ModelDatabase(nama=dataNama,umur=dataUmur,alamat=dataAlamat)
            model.save()

            response = {
                "msg" : "Data berhasil dimasukkan",
                "code" : 200
            }
            return response
            
#setup resource
api.add_resource(ContohResource,"/api", methods=["GET","POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)

