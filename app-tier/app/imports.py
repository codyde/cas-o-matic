from app.caspyr import Project, Request, Deployment, Blueprint, Machine
from app.caspyr import NetworkProfile, StorageProfileAWS, StorageProfileAzure, StorageProfile
from app.caspyr import CloudZone, ImageMapping, FlavorMapping
from app.caspyr import CloudAccountAws, CloudAccountAzure, CloudAccount
from app.caspyr import Session, User, Region
import time
import os

def delete_deployments(session):
    if len(Deployment.list(session)) > 0:
        for i in Deployment.list(session):
            Deployment.delete(session, i['id'])
        return

def force_delete(session):
    if len(Deployment.list(session)) > 0:
        for i in Deployment.list(session):
            Deployment.force_delete(session, i['id'])
        return

def machine_clean(session):
    if len(Machine.list(session)) > 0:
        for i in Machine.list(session):
            Machine.delete(session, i['id'])
    return

def machine_force(session, apikey):
    if len(Machine.list_orphaned(session)) > 0:
        for i in Machine.list_orphaned(session):
            Machine.unregister(session, i)
    return

def remove_user(session, org, username):
            User.remove(session,
                        id=org,
                        username=username)

def cancel_active_requests(session):
    while len(Request.list_incomplete(session)) > 0:
        for i in Request.list_incomplete(session):
            Request.cancel(session, i['id'])
            time.sleep(10)
        return

def delete_blueprints(session):
    while len(Blueprint.list(session)) > 0:
        for i in Blueprint.list(session):
            Blueprint.delete(session, i['id'])
        return

def delete_image_mappings(session):
    while len(ImageMapping.list(session)) > 0:
        for i in ImageMapping.list(session):
            ImageMapping.delete(session, i['id'])
        return

def delete_flavor_mapping(session):
    while len(FlavorMapping.list(session)) > 0:
        for i in FlavorMapping.list(session):
            FlavorMapping.delete(session, i['id'])
        return

def delete_storage_profile(session):
    while len(StorageProfile.list(session)) > 0:
        for i in StorageProfile.list(session):
            StorageProfile.delete(session, i['id'])
        return

def delete_network_profile(session):
    while len(NetworkProfile.list(session)) > 0:
        for i in NetworkProfile.list(session):
            NetworkProfile.delete(session, i['id'])
        return

def delete_orphaned_machines(session):
    for i in Machine.list_orphaned(session):
        Machine.unregister(session, i)
        time.sleep(15)
    return

def delete_project(session):
    while len(Project.list(session)) > 0:
        for i in Project.list(session):
            Project.removezones(session, i['id'])
            time.sleep(5)
            Project.delete(session, i['id'])
    return

def delete_cloudzones(session):
    while len(CloudZone.list(session)) > 0:
        for i in CloudZone.list(session):
            CloudZone.delete(session, i['id'])
    return

def delete_cloudaccounts(session):
    while len(CloudAccount.list(session)) > 0:
        for i in CloudAccount.list(session):
            CloudAccount.unregister(session, i['id'])
            CloudAccount.delete(session, i['id'])
    return

def cleanup(session, org, username):
    remove_user(session, org, username)
    cancel_active_requests(session)
    delete_deployments(session)
    delete_blueprints(session)
    delete_image_mappings(session)
    delete_flavor_mapping(session)
    delete_network_profile(session)
    delete_storage_profile(session)
    delete_project(session)
    delete_cloudzones(session)
    delete_cloudaccounts(session)
    info = ""
    info +=(f'*Cleanup on test org completed.* \n')
    info +=(f'{len(Deployment.list(session))} deployments remaining. \n')
    info +=(f'{len(Blueprint.list(session))} blueprints remaining. \n')
    info +=(f'{len(ImageMapping.list(session))} image mappings remaining. \n')
    info +=(f'{len(FlavorMapping.list(session))} flavor mappings remaining. \n')
    info +=(f'{len(StorageProfile.list(session))} storage profiles remaining. \n')
    info +=(f'{len(Project.list(session))} projects remaining. \n')
    info +=(f'{len(CloudZone.list(session))} cloud zones remaining. \n')
    info +=(f'{len(CloudAccount.list(session))} cloud accounts remaining. \n')
    info +=(f'User {username} removed.')
    text = { "text": info }
    return text


def invite_user(session,
                user,
                api_token,
                org_id,
                cloud_assembly=True,
                code_stream=True,
                service_broker=True,
                log_intelligence=False):
    User.invite(session,
                id=org_id,
                usernames=[user],
                cloud_assembly=cloud_assembly,
                code_stream=code_stream,
                service_broker=service_broker,
                log_intelligence=log_intelligence)


