import socket, time, os, csv, simpleEncryption
from datetime import datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind ((socket.gethostname(), 6060))
s.listen (5)


n = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
n.bind ((socket.gethostname(), 8080))
n.listen (5)
print ("Socket bound")

items = []
clientSocket, address = s.accept ()
notifSocket, nAddress = n.accept ()

while True:
    
    #notifSocket, nAddress = n.accept ()
    print (f"Connection Established from address {address}")
    message = clientSocket.recv(2048).decode ()

    print ("Request Type:", message)

########################################################################################################

    ## Get Tasks From List
    # Get User
    if ']getTasksFromList' in message:
        clientSocket.send("getTasksFromList items incoming".encode("UTF-8"))
        start_index = message.find('[') + 1  # Get the index right after '['
        end_index = message.find(']')        # Get the index of ']'

        # Extract the characters between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            user = message[start_index:end_index]
        
        # Get List Name
        start_index = message.find('<') + 1  # Get the index right after '<'
        end_index = message.find('>')        # Get the index of '>'

        # Extract the name between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            list_name = message[start_index:end_index]
            listFilename = f'lists/{user}PersonalList{list_name}'

        try:
            with open(listFilename, 'r') as listFile:
                for line in listFile:
                    line = line.strip()
                    print('sending', line)
                    clientSocket.send(line.encode("UTF-8"))
                    time.sleep(0.1)
        except FileNotFoundError:
            with open(listFilename, 'w') as listFile:
                print(f'Created new list for {user} as no list was found')
                listFile.write("Add your items below")
            with open(listFilename, 'r') as listFile:
                for line in listFile:
                    line = line.strip()
                    print('sending', line)
                    clientSocket.send(line.encode("UTF-8"))
                    time.sleep(0.1)

        clientSocket.send("getTasksFromList items finished".encode("UTF-8"))
########################################################################################################
    

## Get Tasks From Family List
    # Get User
    if ']getTasksFromFamilyList' in message:
        clientSocket.send ("getTasksFromFamilyList items incoming".encode ("UTF-8"))
        start_index = message.find('[') + 1  # Get the index right after '<'
        end_index = message.find(']')        # Get the index of '>'

        # Extract the characters between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            family = message[start_index:end_index]
    
        # Get List Number
        start_index = message.find('<') + 1  # Get the index right after '<'
        end_index = message.find('>')        # Get the index of '>'

        # Extract the number between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            list_name = message[start_index:end_index]
            listFilename = f'lists/{family}FamilyList{list_name}'
            print (f'Family list requested: {listFilename}')

        try:
            with open (listFilename, 'r') as listFile:
                for line in listFile:
                    line = line.strip ()
                    print ('sending', line)
                    clientSocket.send (line.encode ("UTF-8"))
                    time.sleep (0.1)
        except FileNotFoundError:
            with open (listFilename, 'w') as listFile:
                print(f'Created new list for {family} as no list was found')
                listFile.write ("Add your items below")
            with open (listFilename, 'r') as listFile:
                for line in listFile:
                    line = line.strip ()
                    print ('sending', line)
                    clientSocket.send (line.encode ("UTF-8"))
                    time.sleep (0.1)

                
        clientSocket.send ("getTasksFromFamilyList items finished".encode ("UTF-8"))

########################################################################################################

    ## Get New Items For List
    if ']addNewTasksToList' in message:
        print("Incoming addNewTasksToList request")
        items = []
        start_index = message.find('[') + 1  # Get the index right after '['
        end_index = message.find(']')        # Get the index of ']'
        
        # Extract the characters between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            user = message[start_index:end_index]
            print(f":User  {user}")

        # Get List Name
        start_index = message.find('<') + 1  # Get the index right after '<'
        end_index = message.find('>')        # Get the index of '>'

        # Extract the name between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            list_name = message[start_index:end_index]
            print(f"List Name: {list_name}")
            listFilename = f'lists/{user}PersonalList{list_name}'

        clientSocket.send("ok".encode("UTF-8"))
        newmessage = clientSocket.recv(2048).decode('UTF-8')
        print(newmessage)
        if newmessage == 'addNewTasksToList items incoming':
            newmessage = clientSocket.recv(2048).decode('UTF-8')
            while newmessage != 'addNewTasksToList items finished':
                print('receiving', newmessage)
                items.append(newmessage)
                newmessage = clientSocket.recv(2048).decode('UTF-8')

            print(items)
            if not items:
                with open(listFilename, 'w') as file:
                    file.write('Add your items below' + '\n')
            else:
                print(items)
                open(listFilename, 'w').close()  # Reset file
                with open(listFilename, 'w') as file:
                    for item in items:
                        file.write(item + '\n')


