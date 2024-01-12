# Chatbot Project

## Overview
This project implements a chatbot using Streamlit, SQLAlchemy, and OpenAI's GPT-3.5 Turbo model. The chatbot allows users to interact with an AI assistant, authenticate users based on phone numbers, and store chat history in a PostgreSQL database.

## Getting Started
### Prerequisites
- Python 3.7 or higher
- Streamlit
- SQLAlchemy
- psycopg2
- OpenAI Python SDK
- dotenv

### Installation
1. Clone the repository:

```bash
git clone https://github.com/yourusername/chatbot-project.git
cd chatbot-project
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```
3. Set up a PostgreSQL database and update the .env file with the database connection details.

4. Run the Streamlit app:

```bash
streamlit run streamlitapp.py
```
This will start the web application on your local machine, which you can access at `localhost:
## Usage

- Visit the Streamlit app in your web browser.
- If you are a new user, sign up by entering your username and phone number.
- If you are a returning user, enter your registered username and phone number to log in.

## Features

- User authentication based on phone numbers and usernames.
- Chat history stored in a PostgreSQL database.
- Limit on the number of messages a user can send in a day.

## ShowCase of Project 

![project Screenshot](https://github.com/Basit-Arif/generative_ai/blob/main/generative_ai_projects/Revolutionizing_Chatbot/Screenshot%202024-01-11%20at%207.38.13%20PM.png)

- **Explanation of project**
    - **Your Unique Code:** Users create a unique input code upon registration, ensuring secure and personalized interactions. This code serves as an identifier for seamless logins and chat history access.
    - **Remaining Prompts:** Check the sidebar to see the number of remaining prompts available for a single user. The app limits text-based communication to ensure a smooth prototype experience. This restriction encourages a balanced interaction and helps optimize the application’s performance.
    - **Chat History:** The app stores chat histories in a PostgreSQL database, allowing users to revisit conversations and explore the evolution of interactions with the AI assistant
    - **Human Prompt and AI-Generated Response:** Engage in dynamic conversations by providing human prompts through the user interface. Witness the power of OpenAI’s GPT-3.5 Turbo model as it generates context-aware responses
    - **User Prompt can be added here:** Explore the chat interface and provide prompts for the AI assistant to generate responses. Interact seamlessly and experience the tailored AI conversations.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.