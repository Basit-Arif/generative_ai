from fastapi import FastAPI, HTTPException, Request,status
import hmac
import hashlib
import base64
import os 
from dotenv import load_dotenv

from model import send_confirmation_template

app = FastAPI()
load_dotenv()

def replace_zero_with_country_code(number):
    # Check if the number starts with "0"
    if number.startswith("0"):
        # If yes, replace the leading "0" with "+92"
        converted_number = "+92" + number[1:]
    else:
        # If not, keep the original number
        converted_number = number

    # Return the converted or original number
    return converted_number

# The Shopify app's client secret, viewable from the Partner Dashboard.
# In a production environment, set the client secret as an environment variable
# to prevent exposing it in code.
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

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
        city=payload.get('shipping_address',{}).get('city', '').lower()
        order_id_and_address = {
            "payload_type": "Confirmation_text",
            "order_id": payload.get('id'),
            "city": payload.get('shipping_address', {}).get('city', '').lower()
        }
        data_send= send_confirmation_template(replace_zero_with_country_code(phone_number),name_of_person,order_id,total_price,order_id_and_address)
        return {"Message Sent": f"{data_send}"}



if __name__=="__main__":
    import uvicorn
    uvicorn.run("shopifydata:app",reload=True,port=8001)