########################################################################################################

    ## Get New Items For Family List
    if ']addNewTasksToFamilyList' in message:
        print ("Incoming addNewTasksToFamilyList request")

        previousItems = []
        
        with open (listFilename, 'r') as listFile:
                for line in listFile:
                    line = line.strip ()
                    previousItems.append (line)
        
        items = []
        start_index = message.find('[') + 1  # Get the index right after '<'
        end_index = message.find(']')        # Get the index of '>'
        # Extract the characters between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            family = message[start_index:end_index]
            print (f"Family: {family}")
         # Get List Name
        start_index = message.find('<') + 1  # Get the index right after '<'
        end_index = message.find('>')        # Get the index of '>'
        # Extract the number between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            list_name = message[start_index:end_index]
            print (f"List Name: {list_name}")
        listFilename = f'lists/{family}FamilyList{list_name}'

        clientSocket.send ("ok".encode ("UTF-8"))
        newmessage = clientSocket.recv(2048).decode('UTF-8')
        print (newmessage)
        if newmessage == 'addNewTasksToFamilyList items incoming':
           newmessage = clientSocket.recv(2048).decode('UTF-8')
           while newmessage != 'addNewTasksToFamilyList items finished':
                print ('receiving', newmessage)
                items.append (newmessage)
                newmessage = clientSocket.recv(2048).decode('UTF-8')

           if not items:
               with open (listFilename, 'w') as file:
                   for item in items:
                       file.write('Add your items below' + '\n')
           else:
               print (items)
               print (newmessage)
               open (listFilename, 'w').close () # Reset file
               with open (listFilename, 'w') as file:
                   for item in items:
                       file.write(item + '\n')
               


               differences = list(set(items) - set(previousItems))
               notifiable = []
               for item in differences:
                   if '|' in item:
                       notifiable.append (item)
                       print (f'Notifiable items: {notifiable}')
               for thing in notifiable:
                   task, user = thing.split('|')
                   task = task.strip()  # Remove any leading/trailing whitespace
                   user = user.strip()   # Remove any leading/trailing whitespace
                    
                   # Send the user and task to the client
                   notifSocket.send(f"notify<{user}>{task}".encode("UTF-8"))
                   print(f"sent: notify<{user}>{task}")

               
                    
               #with open ('sendNotification.py', 'r') as sendNotification:
                   #exec (sendNotification.read())
                


