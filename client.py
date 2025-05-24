import socket

HOST = '127.0.0.1'
PORT = 65432

# NOTE: The user can request a stock price by entering the ticker symbol; however, this will need to be known beforehand which is a limiting factor to the usability of the program right now.
# The server will then respond with the last price of the stock from yfinance.
# It would be neat to add a scheduling feature, along with a GUI that also houses all of the active ticker symbols.
# This could be enabled for a user to select from like a drop down or query via a list so that they don't have to manually search beforehand.
# NOTE: This was my initial testing shell document that I used for the client side of the socket script, however, this is just here as a baseplate for where I started.



print()
print()
stock_ticker = input("Which Stock would you like to search for today?".strip())
print()
print()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print()
    print(f"{HOST} connected to {PORT}.")
    print()

    client_socket.sendall(stock_ticker.encode())
    data = client_socket.recv(1024)

    print()
    print(f"This information was successfully received from the server: {data.decode()}.")
    print()
    print()    
    print()