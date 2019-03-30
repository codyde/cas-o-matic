from gevent import monkey
monkey.patch_all()
from app.imports import get_item, get_user_org, delete_item, create_item, invite_user
from app.imports import setup_org, cleanuptoken, force_delete, getorginfo, getspcorgs, orgstats
from app.imports import deletion_block, forceclean
from app.caspyr import Project, Request, Deployment, Blueprint, Machine
from app.caspyr import NetworkProfile, StorageProfileAWS, StorageProfileAzure, StorageProfile
from app.caspyr import CloudZone, ImageMapping, FlavorMapping
from app.caspyr import CloudAccountAws, CloudAccountAzure, CloudAccount
from app.caspyr import Session, User, Region
from threading import Thread
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask.logging import create_logger
import json
import requests
from flask import Flask, jsonify, request
import boto3
import os
import time

app = Flask(__name__)
LOG = create_logger(app)

app.secret_key = "super secret key"
socketio = SocketIO(app)
CORS(app)
thread = None

secrets = {
        "AWS_ACCESS_KEY_ID": os.environ['AWS_ACCESS_KEY_ID'],
        "AWS_SECRET_ACCESS_KEY": os.environ['AWS_SECRET_ACCESS_KEY']
    }

"""
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
"""
my_west = boto3.Session(aws_access_key_id=secrets['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=secrets['AWS_SECRET_ACCESS_KEY'],
                        region_name='us-west-1')
dynamodb = my_west.resource('dynamodb')
table = dynamodb.Table('cas-spc')

@app.route("/api")
def default_route():
    LOG.debug('this is a DEBUG message')
    LOG.info('this is an INFO message')
    LOG.warning('this is a WARNING message')
    LOG.error('this is an ERROR message')
    LOG.critical('this is a CRITICAL message')
    return jsonify('hello world')

@app.route("/api/createorg", methods=["POST"])
def create_org():
    req = request.get_json()
    _account = req['account']
    org = get_item(table,'False')
    token = org['apikey']
    orgId = org['orgid']
    name = org['spcorg']
    use = org['inuse']
    data = {}
    data['aws_access_key'] = org['aws_access_key']
    data['aws_secret_key'] = org['aws_secret_key']
    data['azure_application_id'] = org['azure_application_id']
    data['azure_application_key'] = org['azure_application_key']
    data['azure_tenant_id'] = org['azure_tenant_id']
    data['azure_subscription_id'] = org['azure_subscription_id']
    obj = table.get_item(
        Key={
            'spcorg': name,
            'apikey': token
        }
    )
    item = obj['Item']
    delete_item(table,name,token)
    x = create_item(table,
                    name,
                    orgId,
                    token,
                    data['aws_access_key'],
                    data['aws_secret_key'],
                    data['azure_application_id'],
                    data['azure_application_key'],
                    data['azure_tenant_id'],
                    data['azure_subscription_id'],
                    'True',
                    _account)
    session = Session.login(token)
    invite_user(session, _account, token, orgId)
    setup_org(session, data)
    orgdata = {}
    orgdata['account'] = _account
    orgdata['orgname'] = name
    orgdata['apikey'] = token
    return jsonify(orgdata)


@app.route("/api/deleteorg", methods=["POST"])
def delete_org():
    req = request.get_json()
    _account = req['account']
    u = get_user_org(table,_account)
    session = Session.login(u['apikey'])
    org = u['spcorg']
    try:
        User.remove(session = session,
                            id = u['orgid'],
                            username = _account)
        print("User Removed")
    except:
        print("User not found in org or error has occurred...moving on")
        delete_item(table,u['spcorg'],u['apikey'])
        create_item(table,spc_org = u['spcorg'],
                org_id = u['orgid'],
                api_key = u['apikey'],
                aws_access_key = u['aws_access_key'],
                aws_secret_key = u['aws_secret_key'],
                azure_application_id = u['azure_application_id'],
                azure_application_key = u['azure_application_key'],
                azure_tenant_id = u['azure_tenant_id'],
                azure_subscription_id = u['azure_subscription_id'],
                in_use = 'False',
                username = 'None')
    delete_item(table,u['spcorg'],'True')
    create_item(table,spc_org = u['spcorg'],
                org_id = u['orgid'],
                api_key = u['apikey'],
                aws_access_key = u['aws_access_key'],
                aws_secret_key = u['aws_secret_key'],
                azure_application_id = u['azure_application_id'],
                azure_application_key = u['azure_application_key'],
                azure_tenant_id = u['azure_tenant_id'],
                azure_subscription_id = u['azure_subscription_id'],
                in_use = 'False',
                username = 'None')
    try:
        cancel_active_requests(session)
        print("Cancelled Active Requests")
        delete_deployments(session)
        print("Deployments Removed")
    except:
        print(f'Found {len(Deployment.list(session))} Deployments to Remove')
        for i in Deployment.list(session):
            Deployment.force_delete(session, i['id'])
        print("All Deployments Force Deleted")
    x = deletion_block(session)
    return jsonify(x)

@app.route("/api/orgs", methods=["GET"])
def get_orgs():
    response = table.scan()['Items']
    return jsonify(response)

@app.route('/api/cleanorg', methods=['DELETE'])
def delete_org_by_id():
    req = request.get_json()
    _token = req['cspapitoken']
    session = Session.login(_token)
    x = cleanuptoken(session)
    return jsonify(x)

@app.route('/api/orphancleanup', methods=['DELETE'])
def cleanup_orphans():
    req = request.get_json()
    _token = req['cspapitoken']
    session = Session.login(_token)
    x = forceclean(session, _token)
    return jsonify(x)

@app.route('/api/spcorgs')
def get_spc_orgs_dynamo():
    details = getspcorgs(table)
    data = []
    for i in details:
        jsonObj = {}
        jsonObj['spcorg'] = i['spcorg']
        jsonObj['Username'] = i['username']
        jsonObj['inuse'] = i['inuse']
        jsonObj['orgid'] = i['orgid']
        jsonObj['apikey'] = i['apikey']
        data.append(jsonObj)
    return jsonify(data)

@app.route('/api/orgstats', methods=["POST"])
def get_org_stats():
    req = request.get_json()
    _token = req['apikey']
    data = orgstats(_token)
    return jsonify(data)

@app.route("/api/health", methods=["GET"])
def get_health():
    stats = "{'status':'completed','platform':'healthy'}"
    return jsonify(stats)

@socketio.on('my event')
def handle_event(data):
    print('received')
    return jsonify(data)


@socketio.on('connected')
def handle_connect():
    while True:
        socketio.sleep(3)
        print('connected')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