########################################################################################################

    ## Handle Login

    if 'login' in message:
        clientSocket.send("ready for login".encode("UTF-8"))

        message = clientSocket.recv(2048).decode('UTF-8')
        print (f"Username: {message}")
        username = message
        message = clientSocket.recv(2048).decode('UTF-8')
        print (f"Password: {message}")
        password = message


        def read_data(filename):
            data = []
            with open(filename, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header
                for row in csv_reader:
                    data.append(row)  # Append each row as a list
            return data


        data = read_data('stats.csv')
        found = False
        for row in data:
            if row[0] == simpleEncryption.decrypt(username, 3):
                found = True
                print(f"Data for {simpleEncryption.decrypt(username, 3)}:")
                print(f"Streak: {row[1]}")
                theirStreak = row[1]
                print(f"Points: {row[2]}")
                theirPoints = row[2]
                print(f"Date: {row[3]}")
                theirDate = row[3]
                print(f"Family: {row[4]}")
                theirFamily = row[4]
                break

        with open ('users', 'r') as users:
            if f"{username}◰{password}" in users.read ():
                print (f"Login for {username} successful!")
                clientSocket.send ('login successful'.encode("UTF-8"))
                time.sleep(0.1)
                clientSocket.send('data incoming'.encode("UTF-8"))
                time.sleep(0.1)
                clientSocket.send(theirStreak.encode("UTF-8"))
                time.sleep(0.1)
                clientSocket.send(theirPoints.encode("UTF-8"))
                time.sleep(0.1)
                clientSocket.send(theirDate.encode("UTF-8"))
                time.sleep(0.1)
                clientSocket.send(theirFamily.encode("UTF-8"))
            else:
                print (f"Login for {username} unsuccessful.")
                clientSocket.send ('login unsuccessful'.encode("UTF-8"))



########################################################################################################

    ## Handle Sign Up

    try:
        if 'sign up' in message:
            clientSocket.send("ready for sign up".encode("UTF-8"))

            message = clientSocket.recv(2048).decode('UTF-8')
            print (f"Username: {message}")
            username = message
            message = clientSocket.recv(2048).decode('UTF-8')
            print (f"Password: {message}")
            password = message

            # Read existing data

            def read_data(filename):
                data = []
                with open(filename, mode='r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)  # Skip the header
                    for row in csv_reader:
                        data.append(row)  # Append each row as a list
                return data

            data = read_data('stats.csv')
            print ('opened')
            today = datetime.today()
            currentDate = str(today.strftime('%Y%m%d'))
            new_entry = [simpleEncryption.decrypt(username, 3), '0', '0', currentDate, 'No Family']
            print (new_entry)
            # Insert the new entry in the correct position
            data.append(new_entry)
            data.sort(key=lambda x: x[0])  # Sort by name (first column)
            print('appended')

            # Write all data back to the CSV file
            with open('stats.csv', mode='w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['name', 'streak', 'points', 'date', 'family'])  # Write header
                csv_writer.writerows(data)  # Write all rows
                print('written')


            with open ('users', 'r') as users:
                if f"{username}◰{password}" not in users.read ():
                    with open('users', 'a') as users:
                        users.write (f"\n{username}◰{password}")
                        print (f"Sign up for {username} successful!")
                        clientSocket.send ('sign up successful'.encode("UTF-8"))
                        time.sleep (0.1)
                        clientSocket.send ('data incoming'.encode("UTF-8"))
                        time.sleep (0.1)
                        clientSocket.send ('0'.encode("UTF-8"))
                        time.sleep (0.1)
                        clientSocket.send ('0'.encode("UTF-8"))
                        time.sleep (0.1)
                        clientSocket.send (currentDate.encode("UTF-8"))
                        time.sleep (0.1)
                        clientSocket.send ('No Family'.encode("UTF-8"))
                else:
                    print (f"Sign up for {username} unsuccessful.")
                    clientSocket.send ('sign up unsuccessful'.encode("UTF-8"))

            

    except:
        pass

########################################################################################################

    ## Handle Get Number of Lists request


    if 'get number of lists' in message:
        clientSocket.send("ready to get number".encode("UTF-8"))
        print ("Got here")
        time.sleep (0.1)

        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"Username: {message}")
        username = message


        lists = 0

        filenames = next(os.walk('lists'), (None, None, []))[2]  # [] if no file
        for file in filenames:
            # Check if the filename contains '{username}PersonalList'
            if f'{username}PersonalList' in file:
                lists += 1
        clientSocket.send(str(lists).encode("UTF-8"))


########################################################################################################

    ## Handle Get Number of Family Lists request


    if 'get number of family lists' in message:
        clientSocket.send("ready to get number".encode("UTF-8"))

        message = clientSocket.recv(2048).decode('UTF-8')
        print (message)
        print(f"Family: {message}")
        family = message


        lists = 0

        filenames = next(os.walk('lists'), (None, None, []))[2]  # [] if no file
        for file in filenames:
            # Check if the filename contains '{username}PersonalList'
            if f'{family}FamilyList' in file:
                lists += 1
        clientSocket.send(str(lists).encode("UTF-8"))


########################################################################################################

    ## Create new list


    if 'create new list' in message:
        clientSocket.send("ready to create list".encode("UTF-8"))

        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"user: {message}")
        user = message

        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"user: {message}")
        number = message

        with open(f'lists/{user}PersonalList{number}', 'w') as file:
            file.write ("Add your items below")

        
