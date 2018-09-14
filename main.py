import hashlib
import base64
import json
from flask import jsonify
import requests
from requests_futures.sessions import FuturesSession
from lib import get_name

def collect_requests(request):
    name = get_name.name()
    payload = {'name': name}
    result_one = requests.post('https://us-central1-dave-173321.cloudfunctions.net/req_one', json=payload)
    result_two = requests.post('https://us-central1-dave-173321.cloudfunctions.net/req_two', json=payload)
    response = {
        'name': name,
        'sha256': result_one.json()['hash256'],
        'md5': result_two.json()['hashmd5']
    }
    return jsonify(response)

def collect_requests_async(request):
    name = 'george'
    payload = {'name': name}
    session = FuturesSession()
    future_one = session.post('https://us-central1-dave-173321.cloudfunctions.net/req_one', json=payload)
    future_two = session.post('https://us-central1-dave-173321.cloudfunctions.net/req_two', json=payload)
    result_one = future_one.result()
    result_two = future_two.result()
    response = {
        'name': name,
        'sha256': result_one.json()['hash256'],
        'md5': result_two.json()['hashmd5']
    }
    print(response)
    return jsonify(response)


def req_one(request):
    name = request.get_json()['name'].encode('utf-8')
    name_hash = hashlib.sha256(name).hexdigest()
    return jsonify(hash256=name_hash)

def req_two(request):
    name = request.get_json()['name'].encode('utf-8')
    name_hash = hashlib.md5(name).hexdigest()
    return jsonify(hashmd5=name_hash)
