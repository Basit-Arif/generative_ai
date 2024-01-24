from fastapi import FastAPI
import logging
import requests
import json


from fastapi import FastAPI, HTTPException, Query

app = FastAPI()

VERIFY_TOKEN = '12345'  # Replace with your actual verify token


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
def handle_webhook(payload: dict):
    print(payload)
    return {"received_payload": payload}


if __name__=="__main__":
    import uvicorn
    uvicorn.run("view:app",reload=True,port=8000)
