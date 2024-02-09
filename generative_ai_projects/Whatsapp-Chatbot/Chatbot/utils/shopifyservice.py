import requests
from typing import Optional,Union

def update_tag(order_id:str,tag_value:Optional[Union[str, list]]):
    access_token = "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"

# Define the endpoint URL
    url = f"https://42c5c8-4.myshopify.com/admin/api/2024-01/orders/{order_id}.json"

# Define the payload data
    data = {
        "order": {
            "id": int(order_id),
            "tags":f'{tag_value}'
        }
    }

    # Define headers
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

# Make the PUT request
    response = requests.put(url, json=data,headers=headers)

# Print the response status code and content
    if response.status_code == 200:
        return {"status": "success", "message": "Tag updated successfully"}
    else:
        return {"status": "error", "message": response.content.decode("utf-8")}

