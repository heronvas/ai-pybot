###from typing import Union
from fastapi import FastAPI, Request, HTTPException
import requests
import json
from mangum import Mangum
from openaiconv import speak
import re
import os
import time

from dotenv import load_dotenv

load_dotenv()


app = FastAPI()
handler = Mangum(app)


api_tokens = os.getenv('TOKEN')
 ##api token is used in header to send the reply the user###

my_token = os.getenv('MYTOKEN')### the token whitelisted on the whatsapp dashboard while configuring the API link created after deploying the code 


def clean_response(response):
    
    response = response.replace('\\n', ' ')
    # Remove HTML tags
    
    response = re.sub(r'<[^>]*>', '', response)

    # Remove punctuation
    response = re.sub(r'[^?!\-\+*%$#@\(\)\,.\w\s]', '', response)

    # Remove extra whitespace
    response = re.sub(r'\s+', ' ', response)

    return response


@app.get("/") 
async def read_root():
    return "it is working"


'''once the link is whitelisted it hits a get request on the url configured and 
confirms the subscriptions once the subscription in complete and the sucess response is received it will
execute POST on the same URL for eg:- /webhook with a request containing phone_number_id, name, phone_number of
the recepient and other details refer the payload.jsonl for the same
'''


@app.get("/webhook") 
def read_messade(request: Request):
    # print("mode")
    json_body = request.query_params

    mode = json_body["hub.mode"]
    challenge = json_body["hub.challenge"]
    token = json_body["hub.verify_token"]

    # print(mode)
    # print(token)


    if(mode == "subscribe" and token == my_token):
        print(challenge)
        return int(challenge)
    else:
        raise HTTPException(status_code=403, detail="Item not found")
    


@app.post("/webhook")
async def write_message(request:Request):
    message_body = await request.json()
    
    print(message_body)

    if (message_body["entry"] 
        and message_body["entry"][0]["changes"] 
        and message_body["entry"][0]["changes"][0]["value"]["messages"]
        and message_body["entry"][0]["changes"][0]["value"]["messages"][0]):
            
            phone_no_id = message_body["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
            from_msg = message_body["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            msg = message_body["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

            print("msg  "+msg)
            print("from_msg  "+from_msg)
            print("phone_no_id  "+phone_no_id)

            #start_time = time.perf_counter()
            reply = speak(msg)
            #end_time = time.perf_counter()
            #print("elapsed_time  "+str(end_time-start_time))
            print("normal response "+reply)
            reply = clean_response(reply)
            print("clean response "+reply)

            #print("reply "+reply)
            #print("msg "+msg)

            url = "https://graph.facebook.com/v17.0/"+phone_no_id+"/messages"

            # payload = json.dumps({
            # "messaging_product": "whatsapp",
            # "to": from_msg,
            # "text": {
            #     "body": reply,
                
            # }
            # })
            # headers = {
            # 'Authorization': 'Bearer '+api_tokens,
            # 'Content-Type': 'application/json'
            # }
            #start_time = time.perf_counter()
            response = requests.request("POST", url, 
                                    headers={
                                    'Authorization': 'Bearer '+api_tokens,
                                    'Content-Type': 'application/json'
                                    }, 
                                    data=json.dumps({
                                        "messaging_product": "whatsapp",
                                        "to": from_msg,
                                        "text": {
                                            "body": reply,
                                            
                                        }
                                        }))
            
            #end_time = time.perf_counter()
            #print("elapsed_time  "+str(end_time-start_time))
            print(response.text)
            
            if (response.status_code == 200):
                 return response.text
            else:
                 raise HTTPException(status_code=403, detail=response.text)
                 

            
    else:
         raise HTTPException(status_code=403, detail="Item not found")

    

   
    