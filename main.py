import sqlite3

from flask import Flask, render_template, request, make_response, flash, url_for
from pip._vendor import requests
from werkzeug.utils import redirect

from form import AddForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'


def db_connection():
    conn = sqlite3.connect("PhotoCoordinates.db")
    print("Start connection")
    conn.close()


@app.route('/geodata', methods=['GET'])
def get_data_from_api():
    # Take data from API as json and from database
    # Then bind them them in html
    data_api = requests.get('http://localhost:8010/route.json')
    data_api = data_api.json()
    # for x in range(len(data_api['data'])):
    #     print(data_api['data'][x]['properties'])
    #     print(data_api['data'][x]['geometry']['coordinates'])
    data_db, cnt = get_data_from_db()
    # print(data_db)
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
        print(data_db)
    else:
        print("No records in database")
    conn.close()
    return data_db, cnt[0]


@app.route('/geodata/', methods=["GET", "POST"])
# User submit data on a FlaskWTForm
# Check data and then bind them into database
# Inform user if the submition has been corrected or not
def create():
    result = False
    form = AddForm(request.form)
    if form.validate_on_submit():
        flash("Success")
        return redirect(url_for("add.html"))
    if request.method == 'POST':
        try:
            lat_range = range(-90, 90)
            lon_range = range(-180, 180)
            req = request.form
            name = request.form.get("name")
            lat = request.form.get("lat")
            lon = request.form.get("lon")
            if not name or not lat or not abs(float(lat)) < 90:
                return make_response("Bad Request", 400)
            conn = sqlite3.connect("projectdb.db")
            cursor = conn.cursor()
            conn.execute('INSERT INTO PhotosCoordinates (name,lot, lan) VALUES (?,?,?)'
                         , (name, lat, lon))
            conn.commit()
            print("Table created successfully")
            result = True
            return make_response("Created", 201)
        except:
            conn.rollback()
            return make_response("Bad Request", 400)
        finally:
            print("End connection")
            # if (result == True):
            #     return render_template('prompt.html', result=result)
            # else:
            #     return render_template('prompt.html', result=result)

    return render_template('add.html', form=form)


@app.route('/geodata/<id>', methods=['PUT'])
def update(id):
    if request.method == 'PUT':
        # req_Json = request.form.json
        name = request.json.get("name")
        lat = request.json.get("lat")
        lon = request.json.get("lon")
        if not name or not lat or not lon:
            return "Bad request"
        print("Update start")
        print(name)
        try:
            # req = request.form
            # name = request.form.get("name")
            # lat = request.form.get("lat")
            # lon = request.form.get("lon")
            # print(name)
            conn = sqlite3.connect("projectdb.db")
            cursor = conn.cursor()
            print("Update start")
            l = conn.execute('UPDATE PhotosCoordinates SET name=? WHERE id=?', (["nam2", id]))
            conn.commit()
            print("Update successfully")
            print("Table updated successfully")
            return "ok"
        except Exception as e:
            print(e)
            return request("200")
        finally:
            return "something"
            conn.close()

        return render_template('create.html')


@app.route('/geodata/<id>', methods=['DELETE'])
def delete(id):
    #send a delete request
    #Check if the record exists in database
    #Then delete it and return a http response
    if request.method == 'DELETE':
        try:
            name = request.json.get("name")
            coordinates = request.json.get("coordinates")
            conn = sqlite3.connect("projectdb.db")
            cur = conn.cursor()
            print("Connected to sqlite for delete")
            c = cur.execute('SELECT COUNT(*) FROM PhotosCoordinates WHERE id = ?', [id]).rowcount
            c = cur.fetchone()[0]
            cc = cur.execute('SELECT COUNT(*) FROM PhotosCoordinates WHERE (name=? AND lot=? AND lan=?)',
                             (name, coordinates[0], coordinates[1]))
            cc = cc.fetchone()[0]
            if (c or cc) == 0:
                response = make_response("Record not found", 404)
            else:
                conn.execute('DELETE FROM PhotosCoordinates WHERE id=?', ([id]))
                conn.commit()
                conn.close()
                response = make_response("Record deleted", 200)
        except Exception as e:
            print(e)
            response = make_response("Bad request", 400)
        finally:
            return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
