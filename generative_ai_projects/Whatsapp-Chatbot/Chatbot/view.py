from fastapi import FastAPI,status,Request
import logging
import requests
import json
from model import send_whatsapp_message,send_custom_message,send_logistic_preference
from fastapi.responses import JSONResponse
from utils.shopifyservice import update_tag



from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

VERIFY_TOKEN = '12345'  # Replace with your actual verify token


def genearate_responce(sendernumber,text):
    """Generates a response to an API request.
    """
    return send_custom_message(sender_number=sendernumber,template_name=text.upper())

    


def verify(mode: str , token: str, challenge: str ):
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
       
        if mode == "subscribe" and token == VERIFY_TOKEN:
            # Respond with 200 OK and challenge token from the request
            # logging.info("WEBHOOK_VERIFIED")
            
            return int(challenge)
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            logging.info("VERIFICATION_FAILED")
            return json.dumps({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        logging.info("MISSING_PARAMETER")
        return json.dumps({"status": "error", "message": "Missing parameters"}), 400

@app.get("/webhook")
def data(hub_mode: str = Query(..., alias="hub.mode"),
    hub_challenge: str = Query(..., alias="hub.challenge"),
    hub_verify_token: str = Query(..., alias="hub.verify_token")):
    return verify(mode=hub_mode,token=hub_verify_token,challenge=hub_challenge)

# @app.get("/webhook")
# def hello():
#     verify()
#     return {"return":True}

@app.post("/webhook")
async def handle_webhook(request:Request,payload: dict):
    print("click")
    body=await request.body()
    body_json = json.loads(body)
    if body_json:
        print("----------------------------------")
        print(f"this is body json{body_json}")
        try:
            confirmation_text = body_json["entry"][0]["changes"][0]["value"]["messages"][0]["button"]["text"]
            wa_id = body_json['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']

            try:
                order_id=body_json["entry"][0]["changes"][0]["value"]["messages"][0]["button"]["payload"]
                query_json = order_id.replace("'", "\"")
                query_load = json.loads(query_json)
                print(query_load["order_id"])
                print(query_load["city"])
                try:
                    data2=update_tag(order_id=query_load["order_id"],tag_value=confirmation_text)
                    if query_load["city"]=="karachi":
                        updated=update_tag(order_id=query_load["order_id"],tag_value=[confirmation_text,query_load["city"]])
                        print("updated sucessfilu")
                    else:
                        pass
                except Exception as es:
                     print(f"error is {es}")
                # json_dict=json.dumps(order_id)
                # json_dict = json.loads(json_dict.replace("\"",'"'))
                # print(dict(order_id)[0]["city"])

                # Access individual values
                # order_id = json_dict.gets
                # city_name = json_dict.get('city', None)

                # print("Order ID:", order_id)
                # print("City Name:", city_name)

            except Exception as e:
                print("Error decoding JSON:", e)
                

            print(confirmation_text)
            try:
                city=body_json["entry"][0]["changes"][0]["value"]["messages"][0]["button"]["payload"]["city"]
                if city=="karachi":
                    print("this in karachi")
                else:
                    raise ValueError("City is not Karachi")
            except Exception as es:
                print("this is "+str(es))
                    
            
            if confirmation_text=="Confirm Order":
                print("in confir order")
                
                
                # send_custom_message(sender_number=wa_id,template_name="May i know the preferred logistics you want")
        except:
            print("hi")
    if payload:
        try:
            print("**********************************************")
            print(f"this is paylod {payload}")
            # print(payload)
            text=payload['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            sender_number=payload['entry'][0]['changes'][0]['value']['messages'][0]['from']
            print(text)
            print(sender_number)
            genearate_responce(sendernumber=f"+{sender_number}",text=text)
            return status.HTTP_200_OK
        except Exception as es:
            pass
            
            # return JSONResponse(content={"status": "error", "message": "Not a WhatsApp API event"},status_code=404)
    else:
        raise ValueError('No Payload')
@app.get("/example")
async def example_route():
    return JSONResponse(content={"status": "ok"}, status_code=500)



# @app.post("/webhook")
# def handle_webhook(payload: dict):
#     return {"received_payload": payload}




if __name__=="__main__":
    import uvicorn
    
    uvicorn.run("view:app",reload=True,port=8000)
