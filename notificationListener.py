import notifypy
import socket
import time

def connect_to_server():
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with open('user', 'r') as username:
            user = username.read().strip()  # Read and strip any whitespace

        # Attempt to connect to the notification server
        client_socket.connect((socket.gethostname(), 8080))
        print("Connected to notification server.")
        return client_socket, user
    except ConnectionRefusedError:
        print("Notification server is not available")
        return None, None  # Return None for both values if connection fails


def check(message, client_socket, user):
    # Check if the received message starts with 'notify<'
    if message.startswith('notify<'):
        # Find the position of the '<' and '>'
        start_index = message.find('<') + 1
        end_index = message.find('>')

        # Extract the user and task
        if start_index > 0 and end_index > start_index:
            extracted_user = message[start_index:end_index]
            print (f'User: {extracted_user}')
            task = message[end_index + 1:]  # The task follows the user
            print (f'Task: {task}')

            # Check if the extracted user matches the provided user
            if extracted_user == user:
                # Create and send a notification
                notification = notifypy.Notify()
                notification.title = "New Task Added:"
                notification.message = task
                notification.send()



while True:
    try:
        client_socket, user = connect_to_server()  # Connect to the server
        if client_socket is None or user is None:
            print("Failed to connect to the server. Retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying
            continue  # Skip to the next iteration of the loop
    except ConnectionRefusedError:
        print("Notification server is not available. Retrying in 5 seconds...")
        time.sleep(5)  # Wait before retrying

    while True:
        try:
            message = client_socket.recv(2048).decode("UTF-8")
            if message:
                print("Received from server:", message)
                check(message, client_socket, user)
        except (ConnectionResetError, ConnectionAbortedError):
            print("Connection lost. Reconnecting...")
            client_socket.close()  # Close the socket before reconnecting
            break  # Exit the inner loop and reconnect

client_socket.close()