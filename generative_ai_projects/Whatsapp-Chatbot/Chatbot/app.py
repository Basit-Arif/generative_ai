import streamlit as st
import model

with st.form(key='my_form'):
    number = st.text_area('Enter Phone number')
    message = st.text_area("Enter Message")
    submitted = st.form_submit_button('Send Message')

if submitted:
    message_sent = model.send_whatsapp_message(number, message)
    st.write(message_sent)