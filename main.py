import os
import sqlite3
from subprocess import Popen

import server
from flask import Flask, render_template, request, make_response
from flask_bootstrap import Bootstrap
from pip._vendor import requests

from form import AppForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
Bootstrap(app)
#Run the file server.py
Popen('python server.py')

"""
In this project implement endpoints for POST,GET,PUT,DELETE requests
I created the database using SQLite DB Browser
I used POSTMAN for testing the results of requests
lon -> Longitude between -180 and 180
lat -> Latitude between -90 and 90
These variables have same names in database too.
"""


@app.route('/geodata', methods=['GET'])
def get_data_from_api():
    # Takes data from API as json and
    # Takes data from database
    # Then binds them in html and displays them in a table
    data_api = requests.get('http://localhost:8010/route.json')
    data_api = data_api.json()
    data_db, cnt = get_data_from_db()
    return render_template('alldata.html',
                           data_api=data_api, lenapi=len(data_api['data']),
                           lendb=cnt, data_db=data_db)


def get_data_from_db():
    # Select all data from database if table is not empty
    # Return data and count of them
    conn = sqlite3.connect("projectdb.db")
    print("Start connection with database")
    cursor = conn.cursor()
    x = cursor.execute("SELECT count(*) FROM PhotosCoordinates")
    cnt = cursor.fetchall()[0]
    if (cnt[0] > 0):
        k = conn.execute('SELECT * FROM PhotosCoordinates')
        data_db = k.fetchall()
        make_response("OK",200)
    else:
        make_response("No records in database",404)
    conn.close()
    return data_db, cnt[0]


@app.route('/geodata/', methods=['GET', 'POST'])
def create():
    # User submit data on a FlaskWTForm
    # Check data and if they are correct, save them into database
    # Inform user if the submission has been corrected or not
    form = AppForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            name = request.form.get("name")
            lat = request.form.get("lat")
            lon = request.form.get("lon")
            if not name or not lat or not abs(float(lat)) <= 90 or not abs(float(lon)) <= 180:
                return make_response(render_template('form.html', form=form, suc=0,add=1), 400)
            conn = sqlite3.connect("projectdb.db")
            conn.execute('INSERT INTO PhotosCoordinates (name,lon, lat) VALUES (?,?,?)'
                         , (name, lon, lat))
            conn.commit()
            print("Record created successfully")
            return make_response(render_template('form.html', form=form, suc=1,add=1), 201)
        except:
            conn.rollback()
            return make_response(render_template('form.html', form=form, suc=0,add=0), 400)
        finally:
            print("End connection")

    return render_template('form.html', form=form, suc=None,add=1)


@app.route('/geodata/<id>', methods=['PUT', 'GET','POST'])
def update(id):
    #In this function I use POST method to update a record in database
    #Because the form is the same with post form, applies the same validations
    #Get data from the form, searches if the record exists and then
    #updates the record
    #Return response if record has been updated or not
    form = AppForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form.get("name")
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        print("Update start")
        try:
            conn = sqlite3.connect("projectdb.db")
            cur = conn.cursor()
            print("Connected to sqlite for update")
            c = cur.execute('SELECT COUNT(*) FROM PhotosCoordinates WHERE id = ?',
                            [id]).rowcount
            c = cur.fetchone()[0]
            if (c == 0):
                return make_response(render_template('form.html', form=form,f=0,suc2=0),404)
            print("Update start")
            l = conn.execute('UPDATE PhotosCoordinates SET name=? , lat=?, lon=? WHERE id=?',
                             ([name, lat, lon, id]))
            conn.commit()
            print("Update successfully")
            print("Table updated successfully")
            return make_response(render_template('form.html', form=form, suc2=1), 200)
        except Exception as e:
            print(e)
            return make_response(render_template('form.html', form=form, f=0), 400)
        finally:
            conn.close()
    return render_template('form.html', form=form, suc2=None, id=id)


# @app.route('/geodata/<id>', methods=['PUT'])
# def update(id):
#     #In this function I use PUT method to update
#     #a record in database.
#     #Take data as json from a PUT request
#     #Search if exists record with this id
#     #If record exists, does the update
#     #Else return a response of bad Request or Not Found
#     if request.method == 'PUT':
#         # req_Json = request.form.json
#         name = request.json.get("name")
#         lat = request.json.get("coordinates")[0]
#         lon = request.json.get("coordinates")[1]
#         if not name or not lat or not lon:
#             res= make_response("Bad request",400)
#         print("Update start")
#         try:
#             conn = sqlite3.connect("projectdb.db")
#             cur = conn.cursor()
#             print("Connected to sqlite for delete")
#             c = cur.execute('SELECT COUNT(*) FROM PhotosCoordinates WHERE id = ?',
#                             [id]).rowcount
#             c = cur.fetchone()[0]
#             if (c==0):
#                 return make_response("Not Found",404)
#             print("Update start")
#             l = conn.execute('UPDATE PhotosCoordinates SET name=? , lot=?, lan=? '
#                              'WHERE id=?', ([name,lat,lon,id]))
#             conn.commit()
#             print("Update successfully")
#             print("Table updated successfully")
#             return make_response("OK",200)
#         except Exception as e:
#             print(e)
#             return make_response("Bad request",400)
#         finally:
#             conn.close()
#         return make_response("OK",200)


@app.route('/geodata/<id>', methods=['DELETE'])
def delete(id):
    # Send a delete request
    # Check if the record exists in database
    # Then delete it and return a http response
    # For delete is necessary at least one of these: id, name, lat or lon
    if request.method == 'DELETE':
        try:
            name = request.json.get("name")
            coordinates = request.json.get("coordinates")
            conn = sqlite3.connect("projectdb.db")
            print("Connected to sqlite for delete")
            cur = conn.cursor()
            c = cur.execute('SELECT COUNT(*) FROM PhotosCoordinates WHERE id = ?'
                            , ([id])).rowcount
            c = cur.fetchone()[0]

            cc = cur.execute('SELECT COUNT(*) FROM PhotosCoordinates WHERE (name=? OR lon=? OR lat=?)'
                             ,([name, coordinates[0], coordinates[1]]))
            cc = cur.fetchone()[0]
            print(c,cc)
            if c == 0 or cc==0:
                return make_response("Record not found", 404)
            else:
                conn.execute('DELETE FROM PhotosCoordinates WHERE id=?', ([id]))
                conn.commit()
                conn.close()
                return make_response("Record deleted", 200)
        except Exception as e:
            print(e)
            return make_response("Bad request", 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
