import socket, time, sys

n = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
n.bind ((socket.gethostname(), 8080))
n.listen (5)
print ("Notification Socket bound")

items = []

with open('notifiableItems', 'r') as notifFile:
    for line in notifFile:
        items.append(line.strip())
print(items)


while True:
    clientSocket, address = n.accept ()
    print (f"Connection Established from address {address}")
    for item in items:
        task, user = item.split('|')
        task = task.strip()  # Remove any leading/trailing whitespace
        user = user.strip()   # Remove any leading/trailing whitespace
        
        # Send the user and task to the client
        clientSocket.send(f"notify<{user}".encode("UTF-8"))
        print(f"sent: notify<{user}")
        time.sleep (0.5)
        clientSocket.send(task.encode("UTF-8"))
        print(f"sent: {task}")
        time.sleep (0.5)
        with open('notifiableItems', 'w') as notifFile:
            notifFile.write ('')

    clientSocket.close ()
    break
