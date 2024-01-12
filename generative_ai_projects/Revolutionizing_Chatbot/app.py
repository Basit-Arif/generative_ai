from threading import Thread
from flask import Flask, jsonify
from model import OpenAi  # Assuming your OpenAi class is in model.py

app = Flask(__name__)

assistant = "Your are a data scientist. Your duty is to read the data and provide relevant information about it. Keep in mind you will be talking to stakeholders."
modelname = "Data Scientist"

obj1 = OpenAi(name=modelname, instruction=assistant)
message_create = obj1.send_message("create 10 question real")
@app.route("/completed")
def check_completion():
    global obj1
    if obj1.isCompleted():
        role, content = obj1.get_latest_responce()
        return jsonify(content)  # You can perform any action you want when completed

@app.route("/")
def index():
    
    return 'Hello, this is a basic Flask app!'


if __name__ == '__main__':
    # Start a separate thread to continuously check completion
    completion_thread = Thread(target=check_completion)
    completion_thread.start()

    app.run(debug=True)