def setup_org(session, data):
    i = CloudAccountAws.create(session,
                               name='AWS SPC',
                               access_key=data['aws_access_key'],
                               secret_key=data['aws_secret_key']
                               )
    CloudZone.create(session,
                     name='AWS SPC',
                     region_id=os.path.split(
                         i._links['regions']['hrefs'][0])[1],
                     tags=[{"key": "platform", "value": "aws"}]
                     )

    i = CloudAccountAzure.create(session,
                                 name='Azure SPC',
                                 subscription_id=data['azure_subscription_id'],
                                 tenant_id=data['azure_tenant_id'],
                                 application_id=data['azure_application_id'],
                                 application_key=data['azure_application_key']
                                 )
    CloudZone.create(session,
                     name='AWS SPC',
                     region_id=os.path.split(
                         i._links['regions']['hrefs'][0])[1],
                     tags=[{"key": "platform", "value": "azure"}]
                     )

def get_user_org(table,username):
        response = table.scan()['Items']
        availorg = []
        for i in response:
            if i['username'] == username:
                availorg.append(i)
                break
        item = availorg[0]
        print(item)
        return item

def get_item(table,status):
    response = table.scan()['Items']
    availorg = []
    for i in response:
        if i['inuse'] == status:
            availorg.append(i)
    item = availorg[0]
    print(item)
    return item


def delete_item(table, org_name, token):
    response = table.delete_item(
        Key={
            'spcorg': org_name,
            'apikey': token
        }
    )
    return response

def create_item(table,spc_org,org_id,api_key,aws_access_key,aws_secret_key,azure_application_id,azure_application_key,azure_tenant_id,azure_subscription_id,in_use,username):
    table.put_item(
        Item={
            'spcorg': spc_org,
            'orgid': org_id,
            'apikey': api_key,
            'aws_access_key': aws_access_key,
            'aws_secret_key': aws_secret_key,
            'azure_application_id': azure_application_id,
            'azure_application_key': azure_application_key,
            'azure_tenant_id': azure_tenant_id,
            'azure_subscription_id': azure_subscription_id,
            'inuse': in_use,
            'username': username
        }
    )
    status = table.creation_date_time
    print(status)
    return status

def deletion_block(session):
    try:
        bps = len(Blueprint.list(session))
        delete_blueprints(session)
        print(f"{bps} Blueprints Deleted")
        delete_image_mappings(session)
        print("Image Mappings Deleted")
        delete_flavor_mapping(session)
        print("Flavor Mappings Deleted")
        delete_network_profile(session)
        print("Network Profiles Deleted")
        delete_storage_profile(session)
        print("Storage Profile Deleted")
        delete_project(session)
        print("Projects Removed")
        zones = len(CloudZone.list(session))
        delete_cloudzones(session)
        print(f"{zones} Cloud Zones Cleaned")
        delete_cloudaccounts(session)
        print(f" Removed {zones} Cloud Zones")
        data = {}
        data['Deployments Removed'] = len(Deployment.list(session))
        data['Blueprints Removed'] = len(Blueprint.list(session))  
        data['Image Mappings Removed'] = len(ImageMapping.list(session))
        data['Flavor Mappings Removed'] = len(FlavorMapping.list(session))
        data['Storage Profile Removed'] = len(StorageProfile.list(session))
        data['Projects Removed'] = len(Project.list(session))
        data['Cloud Zones Cleaned'] = len(CloudZone.list(session))
        data['Cloud Accounts Removed'] = len(CloudAccount.list(session))
    except:
        data = {"status":"failed"}
    return data

def cleanuptoken(session):
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
    data = deletion_block(session)
    return data

def forceclean(session, _token):
    delete_deployments(session)
    print("Removed Deployments")
    force_delete(session)
    print("Force Deleted Leftovers")
    machine_clean(session)
    print("Deleted Machines")
    machine_force(session, _token)
    x = deletion_block(session)
    return x

def getorginfo(session):
    cloudaccounts = len(CloudAccount.list(session))
    projects = len(Project.list(session))
    bps = len(Blueprint.list(session))
    deployments = len(Deployment.list(session))
    serialData = {}
    serialData['cloudaccounts'] = cloudaccounts
    serialData['projects'] = projects
    serialData['bps'] = bps
    serialData['deployments'] = deployments
    return serialData

def orgstats(token):
    session = Session.login(token)
    orgStats = {}
    orgStats['blueprints'] = len(Blueprint.list(session))
    orgStats['cloudaccounts'] = len(CloudAccount.list(session))
    orgStats['cloudzones'] = len(CloudZone.list(session))
    orgStats['deployments'] = len(Deployment.list(session))
    return orgStats


def getspcorgs(table):
    response = table.scan()['Items']
    return response