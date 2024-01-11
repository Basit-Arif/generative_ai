import streamlit as st 
from model import OpenAi
from model import messageItem,get_message_by_thread
from authenticate import authenticate_user,get_thread_key,input_data,put_thread_key,get_data,get_limit_message,set_initial_limit,update_limit_counter
import time
from typing import Optional
# Authentication logic
def format_messages(messages:Optional[list]):
    try:
        formatted_messages = []
        for message in messages:
            role = list(message.keys())[0]
            content = message[role]
            formatted_messages.append((role, content))
        return formatted_messages
    except:
        return "No History Found"


st.title("AI Chatterbox 2.0: Your Smart Conversational Partner \U0001F913")
st.sidebar.title("AI Chatterbox 2.0 \U0001F913")
st.sidebar.markdown("---")
st.sidebar.header("Are You New to this Chatterbox?")
asking=st.sidebar.radio("Already user",["Already have Registered Code","New User"])


if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False


if not st.session_state.is_logged_in:
    if asking == "New User":
        username:str = st.sidebar.text_input("Enter Your Username")
        phonenumber:int = st.sidebar.text_input("Enter Any Unique Number")
        
        if st.sidebar.button("Sign Up"):
        
            if phonenumber:
                try:
                    # Check if the phone number is already registered
                    is_registered = get_data(phone_number=phonenumber,username=username)
                    
                    if not is_registered:  # If not registered, proceed with registration
                        data_inserted = input_data(phone_number=phonenumber,username=username)
                        
                        if data_inserted:
                            st.sidebar.success("Successfully registered!")
                            st.balloons()
                            set_initial_limit(phonenumber=phonenumber)
                            key=None
                            st.session_state.is_logged_in = True
                            st.session_state.authentic = True
                
                        else:
                            st.sidebar.write("Already registered")
                    else:
                        st.sidebar.error("Already Registered")
                        st.sidebar.write("Try Another Code Digit")
                except:
                    st.sidebar.error("An error occurred. Please try again.")
    else:
        pass 

if not st.session_state.is_logged_in and asking=="Already have Registered Code":
    username = st.sidebar.text_input("Enter Username")
    phonenumber = st.sidebar.text_input("Enter Registered Code")
    

    if st.sidebar.button("Login"):
    
        if authenticate_user(phone_number=phonenumber,username=username):
            st.sidebar.success("Login successful!")
            key=get_thread_key(phone_number=phonenumber)
            # OpenAi.get_thread()
            st.session_state.is_logged_in = True
            st.session_state.authentic = True  # Set authenticated state
            
        else:
            st.sidebar.error("Invalid credentials. Please try again.")

if st.session_state.is_logged_in==True:
    st.sidebar.empty() 
 
    if "bot" not in st.session_state :
        st.session_state.bot=OpenAi(name="Data Scientist",instruction="Your are an data scientist",thread_key=key,phonenumber=phonenumber)
    # with st.sidebar.expander("your history"):
    #     history=your_previous_message(key)
    #     st.markdown(history) 
    if "phone" not in st.session_state:
        st.session_state.phone=phonenumber
    if "thread_key" not in st.session_state:
        st.session_state.thread_key=key

    st.sidebar.text("Your unique identity "+ st.session_state.phone)
    counter,value=get_limit_message(st.session_state.phone)
    print(counter,value)
    st.sidebar.text(f"Your Remaining Prompt are : {20-value}")
    for m in st.session_state.bot.get_message():
        with st.chat_message(m.role):
            st.markdown(m.content)


    messages = get_message_by_thread(thread_key=st.session_state["thread_key"])
 
    formatted_messages = format_messages(messages)

    with st.sidebar.expander("See History"):
        try:
            for role, content in formatted_messages:
                if role == "user":
                    with st.container():
                        st.markdown(f":bust_in_silhouette: **User:** {content}")
                else:
                    with st.container():
                        st.markdown(f":robot_face: **AI:** {content}")
        except:
            with st.container():
               st.write("No History Found")

    if st.session_state.is_logged_in:
        print(st.session_state.phone)
        counter,value=get_limit_message(st.session_state.phone)
        print(counter)
        if counter and value < 20: 
        # if get_limit_message(phonenumber=phonenumber):
            if prompt := st.chat_input("Please Ask a Question") :
                st.session_state.bot.send_message(prompt)
                update_limit_counter(st.session_state.phone,value+1)
                
                with st.chat_message("user"):
                    st.markdown(prompt)

                if(st.session_state.bot.isCompleted()):
                    response: messageItem = st.session_state.bot.get_latest_responce()
                    with st.chat_message(response.role):
                        st.markdown(response.content)
        else:
            st.error("You have reached the limit of text-based communication today.")
# st.sidebar.text(st.session_state.bot.get_thread())