from flask import Flask, jsonify
from pip._vendor import requests

app = Flask(__name__)
@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"
@app.route('/geodata', methods=['GET'])
def get_data():
    data=requests.get('http://localhost:8010/route.json')
    d=data.json()

    for x in range(len(d['data'])):
        print(d['data'][x]['properties'])
        print(d['data'][x]['geometry']['coordinates'])
    return  d

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)

