import json

from flask import Flask, request

import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

app.debug = True
BASE_DIR = Path(__file__).resolve().parent


def _save_data_to_file(data):
    now = datetime.now()
    if not os.path.exists(f'{BASE_DIR}/files/'):
        os.makedirs(f'{BASE_DIR}/files/')

    dir_path = f'{BASE_DIR}/files/{now.date().strftime("%m-%d-%Y")}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(f'{dir_path}/{now.hour * 60 * 60 + now.minute * 60 + now.second}.json', 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/save_data/', methods=['POST'])
def save_data():
    data = request.json
    try:
        _save_data_to_file(data)
        return 'Ok'
    except:
        return 'Bad request', 400


if __name__ == "__main__":
    app.run()