########################################################################################################

    ## Create new family list


    if 'create new family list' in message:
        clientSocket.send("ready to create family list".encode("UTF-8"))

        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"family: {message}")
        family = message

        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"user: {message}")
        number = message

        with open(f'lists/{family}FamilyList{number}', 'w') as file:
            file.write ("Add your items below")

########################################################################################################

    ## Update user stats


    if 'send new data' in message:
        clientSocket.send("ready to receive data".encode("UTF-8"))
        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"username: {message}")
        username = message
        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"streak: {message}")
        streak = message
        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"points: {message}")
        points = message
        print ('points assigned. Now about to get date')
        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"date: {message}")
        date = message
        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"family: {message}")
        family = message


        # Read existing data
        def read_data(filename):
            data = []
            with open(filename, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip the header
                for row in csv_reader:
                    data.append(row)  # Append each row as a list
            return data


        # Update or append data
        def update_or_append_data(filename, username, streak, points, familyParam):
            data = read_data(filename)
            today = datetime.today()
            currentDate = str(today.strftime('%Y%m%d'))
            new_entry = [username, streak, points, currentDate, familyParam]

            # Check if the username already exists in the data
            updated = False
            for i, row in enumerate(data):
                if row[0] == username:  # Assuming the first column is the username
                    data[i] = new_entry  # Update the existing entry
                    updated = True
                    break

            if not updated:
                data.append(new_entry)  # Append the new entry if it doesn't exist

            # Sort data by name (first column)
            data.sort(key=lambda x: x[0])

            # Write all data back to the CSV file
            with open(filename, mode='w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['name', 'streak', 'points', 'date', 'family'])  # Write header
                csv_writer.writerows(data)  # Write all rows
                print('Data written to file.')


        update_or_append_data('stats.csv', username, streak, points, family)
        clientSocket.close ()
        clientSocket, address = s.accept ()


    ## Delete List
    if ']deleteList' in message:
        start_index = message.find('[') + 1  # Get the index right after '<'
        end_index = message.find(']')        # Get the index of '>'

        # Extract the characters between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            user = message[start_index:end_index]
    
        # Get List Number
        start_index = message.find('<') + 1  # Get the index right after '<'
        end_index = message.find('>')        # Get the index of '>'

        # Extract the number between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            number = message[start_index:end_index]
            listFilename = 'lists/' + user + 'PersonalList' + number

        try:
            # Check if the file exists before attempting to delete it
            if os.path.exists(listFilename):
                os.remove(listFilename)  # Delete the file
                print(f"{listFilename} has been deleted.")
                clientSocket.send ('deleted'.encode ("UTF-8"))
            else:
                print(f"The file {listFilename} does not exist.")
        except:
            clientSocket.send ('error'.encode ("UTF-8"))
                
########################################################################################################

        ## Delete Family List
    if ']deleteFamilyList' in message:
        start_index = message.find('[') + 1  # Get the index right after '<'
        end_index = message.find(']')        # Get the index of '>'

        # Extract the characters between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            family = message[start_index:end_index]
    
        # Get List Number
        start_index = message.find('<') + 1  # Get the index right after '<'
        end_index = message.find('>')        # Get the index of '>'

        # Extract the number between the brackets
        if start_index != -1 and end_index != -1 and start_index < end_index:
            number = message[start_index:end_index]
            listFilename = 'lists/' + family + 'FamilyList' + number

        try:
            # Check if the file exists before attempting to delete it
            if os.path.exists(listFilename):
                os.remove(listFilename)  # Delete the file
                print(f"{listFilename} has been deleted.")
                clientSocket.send ('deleted'.encode ("UTF-8"))
            else:
                print(f"The file {listFilename} does not exist.")
        except:
            clientSocket.send ('error'.encode ("UTF-8"))
                
########################################################################################################
    
    ## Handle Get names request


    if 'get list names' in message:
        clientSocket.send("ready to get names".encode("UTF-8"))
        time.sleep (0.1)

        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"Username: {message}")
        username = message

        def extract_personal_list(text):
            # Find the starting index of 'PersonalList'
            start_index = text.find('PersonalList')
            
            # If 'PersonalList' is found, extract the substring from the character after it
            if start_index != -1:
                return text[start_index + len('PersonalList'):]  # Start after 'PersonalList'
            else:
                return None  # or return an empty string if preferred

        allfilenames = next(os.walk('lists'), (None, None, []))[2]  # [] if no file
        ourfilenames = []
        for file in allfilenames:
            # Check if the filename contains '{username}PersonalList'
            if f'{username}PersonalList' in file:
                ourfilenames.append (file)


        for item in ourfilenames:
            clientSocket.send(extract_personal_list(item).encode("UTF-8"))
            print (f'sent: {item}')
            time.sleep (0.1)
        clientSocket.send('done'.encode("UTF-8"))


########################################################################################################

    ## Handle Get family names request


    if 'get family list names' in message:
        clientSocket.send("ready to get names".encode("UTF-8"))
        time.sleep (0.1)

        message = clientSocket.recv(2048).decode('UTF-8')
        print(f"Family: {message}")
        family = message

        def extract_family_list(text):
            # Find the starting index of 'FamilyList'
            start_index = text.find('FamilyList')
            
            # If 'FamilyList' is found, extract the substring from the character after it
            if start_index != -1:
                return text[start_index + len('FamilyList'):]  # Start after 'FamilyList'
            else:
                return None  # or return an empty string if preferred

        allfilenames = next(os.walk('lists'), (None, None, []))[2]  # [] if no file
        ourfilenames = []
        for file in allfilenames:
            # Check if the filename contains '{family}FamilyList'
            if f'{family}FamilyList' in file:
                ourfilenames.append (file)


        for item in ourfilenames:
            clientSocket.send(extract_family_list(item).encode("UTF-8"))
            print (f'sent: {item}')
            time.sleep (0.1)
        clientSocket.send('done'.encode("UTF-8"))


########################################################################################################

        ## Rename Personal List
    if 'rename personal list' in message:
        clientSocket.send ('ready to rename list'.encode('UTF-8'))
        username = clientSocket.recv(2048).decode('UTF-8')
        currentName = clientSocket.recv(2048).decode('UTF-8')
        newName = clientSocket.recv(2048).decode('UTF-8')

        def renameFile(username, currentName, newName):
            # Construct the current file name
            currentFileName = f"{username}PersonalList{currentName}"
            # Define the path to the file
            filePath = os.path.join('lists', currentFileName)
            
            # Check if the file exists
            if os.path.isfile(filePath):
                # Construct the new file name
                newFileName = f"{username}PersonalList{newName}"
                newFilePath = os.path.join('lists', newFileName)
                
                # Rename the file
                os.rename(filePath, newFilePath)
                print(f"File renamed from {currentFileName} to {newFileName}")
            else:
                print(f"File {currentFileName} does not exist in the 'lists/' directory.")

        renameFile(username, currentName, newName)
        
                
########################################################################################################
    
        ## Rename Family List
    if 'rename family list' in message:
        clientSocket.send ('ready to rename list'.encode('UTF-8'))
        family = clientSocket.recv(2048).decode('UTF-8')
        currentName = clientSocket.recv(2048).decode('UTF-8')
        newName = clientSocket.recv(2048).decode('UTF-8')

        def renameFile(family, currentName, newName):
            # Construct the current file name
            currentFileName = f"{family}FamilyList{currentName}"
            # Define the path to the file
            filePath = os.path.join('lists', currentFileName)
            
            # Check if the file exists
            if os.path.isfile(filePath):
                # Construct the new file name
                newFileName = f"{family}FamilyList{newName}"
                newFilePath = os.path.join('lists', newFileName)
                
                # Rename the file
                os.rename(filePath, newFilePath)
                print(f"File renamed from {currentFileName} to {newFileName}")
            else:
                print(f"File {currentFileName} does not exist in the 'lists/' directory.")

        renameFile(family, currentName, newName)
        listFilename = f"lists/{family}FamilyList{newName}"
        
                
########################################################################################################
    


        
clientSocket.close ()   
