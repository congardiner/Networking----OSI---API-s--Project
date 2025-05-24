# Program Overview:
# Refer to the README.md file for a detailed explanation, basis of this project though to explore the OSI Model through a simple client-server architecture,
# and fine tune my understanding of how the OSI model works in a software context alongside with the TCP/IP model.

# First initial steps included installing y-finance, pandas, and a few other dependency libraries:

import socket
import yfinance as yf
import pandas as pd
from datetime import datetime
import os

SERVER_HOST = '127.0.0.1'

SERVER_PORT = 65432


def stock_price(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data_frame = ticker.history(period="1d")

    # implemented a quick boolean check to see if the data frame was actually sent with data from yfinance.
    if not data_frame.empty:

        last_price = data_frame['Close'].iloc[-1]
        return True, last_price
    
    else:
        return False, f"There was no data found or available for {ticker_symbol.upper()}. Please try again and ensure that the symbol is spelled correctly."


# I created this function with the intent to use pandas to store the retrieved packets from the server within a csv file.
# This is something that can be used to data analysis on the packets that are being sent and received.
# This server uses TCP sockets to send and receive data ensuring that no data is lost, the csv file is sort of an afterthought to ensure that the data is stored correctly and formatted in the manner that I want it to be.

def save_to_csv_file(ticker_symbol, price):

    file_path = "stock_price.csv"
    file_exists = os.path.isfile(file_path)

    yfin_df = pd.DataFrame([{

            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ticker": ticker_symbol,
            "price": price

        }])
    

    yfin_df.to_csv("stock_price.csv", mode='a', header=not file_exists, index=False)

    print("File Saved:", os.path.abspath("stock_price.csv"))


# Creates a TCP/IP Socket, binds it to the server address and port, and listens for incoming connections.
# This is something that could be traceable within WireShark, which is an excellent tool for monitoring network traffic.
# Behavior like this ensures that the server is listening and accepting the correct packets instead of dropping them otherwise.

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen()

    print()
    print(f"{SERVER_HOST}: {SERVER_PORT} is in a listening state... Make the initial request now...")
    print()

    # The purpose of this while loop is to ensure that the server is accepting connections and handles requests recursively.
    # This ensures that as well that scheduling can be integrated for time-sequenced requests.

    while True:

        connection, address = server_socket.accept()

        with connection:
            print(f"\n{SERVER_HOST} connected by {address} on {SERVER_PORT}.")

            ticker_symbol = connection.recv(1024).decode().strip().upper()
            print(f"Received request for: {ticker_symbol}")

            success, result = stock_price(ticker_symbol)

            if success:
                save_to_csv_file(ticker_symbol, result)
                response = f"Stock Symbol: {ticker_symbol} Last price: ${result:.2f}."
            else:
                response = result  # The error message from stock_price()

            connection.sendall(response.encode())
