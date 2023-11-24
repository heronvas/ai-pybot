###from typing import Union
from fastapi import FastAPI, Request, HTTPException
import requests
import json


import os

from dotenv import load_dotenv

load_dotenv()


app = FastAPI()



api_tokens = os.getenv('TOKEN')
 ##api token is used in header to send the reply the user###

my_token = os.getenv('MYTOKEN')### the token whitelisted on the whatsapp dashboard while configuring the API link created after deploying the code 



@app.get("/") 
def read_root():
    return "it is working"


'''once the link is whitelisted it hits a get request on the url configured and 
confirms the subscriptions once the subscription in complete and the sucess response is received it will
execute POST on the same URL for eg:- /webhook with a request containing phone_number_id, name, phone_number of
the recepient and other details refer the payload.jsonl for the same
'''
@app.get("/webhook") 
async def read_messade(request: Request):
    print("mode")
    json_body = await request.json()

    mode = json_body["hub.mode"]
    challenge = json_body["hub.challenge"]
    token = json_body["hub.verify_token"]

    print(mode)


    if(mode == "subscribe" and token == my_token):
        print("sucess")
        return challenge
    else:
        raise HTTPException(status_code=403, detail="Item not found")
    


@app.post("/webhook")
async def write_message(request:Request):
    message_body = await request.json()

    if (message_body["entry"] 
        and message_body["entry"][0]["changes"] 
        and message_body["entry"][0]["changes"][0]["value"]["messages"]
        and message_body["entry"][0]["changes"][0]["value"]["messages"][0]):
            
            phone_no_id = message_body["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
            from_msg = message_body["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            msg = message_body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

            url = "https://graph.facebook.com/v17.0/"+phone_no_id+"/messages"

            payload = json.dumps({
            "messaging_product": "whatsapp",
            "to": from_msg,
            "text": {
                "body": msg,
                
            }
            })
            headers = {
            'Authorization': 'Bearer '+api_tokens,
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)
            
            return response.text
    else:
         raise HTTPException(status_code=403, detail="Item not found")

    

    
    