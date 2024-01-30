from fastapi import FastAPI, HTTPException, Request,status
import hmac
import hashlib
import base64
from model import send_whatsapp_message,send_confirmation_template

app = FastAPI()

# The Shopify app's client secret, viewable from the Partner Dashboard.
# In a production environment, set the client secret as an environment variable
# to prevent exposing it in code.
CLIENT_SECRET = "965e1b5acc7e31e9afe8c385893fbd08a0a2820b7cd5c0eb22c28c90a90b0ff2"

def verify_webhook(data, hmac_header):
    digest = hmac.new(CLIENT_SECRET.encode('utf-8'), data, digestmod=hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest)
    # print(hmac_header.encode('utf-8'))
    print(hmac.compare_digest(computed_hmac, hmac_header.encode('utf-8')))
    return hmac.compare_digest(computed_hmac, hmac_header.encode('utf-8'))

@app.post('/webhook')
async def handle_webhook(request: Request,payload:dict):
    data = await request.body()
    print("-------------------------------------------")
    hmac_header = request.headers.get('X-Shopify-Hmac-SHA256')
    print(hmac_header)
    if not verify_webhook(data, hmac_header):
        raise HTTPException(status_code=401, detail="Invalid webhook")
    else:
        order_id = payload.get('id')
        name_of_person = payload.get('billing_address', {}).get('name')
        total_price = payload.get('total_price_set', {}).get('shop_money', {}).get('amount')
        phone_number = payload.get('billing_address', {}).get('phone')
        print(payload)
        print(phone_number)
        data_send= send_confirmation_template(phone_number,name_of_person,order_id,total_price)
        return {"Message Sent": f"{data_send}"}


# @app.get("/webhook")
# async def data_received(request:Request):
#     data=request.body()
#     print(data)


if __name__=="__main__":
    import uvicorn
    uvicorn.run("shopifydata:app",reload=True,port=8001)
