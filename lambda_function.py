import json, ipaddress, boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
table = dynamodb.Table('age_series_stats')


def put_stat(client_ip, uuid, mod_id, avg_sim_performance, game_lang, os_lang):
    data = {}
    data["ip"] = client_ip
    data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["uuid"] = uuid
    data["mod_id"] = mod_id
    data["avg_sim_performance"] = avg_sim_performance
    data["game_lang"] = game_lang
    data["os_lang"] = os_lang
    
    table.put_item(Item=data)


def lambda_handler(event, context):
    # print(json.dumps(event))

    http_type = event["requestContext"]["http"]["method"]
    source_ip = event["requestContext"]["http"]["sourceIp"]
    
    try:
        if (http_type == "POST"):
            if ("body" in event):
                body = json.loads(event["body"])
                
                uuid = ""
                if ("uuid" in body):
                    uuid = body["uuid"]
                
                mod_id = ""
                if ("mod_id" in body):
                    mod_id = body["mod_id"]
                
                avg_sim_performance = ""
                if ("avg_sim_performance" in body):
                    avg_sim_performance = body["avg_sim_performance"]
                    
                game_lang = ""
                if ("game_lang" in body):
                    game_lang = body["game_lang"]
                    
                os_lang = ""
                if ("os_lang" in body):
                    os_lang = body["os_lang"]
                
                print("Sending stat to DynamoDB...")
                put_stat(source_ip, uuid, mod_id, avg_sim_performance, game_lang, os_lang)
    except Exception:
        pass # Don't pass exceptions, just return 200 all the time.
        
    
    # Generic response
    message = "Age Series Stats API"
    code = 200
    
    response = {
        "isBase64Encoded": False,
        "statusCode": code,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET'
        },
        "body": message
    }
    
    return response
