from fastapi import FastAPI,status,Request
import logging
import requests
import json
from model import send_whatsapp_message,send_custom_message,send_logistic_preference
from fastapi.responses import JSONResponse
from utils.shopifyservice import update_tag
import os 
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()
load_dotenv()
VERIFY_TOKEN = str(os.getenv("VERIFY_TOKEN"))  # Replace with your actual verify token


async def genearate_responce(sendernumber,text):
    """Generates a response to an API request.
    """
    return await send_custom_message(sender_number=sendernumber,template_name="🌟 Thank you for contacting Kidsay Store! 🌟 This number is for confirmation texts only. For inquiries, please call us at +92 324 2586315. 📞 We appreciate your understanding! 🙏")

    


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
    # print("click")
    body=await request.body()
    body_json = json.loads(body)
    if body_json:
        # print("----------------------------------")
        # print(f"this is body json{body_json}")
        try:
            payload_buttton_text = body_json["entry"][0]["changes"][0]["value"]["messages"][0]["button"]["text"]
            wa_id = body_json['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
            payload=body_json["entry"][0]["changes"][0]["value"]["messages"][0]["button"]["payload"]
            query_json = payload.replace("'", "\"")
            query_load = json.loads(query_json)
            # print(query_json)
            try:
                if query_load["payload_type"]=="logistics":
                    await send_custom_message(wa_id,f"Good news! Your order is set, and {payload_buttton_text} is on the way. Thanks for choosing us. Get ready for your special delivery") 
                    update_tag(order_id=query_load["order_id"],tag_value=[payload_buttton_text,payload_buttton_text])
            except:
                pass
            try:
                
                if query_load["payload_type"]=="Confirmation_text":
                    if payload_buttton_text=="Confirm Order":
                        try:
                            update_tag(order_id=query_load["order_id"],tag_value=payload_buttton_text)
                            if query_load["city"]=="karachi":
                                send_logistic_preference(wa_id,query_load["order_id"])
                                # updated=update_tag(order_id=query_load["order_id"],tag_value=[confirmation_text,query_load["city"]])
                                return {"success":"200"}
                            else:
                                await send_custom_message(wa_id,"Got it! Your order is confirmed. We're on it. Thanks for choosing us!")
                        except Exception as es:
                            print(f"error is {es}")  
                    else:
                        await send_custom_message(wa_id,"Your order got *canceled*. Can you tell us why? We're here to help. Thank you. 🛍️")
                        update_tag(order_id=query_load["order_id"],tag_value=payload_buttton_text)
            except Exception as e:
                pass
        except:
            pass
    if payload:
        try:
            # print("**********************************************")
            # print(f"this is paylod {payload}")
            # print(payload)
            text=payload['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            sender_number=payload['entry'][0]['changes'][0]['value']['messages'][0]['from']

            await genearate_responce(sendernumber=f"+{sender_number}",text=text)
            return status.HTTP_200_OK
        except Exception as es:
            pass
            
            # return JSONResponse(content={"status": "error", "message": "Not a WhatsApp API event"},status_code=404)
    else:
        raise ValueError('No Payload')




# @app.post("/webhook")
# def handle_webhook(payload: dict):
#     return {"received_payload": payload}




if __name__=="__main__":
    import uvicorn
    
    uvicorn.run("view:app",reload=True,port=8000)
