# Streamlit is a webkit application that makes locally hosting a GUI for a webpage for basic interactivity accessible, which is why I opted to use this library
# for this project, as it allowed me to experiment with something new that I found with some research, overall I am pleased with how it turned out for a basic foundation for a user interface.

import streamlit as st
import socket
import pandas as pd
import os


HOST = '127.0.0.1'
PORT = 65432


st.set_page_config(layout='centered')

st.title("Real-Time Stock Price Tracker")
st.subheader("Created by: Conner Gardiner")
st.write("This applet allows you to request real-time stock prices for various tech companies using yfinance and a TCP socket connection.")

# This was a format that I came across in which I realized I could create a dropdown of the listed ticker(s) that are at least common within the tech industry as a reference.
# I chose several of the biggest tech companies to include in this dropdown menu.

tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'TSM', 'AVGO', 'ORCL', 'CRM', 'ADBE', 'CSCO', 'AMD', 'QCOM', 'INTC', 'IBM', 'SAP', 'ACN', 'INTU']


ticker = st.selectbox("Select a Stock to Explore:", tech_stocks)


if st.button("Get the Stock Price") and ticker:

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sendit:

        sendit.connect((HOST, PORT))
        sendit.sendall(ticker.encode())
        data = sendit.recv(1024)


    print()
    st.success(f"The Server sent this after the request: {data.decode()}")
    print()


# This aspect allows the user to request any stock ticker if they have a specific one that they've researched as its not a static list of tech stocks.

st.divider()



### TESTING in PROGRESS ###
# This ensures that the stock_price.csv file is found within the folder structure, and if present, the data is read and displayed within the streamlit app.
# If the file is not found, which if the specific csv file has not been made yet, well then it will populate this error.
# Overall, this logic works as a basic foundation, however, it could be improved with being able to handle or even create the file under a different name if the user desired that option.

log_path = os.path.join(os.getcwd(), "stock_price.csv")

if os.path.exists(log_path):
    df = pd.read_csv(log_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    st.divider()
    st.subheader("Historical Price Data")

    selected = st.selectbox("Select a desired Stock to View the History", df['ticker'].unique())
    filtered = df[df['ticker'] == selected]

    st.dataframe(filtered.tail(10), use_container_width=True)
    st.line_chart(filtered.set_index('timestamp')['price'])

else:

    st.warning("stock_price.csv wasn't found yet. Start by initiating a request to the yfiance API first to create the file.")
