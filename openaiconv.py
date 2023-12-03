#event.get('queryStringParameters', {}).get('key1', None)       "get request"
#event.get('key1')                                             "post request"
import json
import openai


###def lambda_handler(event, context):
def speak(name):
    ##event_data = event.get('queryStringParameters', {}).get('key1', None)
    openai.api_key = "XzuN75mVA3xxtfAS3sXF8Lg6E8ZlqWUA"
    openai.api_base = "https://api.deepinfra.com/v1/openai"
    
    print([{'role': 'user', 'content' : name}])

    response = openai.ChatCompletion.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        messages=[{'role': 'user', 'content' : name}],
        #prompt=name,
        #prompt = 'explain credit card',
        temperature = 1,
        max_tokens = 200 
    )

    #print("see "+json.dumps(response.choices[0].message['content']))

    if response:
        return json.dumps(response.choices[0].message['content'])
    else:
        return "i am really sorry......i was not able to understand you please ask me again."

# while 1:
    
#     text = input("speak .....")

#     if text == "stop":
#         break

#     print(speak(text))

    
