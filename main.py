import json

from flask import Flask, jsonify, render_template
from pip._vendor import requests

app = Flask(__name__)


@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return render_template('index.html')


@app.route('/geodata', methods=['GET'])
def get_data():
    data = requests.get('http://localhost:8010/route.json')
    d = data.json()

    for x in range(len(d['data'])):
        print(d['data'][x]['properties'])
        print(d['data'][x]['geometry']['coordinates'])
    return render_template('index.html', d=d, len=len(d['data']))


@app.route('/geodata/', methods=['POST'])
def foo():
    print('post')


@app.route('/geodata', methods=['PUT'])
def foo2():
    print('put')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
