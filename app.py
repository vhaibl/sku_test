import time
from typing import Optional

from flask import Flask, jsonify, request


app = Flask(__name__)


def get_line():
    with open('recommends.csv', 'rb') as in_f:
        for line in in_f:
            yield line


def filter_result(grade, results, sku, temp):
    for line in temp:
        if sku in line[:line.find(b',', 9, 11)]:
            if not grade:
                results.append((line.decode()).split(','))
            else:
                decoded_line = (line.decode()).split(',')
                if float(decoded_line[2]) <= grade:
                    results.append(decoded_line)


@app.route('/gen', methods=["GET"])
def gen():
    results = []
    temp = []
    response = []

    sku = request.args.get('sku')
    grade: Optional[float] = request.args.get('grade', type=float)
    if not sku:
        return jsonify({'error': 'No SKU provided'}), 400
    sku = sku.encode()
    started_at = time.time()

    iter_line = iter(get_line())
    for line in iter_line:
        if sku[0] == line[0]:
            temp.append(line)

    filter_result(grade, results, sku, temp)
    ended_at = time.time()
    elapsed = round(ended_at - started_at, 2)
    print(f'Calculating time: {elapsed}')

    for sku in results:
        response.append({'sku': sku[1], 'grade': str(sku[2].replace('\n', ''))})

    return jsonify(response), 200


@app.route('/simple', methods=["GET"])
def simple():
    results = []
    temp = []
    response = []

    sku = request.args.get('sku')
    grade: Optional[float] = request.args.get('grade', type=float)
    if not sku:
        return jsonify({'error': 'No SKU provided'}), 400

    sku = sku.encode()
    started_at = time.time()

    with open('recommends.csv', 'rb') as in_f:
        for line in in_f:
            if sku[0] == line[0]:
                temp.append(line)

    filter_result(grade, results, sku, temp)

    ended_at = time.time()
    elapsed = round(ended_at - started_at, 2)
    print(f'Calculating time: {elapsed}')

    for sku in results:
        response.append({'sku': sku[1], 'grade': str(sku[2].replace('\n', ''))})

    return jsonify(response), 200


if __name__ == '__main__':
    app.run()
