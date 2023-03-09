#!/usr/bin/python3
import os
import yaml
import subprocess

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.exceptions import HTTPException
from http import HTTPStatus

app = Flask(__name__)
scheduler = BackgroundScheduler()
results = {}

def fetch_tp_result(tp):
    print("Fetch TP results for {0}".format(tp))
    for step in next(iter(tp.values())):
        print ("Init subprocess TP {0}".format(tp))
        res = subprocess.run(['/bin/bash', '-i', '-c', step['test']])
        step['status'] = (res.returncode == 0)
        print("{0}".format(list(tp.keys())[0]) + " - {0}".format(step['name']) + " - Result {0}".format(step['status']))

@app.route('/')
def results():
    response = jsonify(results)
    return response

@app.route("/healthz")
def healthz():
    return "Tutto bene !"


@app.errorhandler(HTTPException)
def handle_internal_server_error(exception: HTTPException):
    app.logger.error("Raised Exception: %s" % exception)
    return exception.description, exception.code


@app.errorhandler(Exception)
def handle_internal_server_error(exception: Exception):
    app.logger.error("Raised Exception: %s" % exception)
    return HTTPStatus.INTERNAL_SERVER_ERROR.description, HTTPStatus.INTERNAL_SERVER_ERROR


if __name__ == '__main__':
    tests_config_file = os.getenv('REPORTING_TESTS_CONFIG_FILE', 'checks.yaml')
    print("Load Tests From {0}".format(tests_config_file))
    with open(tests_config_file) as file:
        results = yaml.safe_load(file)

    scheduler.configure()
    for tp in results:
        print("Add scheduler for TP {0}".format(tp))
        scheduler.add_job(fetch_tp_result, 'interval', seconds=30, args=[tp])
    scheduler.start()
    app.run(port=4000, host='0.0.0.0')
    scheduler.shutdown()
