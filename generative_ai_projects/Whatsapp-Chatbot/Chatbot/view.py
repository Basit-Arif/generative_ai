from fastapi import FastAPI,status,Request
import logging
import requests
import json
from model import send_whatsapp_message,send_custom_message
from fastapi.responses import JSONResponse



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
    body=await request.body()
    body_json = json.loads(body)
    if body_json:
        try:
            confirmation_text = body_json["entry"][0]["changes"][0]["value"]["messages"][0]["button"]["text"]
            if confirmation_text=="Confirm Order":
                print(f"{confirmation_text} your order is confirmed")
        except:
            print("hi")
    if payload:
        try:
            # print(payload)
            text=payload['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            sender_number=payload['entry'][0]['changes'][0]['value']['messages'][0]['from']
            # print(text)
            # print(sender_number)
            # genearate_responce(sendernumber=sender_number,text=text)
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
