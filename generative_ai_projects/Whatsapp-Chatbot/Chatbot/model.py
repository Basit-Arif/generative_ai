import requests
import json
from dotenv import load_dotenv
import os 

def send_whatsapp_message(sender_number:str,name:str,order:str):
    load_dotenv()
    url = "https://graph.facebook.com/v18.0/190019904202736/messages"

    payload = json.dumps({
    "messaging_product": "whatsapp",    
    "recipient_type": "individual",
    "to": f"{sender_number}",
    "type": "template",
    "template": {
        "name": "order_confirmation_template",
        "language": { "code": "en_US" },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": f"{name}"
                    },
                    {
                        "type": "text",
                        "text": f"{order}"
                    }
                ]
            }
        ]
    }
})
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("Whatsapi2")}'
    }
    responce=requests.request("POST", url, headers=headers, data=payload)

    return responce.text



def send_confirmation_template(sender_number:str,name:str,order:str,currency:str,order_id_and_address:dict):
    load_dotenv()
    url = "https://graph.facebook.com/v18.0/190019904202736/messages"

    try:
        payload = json.dumps({
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"{sender_number}",
        "type": "template",
        "template": {
            "name": "order_confirmation",
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {"link": "https://kidsay.pk/cdn/shop/files/264093038_328334635446492_1088017589315017607_n.jpg"}
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": f"{name}"},
                        {"type": "text", "text": f"{order}"},
                        {"type": "text", "text": f"{currency}"}
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "quick_reply",
                    "index": "0",
                    "parameters": [
                        {"type": "payload", "payload": f"{order_id_and_address}"},
                        # {"type":"text","text":f"{city}"}
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "quick_reply",
                    "index": "1",
                    "parameters": [
                        {"type": "payload", "payload": f"{order_id_and_address}"}
                    ]
                }
            ]
        }
    })
    except Exception as es:
        print(es)
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("Whatsapi2")}'
    }
    try:
        responce=requests.request("POST", url, headers=headers, data=payload)
    except Exception as es:
        print(es)
    print(responce.text)
    return responce.text



def send_logistic_preference(w_id):
    load_dotenv()
    url = "https://graph.facebook.com/v18.0/190019904202736/messages"
    payload = json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": f"{w_id}",
    "type": "template",
    "template": {
        "name": "logistic_preference",
        "language": {"code": "en_US"},
        "components": [
            {
                "type": "button",
                "sub_type": "quick_reply",
                "index": "0",
                "parameters": [
                    {"type": "payload", "payload": "TCS"}
                ]
            },
            {
                "type": "button",
                "sub_type": "quick_reply",
                "index": "1",
                "parameters": [
                    {"type": "payload", "payload": "Leopard"}
                ]
            },
            {
                "type": "button",
                "sub_type": "quick_reply",
                "index": "2",
                "parameters": [
                    {"type": "payload", "payload": "Trax"}
                ]
            }
        ]
    }
})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("Whatsapi2")}'
        }
    responce=requests.request("POST", url, headers=headers, data=payload)

    return responce.text





def send_custom_message(sender_number:str,template_name:str):
    load_dotenv()
    url = "https://graph.facebook.com/v18.0/190019904202736/messages"

    payload = json.dumps({
    
    "messaging_product": "whatsapp",    
    "recipient_type": "individual",
    "to": f"{sender_number}",
    "type": "text",
    "text": {
        "preview_url": False,
        "body": f"{template_name}"
    }

    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {os.getenv("Whatsapi2")}'
    }
    responce=requests.request("POST", url, headers=headers, data=payload)

    return responce



def send_personalise_whatsapp_message(recipient,text):
        return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )
def send_message(data):
    
    headers = {
        "Content-type": "application/json",
        "Authorization": f'Bearer {os.getenv("Whatsapi2")}'
    }

    url = f"https://graph.facebook.com/v18.0/190019904202736/messages"

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response



# data=send_whatsapp_message(sender_number='+923242586315',name="basit",order="321")
# print(data)
# obj1=send_message(data=data)
# data=send_logistic_preference("+923242586315")
# data=send_custom_message('+923242586315',"basit")
# data
# data=send_confirmation_template("+923242586315","Basit","5867126882391","1200","{'order_id': 5867126882391, 'city': 'karachi'}")
# data