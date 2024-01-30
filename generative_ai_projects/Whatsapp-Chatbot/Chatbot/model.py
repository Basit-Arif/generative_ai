import requests
import json

async def send_whatsapp_message(sender_number:str,name:str,order:str):
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
    'Authorization': 'Bearer EAAVickuwzN8BOyNMU0UDxyhSid7rxZAkWOZBCF4hn3ACC6IAo6uvSmZAd1TWwmqWRELw4ugrbVkvpZBBoMsdQR820RvPGgEiAyGoMtFOTFouGhpYvLYDwebT0ZAHcUDQHOZC1HMcM7DWZA1ZAFQwUTrTumZAOwKdqJAV3zkRIpgo2scayStT5q5tKhyguL4uocZAUNIQIi2zaimjqeos7QNtAZD'
    }
    responce=requests.request("POST", url, headers=headers, data=payload)

    return await responce.text



def send_confirmation_template(sender_number:str,name:str,order:str,currency:str):
    url = "https://graph.facebook.com/v18.0/190019904202736/messages"

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
                    {"type": "payload", "payload": "PAYLOAD"}
                ]
            },
            {
                "type": "button",
                "sub_type": "quick_reply",
                "index": "1",
                "parameters": [
                    {"type": "payload", "payload": "PAYLOAD"}
                ]
            }
        ]
    }
})
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer EAAVickuwzN8BOyNMU0UDxyhSid7rxZAkWOZBCF4hn3ACC6IAo6uvSmZAd1TWwmqWRELw4ugrbVkvpZBBoMsdQR820RvPGgEiAyGoMtFOTFouGhpYvLYDwebT0ZAHcUDQHOZC1HMcM7DWZA1ZAFQwUTrTumZAOwKdqJAV3zkRIpgo2scayStT5q5tKhyguL4uocZAUNIQIi2zaimjqeos7QNtAZD'
    }
    responce=requests.request("POST", url, headers=headers, data=payload)

    return responce.text



def send_custom_message(sender_number:str,template_name:str):
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
    'Authorization': 'Bearer EAAVickuwzN8BOyNMU0UDxyhSid7rxZAkWOZBCF4hn3ACC6IAo6uvSmZAd1TWwmqWRELw4ugrbVkvpZBBoMsdQR820RvPGgEiAyGoMtFOTFouGhpYvLYDwebT0ZAHcUDQHOZC1HMcM7DWZA1ZAFQwUTrTumZAOwKdqJAV3zkRIpgo2scayStT5q5tKhyguL4uocZAUNIQIi2zaimjqeos7QNtAZD'
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
        "Authorization": "Bearer EAAVickuwzN8BO5wqPNVsZA4py8MrZBaDcJHW1u1f3QZBWFEtjDRsMNfM340ZCTZCTmoCDSIf6r4uzqrwIBDwnQPdwiXVgsHLlp2Bpvr6Mpxq7ehk8ZBkboz0xjPgAV2Yd2CXOxZCyLs7dZBIcGdvHQy320XznAuzh8LmlzK33D4N8KZBSVEdGZAcmkjGGwE6CvAB7byPlTawRQZAmIqqzr8wJsZD'",
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

# data=send_whatsapp_message(sender_number='923242586315',name="basit",order="321")
# print(data)
# obj1=send_message(data=data)
# data=send_confirmation_template(sender_number='923242586315',name="basit",order="321",currency="100")
# print(data)