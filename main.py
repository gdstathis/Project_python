import sqlite3
import server
from flask import Flask, render_template, request, json
from pip._vendor import requests

from form import AddForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'


def db_connection():
    conn = sqlite3.connect("PhotoCoordinates.db")
    print("Start connection")
    conn.close()


@app.route('/geodata', methods=['GET'])
def get_data_from_api():
    #Take data from API as json and from database
    #Then bind them them in html
    data_api = requests.get('http://localhost:8010/route.json')
    data_api = data_api.json()
    # for x in range(len(data_api['data'])):
    #     print(data_api['data'][x]['properties'])
    #     print(data_api['data'][x]['geometry']['coordinates'])
    data_db, cnt = get_data_from_db()
    print(data_db)
    return render_template('alldata.html',
                           data_api=data_api, lenapi=len(data_api['data']),
                           lendb=cnt, data_db=data_db)


def get_data_from_db():
    #Select all data from database if table is not empty
    #Return data and count of them
    conn = sqlite3.connect("projectdb.db")
    print("Start connection with database")
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM PhotosCoordinates")
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
#User submit data on a FlaskWTForm
#Check data and then bind them into database
#Inform user if the submition has been corrected or not
def create():
    result=False
    form=AddForm(request.form)
    if request.method == "POST" :
        try:
            req = request.form
            name = request.form.get("name")
            lat = request.form.get("lat")
            lon = request.form.get("lon")
            if not name or not lat or not lon:
                return "BadRequest"
            conn = sqlite3.connect("projectdb.db")
            cursor = conn.cursor()
            l = conn.execute('INSERT INTO PhotosCoordinates (name,lot,lan) VALUES (?,?,?)', (name, lat, lon))
            conn.commit()
            print("Table created successfully")
            result=True
            return "ok"
        except:
            conn.rollback()
            return "Bad request"
        finally:
            print("End connection")
            if (result==True):
                return render_template('prompt.html',result=result)
            else:
                return render_template('prompt.html',result=result)

    return render_template('add.html',form=form)


@app.route('/geodata/<id>', methods=['PUT'])
def update(id):
    if request.method == 'PUT':
        # req_Json = request.form.json
        name = request.json.get("name")
        lat = request.json.get("lat")
        lon = request.json.get("lon")
        if not name or not lat  or not lon:
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
            l = conn.execute('UPDATE PhotosCoordinates SET name=? WHERE id=2', (["nam2"]))
            conn.commit()
            print("Update successfully")
            print("Table created successfully")
            return "ok"
        except Exception as e:
            print(e)
            return "problem"
        finally:
            return "sdasdas"
            conn.close()

        return render_template('create.html')

@app.route('/geodata/<id>', methods=['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        conn = sqlite3.connect("projectdb.db")
        cur = conn.cursor()
        print("Connected to sqlite for delete")
        cur.execute('DELETE FROM PhotosCoordinates WHERE id = ?', [id])
        conn.commit()
        conn.close()
        return "Ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
