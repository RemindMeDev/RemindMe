# RemindMe v1.1
# © William George 2025

import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import messagebox as mb
from PIL import Image
import socket, time, sys, subprocess
import simpleEncryption

delete_image = ctk.CTkImage(Image.open("deleteicon.png"))

with open ('user', 'r') as userFileToRead:
    usernameTest = userFileToRead.read()

with open('streak', 'r') as streak:
    streak = streak.read()

with open('user', 'r') as user:
    getUsername = user.read()

with open('family', 'r') as familyFile:
    getFamily = familyFile.read()
if getFamily == '':
    with open('family', 'w') as familyFile:
        familyFile.write('No Family')

global s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 6060)) # Connect to the server
print (f'socket details: {s}')


def clear_window(window):
    # Iterate through all widgets in the window and destroy them
    for widget in window.winfo_children():
        widget.destroy()


def loadingCursor(boolean):
    if boolean:
        app.config(cursor='watch')
    if not boolean:
        app.config(cursor='arrow')


with open ('chosenTheme', 'r') as chosenTheme:
    chosenTheme = chosenTheme.read()
ctk.set_appearance_mode(chosenTheme)


with open ('chosenColourTheme', 'r') as chosenColourTheme:
    chosenColourTheme = chosenColourTheme.read()
ctk.set_default_color_theme(chosenColourTheme)


with open ('streak', 'r') as streak:
    streak = streak.read()

with open ('user', 'r') as user:
    getUsername = user.read()

with open ('family', 'r') as familyFile:
    getFamily = familyFile.read()





## Streak code

# Read the streak date from the file
with open('streak', 'r') as streakFile:
    streak = streakFile.read()
    print (f'read: {streak}')
    if streak != '':
        #streak = streak # Why does this line exist??
        print (f'streak: {streak}')
    else:
        print ("Starting streak")
        today = datetime.today().strftime('%Y%m%d')
        with open('streak', 'w') as streakFile:
            streakFile.write(today)
        streak = today


with open ('streakAmount', 'r') as streakAmountFile:
    streakAmount = int(streakAmountFile.read())
    print (f'streakAmount: {streakAmount}')


def format_string(input_string):
    # Replace underscores with spaces
    modified_string = input_string

    # Remove the .json extension if it exists
    if modified_string.endswith('.json'):
        modified_string = modified_string[:-5]  # Remove the last 5 characters ('.json')

    # Capitalize the first letter of each word
    formatted_string = modified_string.title()

    return formatted_string


def format_other_string(input_string):
    # Replace hyphens with spaces
    modified_string = input_string

    # Remove the .json extension if it exists
    if modified_string.endswith('.json'):
        modified_string = modified_string[:-5]  # Remove the last 5 characters ('.json')

    # Capitalize the first letter of each word
    formatted_string = modified_string.title()

    return formatted_string


# Get today's date
today = datetime.today()
currentDate = int(today.strftime('%Y%m%d'))
print (f'current date: {currentDate}')

# Calculate yesterday's date
yesterday = today - timedelta(days=1)
yesterdayDate = int(yesterday.strftime('%Y%m%d'))
print (f'yesterday date: {yesterdayDate}')

# Check the streak
if int(yesterdayDate) == int(streak):
    print('Streak continued')
    streakAmount += 1
    print (f'streak amount: {streakAmount}')
    with open('streakAmount', 'w') as streakAmountFile:
        streakAmountFile.write (str(streakAmount))
    streak = today.strftime('%Y%m%d')
    print (streak)
    with open('streak', 'w') as streakFile:
        streakFile.write (streak)

elif int(currentDate) == int(streak):
    print("Was today")

elif int(currentDate) - int(streak) >= 2:
    print("Streak expired")
    streak = today.strftime('%Y%m%d')
    with open('streak', 'w') as streakFile:
        streakFile.write(streak)
    with open('streakAmount', 'w') as streakAmountFile:
        streakAmountFile.write ('0')
        streakAmount = 0

else:
    print ("ERROR: Streak out of range")


## Get points
with open ('points', 'r') as pointsFile:
    points = int(pointsFile.read())


def sendNewData(close):
    # Connect to the server
    s.send('send new data'.encode('UTF-8'))  # Send login message
    message = s.recv(2048).decode('UTF-8')  # Receive response
    print('asked')
    if message == 'ready to receive data':  # If the server is ready
        print("Connection successful")  # Print success message

        with open('points', 'r') as pointsFile:
            pointsAmount = pointsFile.read()



        s.send(getUsername.encode('UTF-8'))
        print(f'sent {getUsername}')
        time.sleep(0.1)
        s.send(str(streakAmount).encode('UTF-8'))
        print(f'sent {streakAmount}')
        time.sleep(0.1)
        s.send(str(pointsAmount).encode('UTF-8'))
        print(f'sent {pointsAmount}')
        time.sleep(0.1)
        dateToSend = str(today.strftime('%Y%m%d'))
        print(dateToSend)
        s.send(dateToSend.encode("utf-8"))
        time.sleep (0.1)
        print(f'sent {dateToSend}')
        s.send(getFamily.encode("utf-8"))
        print(f'sent {getFamily}')

        if close:
            listener_process.terminate()
            listener_process.wait()
            s.close()
            try:
                app.destroy()
            except:
                sys.exit(1)


def createnewlist():
    # Connect to the server
    s.send('create new list'.encode('UTF-8'))  # Send login message
    message = s.recv(2048).decode('UTF-8')  # Receive response
    if message == 'ready to create list':  # If the server is ready for login
        print("Connection successful")  # Print success message
        s.send(getUsername.encode('UTF-8'))  # Send login message
        time.sleep(0.1)
        s.send(str(listNumber + 1).encode('UTF-8'))  # Send login message
        print("SHOW NEW LIST")

    clear_window(app)
    drawHomeElements()


def createnewflist():
    with open('family', 'r') as family:
        getFamily = family.read()
    if getFamily != 'No Family':
        print(getFamily)

        # Connect to the server
        s.send('create new family list'.encode('UTF-8'))  # Send login message
        message = s.recv(2048).decode('UTF-8')  # Receive response
        if message == 'ready to create family list':  # If the server is ready for login
            print("Connection successful")  # Print success message
            s.send(getFamily.encode('UTF-8'))  # Send login message
            time.sleep(0.1)
            s.send(str(familyListNumber + 1).encode('UTF-8'))  # Send login message
            print("SHOW NEW LIST")

            clear_window(app)
            drawHomeElements()
    else:
        print("You can't make a list with no family.")
        print(getFamily)
        mb.showerror(title="Warning", message="No family is set. Please enter your family name in the user settings.")


def viewList(number):
    edit_buttons = []

    class EditButton (ctk.CTkButton):
        def __init__(self, capturedN):
            super().__init__(frame, text="Edit", command=lambda n=n: editItemButton(n), width=15)
            self.grid (row=capturedN + 1, column=1, padx=20, pady=10)
            self.value = capturedN
            edit_buttons.append(self)

        def remove (self):
            self.destroy ()



    clear_window(app)
    loadingCursor(True)

    with open('currentList', 'w') as currentList:
        currentList.write(str(number))

    with open('chosenTheme', 'r') as chosenTheme:
        chosenTheme = chosenTheme.read()
    ctk.set_appearance_mode(chosenTheme)

    with open('chosenColourTheme', 'r') as chosenColourTheme:
        chosenColourTheme = chosenColourTheme.read()
    ctk.set_default_color_theme(chosenColourTheme)

    with open('user', 'r') as username:
        username = username.read()

    items = []

    def getItems(list_name):
        # This gets tasks from our temporary file and adds them to an array
        string = "[" + username + "]" + "getTasksFromList<" + list_name + ">"
        s.send(string.encode('UTF-8'))
        message = s.recv(2048).decode('UTF-8')
        print(message)
        if message == 'getTasksFromList items incoming':
            message = s.recv(2048).decode('UTF-8')
            while message != 'getTasksFromList items finished':
                print('receiving', message)
                items.append(message)
                message = s.recv(2048).decode('UTF-8')
            print(items)
            print(message)

    def newItemEntry():
        global itemEntry
        itemEntry = ctk.CTkEntry(frame, placeholder_text="Enter new task", height=35, font=("Roboto", 15))
        itemEntry.grid(row=len(items) + 1, column=0, padx=20, pady=10)
        itemEntry.bind('<Return>', getEntry)
        itemEntry.focus()
        print(items)

    def getEntry(event):
        if len(itemEntry.get()) > 43:
            mb.showerror("Item too long", "Your item should be less than 44 characters long.")
        elif itemEntry.get() == '':
            mb.showerror("No item entered", "Please enter at least one character.")
        else:
            items.append(itemEntry.get())
            populateList()
            itemEntry.delete(0, ctk.END)
            itemEntry.grid(row=len(items) + 1, column=0, padx=20, pady=10)
            addButton.grid(row=len(items) + 1, column=1, padx=20, pady=10)
            closeButton.grid(row=len(items) + 2, column=0, padx=20, pady=10)
            renameButton.grid(row=len(items) + 3, column=0, padx=20, pady=10)

    def sendNewList(list_name):
        if itemEntry.get() != '':
            getEntry("placeholder")

        with open('user', 'r') as username:
            user = username.read()
        with open('points', 'r') as pointsFile:
            points = pointsFile.read()

        string = "[" + user + "]" + "addNewTasksToList<" + list_name + ">"
        s.send(string.encode('UTF-8'))
        message = s.recv(2048).decode('UTF-8')
        if message == 'ok':
            s.send("addNewTasksToList items incoming".encode("UTF-8"))
            time.sleep(0.1)
            for item in items:
                print('sending', item)
                s.send(item.encode("UTF-8"))
                time.sleep(0.1)
            time.sleep(0.1)
            s.send("addNewTasksToList items finished".encode("UTF-8"))

        clear_window(app)
        drawHomeElements()

    check_boxes = []


    def populateList():
        # Clear existing checkboxes
        for cb in check_boxes:
            cb.destroy()
        for eb in edit_buttons:
            eb.remove()
        check_boxes.clear()

        # Create new checkboxes
        global n
        for n in range(len(items)):
            check_var = ctk.StringVar(value="off")
            cb = ctk.CTkCheckBox(frame, text=items[n], command=lambda n=n: completeTask(n), variable=check_var,
                                 onvalue="on", offvalue="off")
            cb.grid(row=n + 1, column=0, padx=20, pady=10,sticky='w')
            check_boxes.append(cb)
            EditButton(n)

    def completeTask(item):
        print('Completed task ' + str(item) + " which was " + items[item])
        items.remove(items[item])  # Remove the item from the list
        print(items)
        populateList()  # Refresh the list of checkboxes
        if items[item] != 'Add your items below':
            with open('points', 'r') as pointsFile:
                points = int(pointsFile.read())
            points += 1
            with open('points', 'w') as pointsFile:
                pointsFile.write(str(points))

    edit_widgets = {}

    def editItemButton(item):
        for cb in check_boxes:
            cb.configure(state='disabled')
        text = items[item]
        for button in edit_buttons:
            if button.value == item:
                button.remove()

        # Create the entry field
        editEntry = ctk.CTkEntry(frame, placeholder_text=text, width=200)
        editEntry.grid(row=item + 1, column=0, padx=20, pady=10)
        editEntry.bind('<Return>',
                       lambda event, n=item, entry=editEntry: editItem(n, entry.get(), editEntry, confirmButton))

        # Create the confirm button
        confirmButton = ctk.CTkButton(frame, text="Confirm",command=lambda n=item,
                                        entry=editEntry: editItem(n, entry.get(), editEntry, confirmButton), width=15)
        confirmButton.grid(row=item + 1, column=1, padx=20, pady=10)

        # Store references to the editEntry and confirmButton
        edit_widgets[item] = (editEntry, confirmButton)

    def editItem(item, newValue, editEntry, confirmButton):
        print(f'Editing {items[item]} to {newValue}')
        if newValue != '':
            items[item] = newValue
        else:
            newValue = items[item]
        # Destroy the editEntry and confirmButton
        editEntry.destroy()
        confirmButton.destroy()
        del edit_widgets[item]
        check_boxes[item].configure(text=newValue)
        populateList()
        for cb in check_boxes:
            cb.configure(state='normal')


    def closeButton():
        with open('currentList', 'r') as currentList:
            currentList_name = currentList.read()
        sendNewList(currentList_name)


    def renameListEntry ():
        global nameEntry, confirmButton
        nameEntry = ctk.CTkEntry(frame, placeholder_text="Enter new name")
        nameEntry.grid(row=len(items) + 4, column=0, padx=20, pady=10, columnspan=2)
        confirmButton = ctk.CTkButton(frame, text="Confirm", command=lambda: renameList(nameEntry.get()))
        confirmButton.grid(row=len(items) + 5, column=0, padx=20, pady=10, columnspan=2)


    def renameList(new_name):
        if len(new_name) > 13:
            mb.showerror("Name too long", "Your list name should be less than 14 characters long.")
        elif new_name == '':
            mb.showerror("No name entered", "Please enter at least one character for a list name.")
        else:
            with open('currentList', 'r') as currentListFile:
                currentList = currentListFile.read()
            s.send('rename personal list'.encode('UTF-8'))  # Send login message
            message = s.recv(2048).decode('UTF-8')  # Receive response
            if message == 'ready to rename list':  # If the server is ready for login
                print("Connection successful")  # Print success message
                s.send(username.encode('UTF-8'))  # Send login message
                time.sleep(0.1)
                s.send(currentList.encode('UTF-8'))
                time.sleep (0.1)
                s.send (new_name.encode('UTF-8'))
            with open('currentList', 'w') as currentList:
                currentList.write(new_name)
            welcome.configure(text=new_name)  # Update the displayed list name
            nameEntry.destroy()
            confirmButton.destroy()

    title = ctk.CTkLabel(app, text="RemindMe", font=("Roboto", 30, "bold"))
    title.grid(row=0, column=0, padx=20, pady=20)

    frame = ctk.CTkScrollableFrame(app, width=xSize - 100, height=ySize - 120, corner_radius=20)
    frame.grid(row=1, column=0, padx=20, pady=20)

    frame.grid_columnconfigure(0, weight=1)

    with open('currentList', 'r') as currentList:
        currentList_name = currentList.read()

    getItems(currentList_name)
    populateList()
    print(items)

    itemEntry = ctk.CTkEntry(frame, placeholder_text="Enter new task", height=35, font=("Roboto", 15), width=400)
    itemEntry.grid(row=n + 2, column=0, padx=20, pady=10,columnspan=2)
    itemEntry.bind('<Return>', getEntry)

    addButton = ctk.CTkButton(frame, text="+", command=lambda: [getEntry("placeholder")], width=15, font=("Roboto", 25))
    addButton.grid(row=n + 2, column=1, padx=20, pady=10)

    welcome = ctk.CTkLabel(frame, text=currentList_name, font=("Roboto", 25, "bold"))
    welcome.grid(row=0, column=0, padx=100, pady=10,columnspan=2)

    closeButton = ctk.CTkButton(frame, text="Save and Close", command=closeButton)
    closeButton.grid(row=len(items) + 2, column=0, padx=20, pady=10,columnspan=2)

    renameButton = ctk.CTkButton(frame, text="Rename List",
                                 command=lambda: renameListEntry(), fg_color='green', hover_color='#006311', text_color='white')
    renameButton.grid(row=len(items) + 3, column=0, padx=20, pady=10,columnspan=2)

    loadingCursor(False)


def deleteList (number):
    result = mb.askyesno(title="Delete List", message="Are you sure you want to delete this list?", icon=mb.QUESTION)
    if result:
        string = "[" + usernameTest + "]" + "deleteList<" + str(number) + ">"
        s.send(string.encode('UTF-8'))
        message = s.recv(2048).decode('UTF-8')
        if message == 'deleted':
            clear_window(app)
            drawHomeElements()
        elif message == 'error':
            print ("ERROR: Could not delete")
    else:
        pass

def deleteFamilyList (number):
    result = mb.askyesno(title="Delete List", message="Are you sure you want to delete this list?", icon=mb.QUESTION)
    if result:
        string = "[" + getFamily + "]" + "deleteFamilyList<" + str(number) + ">"
        s.send(string.encode('UTF-8'))
        message = s.recv(2048).decode('UTF-8')
        if message == 'deleted':
            clear_window(app)
            drawHomeElements()
        elif message == 'error':
            print ("ERROR: Could not delete")
    else:
        pass


def viewFamilyList(number):
    edit_buttons = []

    class EditButton(ctk.CTkButton):
        def __init__(self, capturedN):
            super().__init__(frame, text="Edit", command=lambda n=n: editItemButton(n), width=15)
            self.grid(row=capturedN + 1, column=1, padx=20, pady=10)
            self.value = capturedN
            edit_buttons.append(self)

        def remove(self):
            self.destroy()



    clear_window(app)
    loadingCursor(True)

    with open('currentFamilyList', 'w') as currentFamilyList:
        currentFamilyList.write(str(number))

    with open('chosenTheme', 'r') as chosenTheme:
        chosenTheme = chosenTheme.read()
    ctk.set_appearance_mode(chosenTheme)

    with open('chosenColourTheme', 'r') as chosenColourTheme:
        chosenColourTheme = chosenColourTheme.read()
    ctk.set_default_color_theme(chosenColourTheme)

    with open('family', 'r') as family:
        family = family.read()

    items = []

    def getItems(list_name):
        string = "[" + family + "]" + "getTasksFromFamilyList<" + list_name + ">"
        s.send(string.encode('UTF-8'))
        message = s.recv(2048).decode('UTF-8')
        print(message)
        if message == 'getTasksFromFamilyList items incoming':
            message = s.recv(2048).decode('UTF-8')
            while message != 'getTasksFromFamilyList items finished':
                print('receiving', message)
                items.append(message)
                message = s.recv(2048).decode('UTF-8')
            print(items)
            print(message)

    def newItemEntry():
        global itemEntry
        itemEntry = ctk.CTkEntry(frame, placeholder_text="Enter new task", height=35, font=("Roboto", 15))
        itemEntry.grid(row=len(items) + 1, column=0, padx=20, pady=10)
        itemEntry.bind('<Return>', getEntry)
        itemEntry.focus()

    def getEntry(event):
        if len(itemEntry.get()) > 43:
            mb.showerror("Item too long", "Your item should be less than 44 characters long.")
        elif itemEntry.get() == '':
            mb.showerror("No item entered", "Please enter at least one character.")
        else:
            items.append(itemEntry.get())
            populateList()
            itemEntry.delete(0, ctk.END)
            itemEntry.grid(row=len(items) + 1, column=0, padx=20, pady=10)
            addButton.grid(row=len(items) + 1, column=1, padx=20, pady=10)
            closeButton.grid(row=len(items) + 2, column=0, padx=20, pady=10)
            renameButton.grid(row=len(items) + 3, column=0, padx=20, pady=10)


    check_boxes = []

    def populateList():
        # Clear existing checkboxes
        for cb in check_boxes:
            cb.destroy()
        check_boxes.clear()
        for eb in edit_buttons:
            eb.remove ()

        # Create new checkboxes
        global n
        for n in range(len(items)):
            check_var = ctk.StringVar(value="off")
            cb = ctk.CTkCheckBox(frame, text=items[n], command=lambda n=n: completeTask(n), variable=check_var,
                                 onvalue="on", offvalue="off")
            cb.grid(row=n + 1, column=0, padx=20, pady=10, sticky='w')
            check_boxes.append(cb)
            EditButton(n)

    def completeTask(item):
        print('Completed task ' + str(item) + " which was " + items[item])
        items.remove(items[item])  # Remove the item from the list
        print(items)
        populateList()  # Refresh the list of checkboxes
        if items[item] != 'Add your items below':
            with open('points', 'r') as pointsFile:
                points = int(pointsFile.read())
            points += 1
            with open('points', 'w') as pointsFile:
                pointsFile.write(str(points))

    edit_widgets = {}

    def editItemButton(item):
        for cb in check_boxes:
            cb.configure(state='disabled')
        text = items[item]
        for button in edit_buttons:
            if button.value == item:
                button.remove()

        # Create the entry field
        editEntry = ctk.CTkEntry(frame, placeholder_text=text, width=200)
        editEntry.grid(row=item + 1, column=0, padx=20, pady=10)
        editEntry.bind('<Return>',
                       lambda event, n=item, entry=editEntry: editItem(n, entry.get(), editEntry, confirmButton))

        # Create the confirm button
        confirmButton = ctk.CTkButton(frame, text="Confirm",command=lambda n=item,
                                        entry=editEntry: editItem(n, entry.get(), editEntry, confirmButton), width=15)
        confirmButton.grid(row=item + 1, column=1, padx=20, pady=10)

        # Store references to the editEntry and confirmButton
        edit_widgets[item] = (editEntry, confirmButton)

    def editItem(item, newValue, editEntry, confirmButton):
        print(f'Editing {items[item]} to {newValue}')
        if newValue != '':
            items[item] = newValue
        else:
            newValue = items[item]
        # Destroy the editEntry and confirmButton
        editEntry.destroy()
        confirmButton.destroy()
        del edit_widgets[item]
        check_boxes[item].configure(text=newValue)
        populateList()
        for cb in check_boxes:
            cb.configure(state='normal')

    def sendNewList(list_name):
        if itemEntry.get () != '':
            getEntry ("placeholder")

        with open('family', 'r') as familyname:
            family = familyname.read()
        with open('points', 'r') as pointsFile:
            points = pointsFile.read()

        string = "[" + family + "]" + "addNewTasksToFamilyList<" + list_name + ">"
        s.send(string.encode('UTF-8'))
        message = s.recv(2048).decode('UTF-8')
        if message == 'ok':
            s.send("addNewTasksToFamilyList items incoming".encode("UTF-8"))
            time.sleep(0.1)
            for item in items:
                print('sending', item)
                s.send(item.encode("UTF-8"))
                time.sleep(0.1)
            time.sleep(0.1)
            s.send("addNewTasksToFamilyList items finished".encode("UTF-8"))
        clear_window(app)
        drawHomeElements()

    def closeButton():
        with open('currentFamilyList', 'r') as currentList:
            currentList = currentList.read()
        sendNewList(currentList)

    def renameListEntry():
        global nameEntry, confirmButton
        nameEntry = ctk.CTkEntry(frame, placeholder_text="Enter new name")
        nameEntry.grid(row=len(items) + 4, column=0, padx=20, pady=10, columnspan=2)
        confirmButton = ctk.CTkButton(frame, text="Confirm", command=lambda: renameList(nameEntry.get()))
        confirmButton.grid(row=len(items) + 5, column=0, padx=20, pady=10, columnspan=2)

    def renameList(new_name):
        if len(new_name) > 13:
            mb.showerror("Name too long", "Your list name should be less than 14 characters long.")
        elif new_name == '':
            mb.showerror("No name entered", "Please enter at least one character for a list name.")
        else:
            with open('currentFamilyList', 'r') as currentFamilyListFile:
                currentFamilyList = currentFamilyListFile.read()
            s.send('rename family list'.encode('UTF-8'))  # Send login message
            message = s.recv(2048).decode('UTF-8')  # Receive response
            if message == 'ready to rename list':  # If the server is ready for login
                print("Connection successful")  # Print success message
                s.send(family.encode('UTF-8'))  # Send login message
                time.sleep(0.1)
                s.send(currentFamilyList.encode('UTF-8'))
                time.sleep(0.1)
                s.send(new_name.encode('UTF-8'))
            with open('currentFamilyList', 'w') as currentFamilyListFile:
                currentFamilyListFile.write(new_name)
            welcome.configure(text=new_name)  # Update the displayed list name
            nameEntry.destroy()
            confirmButton.destroy()


    title = ctk.CTkLabel(app, text="RemindMe", font=("Roboto", 30, "bold"))
    title.grid(row=0, column=0, padx=20, pady=20)

    frame = ctk.CTkScrollableFrame(app, width=xSize - 100, height=ySize - 120, corner_radius=20)
    frame.grid(row=1, column=0, padx=20, pady=20)
    # frame.grid_propagate(0)

    frame.grid_columnconfigure(0, weight=1)
    # frame.grid_rowconfigure(1, weight=1)

    with open('currentFamilyList', 'r') as currentFamilyList:
        currentFamilyList = currentFamilyList.read()

    getItems(currentFamilyList)
    populateList()
    print(items)

    itemEntry = ctk.CTkEntry(frame, placeholder_text="Enter new task", height=35, font=("Roboto", 15), width=400)
    itemEntry.grid(row=n + 2, column=0, padx=20, pady=10, columnspan=2)
    itemEntry.bind('<Return>', getEntry)

    addButton = ctk.CTkButton(frame, text="+", command=lambda: [getEntry("placeholder")], width=15, font=("Roboto", 25))
    addButton.grid(row=n + 2, column=1, padx=20, pady=10)

    welcome = ctk.CTkLabel(frame, text=currentFamilyList, font=("Roboto", 25, "bold"))
    welcome.grid(row=0, column=0, padx=100, pady=10, columnspan=2)

    closeButton = ctk.CTkButton(frame, text="Save and Close", command=closeButton)
    closeButton.grid(row=len(items) + 2, column=0, padx=20, pady=10, columnspan=2)

    #renameButton = ctk.CTkButton(frame, text="Rename List", command=lambda: renameListEntry(), fg_color='green', hover_color='#006311', text_color='white')
    renameButton = ctk.CTkButton(frame, text="Rename List",
                                 command=lambda: renameListEntry(), fg_color='green', hover_color='#006311', text_color='white')
    renameButton.grid(row=len(items) + 3, column=0, padx=20, pady=10, columnspan=2)

    loadingCursor(False)


def userSettings():
    clear_window(app)
    loadingCursor(True)

    with open('chosenTheme', 'r') as chosenTheme:
        chosenTheme = chosenTheme.read()
    ctk.set_appearance_mode(chosenTheme)

    with open('chosenColourTheme', 'r') as chosenColourTheme:
        chosenColourTheme = chosenColourTheme.read()
    ctk.set_default_color_theme(chosenColourTheme)

    def changeTheme(choice):
        with open('chosenTheme', 'w') as chosenTheme:
            chosenTheme.write(choice)
        ctk.set_appearance_mode(choice)

    def changeColourTheme(choice):
        with open('chosenColourTheme', 'w') as chosenColourTheme:
            if choice == 'Blue':
                ctk.set_default_color_theme('blue')
                chosenColourTheme.write('blue')
            elif choice == 'Dark Blue':
                ctk.set_default_color_theme('dark-blue')
                chosenColourTheme.write('dark-blue')
            elif choice == 'Green':
                ctk.set_default_color_theme('green')
                chosenColourTheme.write('green')
            elif choice == 'Dark Red':
                ctk.set_default_color_theme('dark_red.json')
                chosenColourTheme.write('dark_red.json')
            elif choice == 'Yellow':
                ctk.set_default_color_theme('yellow.json')
                chosenColourTheme.write('yellow.json')
            elif choice == 'Pink':
                ctk.set_default_color_theme('pink.json')
                chosenColourTheme.write('pink.json')
            elif choice == 'Red':
                ctk.set_default_color_theme('red.json')
                chosenColourTheme.write('red.json')
            elif choice == 'Orange':
                ctk.set_default_color_theme('orange.json')
                chosenColourTheme.write('orange.json')
            elif choice == 'Dark Purple':
                ctk.set_default_color_theme('dark_purple.json')
                chosenColourTheme.write('dark_purple.json')
            elif choice == 'Purple':
                ctk.set_default_color_theme('purple.json')
                chosenColourTheme.write('purple.json')
            elif choice == 'Light Blue':
                ctk.set_default_color_theme('light_blue.json')
                chosenColourTheme.write('light_blue.json')
            elif choice == 'Turqoise':
                ctk.set_default_color_theme('turqoise.json')
                chosenColourTheme.write('turqoise.json')
        clear_window(app)
        userSettings ()

    def setFamilyName():
        name = familyEntry.get()
        with open('family', 'w') as family:
            family.write(name)
        familyEntry.delete(0, ctk.END)
        mb.showinfo(title="Name Changed", message=f"Family name set to {name}")
        clear_window(app)
        drawHomeElements()
        with open('showNewList.py', 'r') as file:
            exec(file.read())

    def signOut():
        sendNewData(True)
        with open('user', 'w') as user:
            user.write('')
        with open('family', 'w') as family:
            family.write('No Family')
        with open('streak', 'w') as streak:
            streak.write('')
        with open('chosenColourTheme', 'w') as streak:
            streak.write('blue')
        clear_window(app)
        drawHomeElements()

    def saveSettings():
        clear_window(app)
        drawHomeElements()

    title = ctk.CTkLabel(app, text="RemindMe", font=("Roboto", 30, "bold"))
    title.grid(row=0, column=0, padx=20, pady=20)

    frame = ctk.CTkFrame(master=app, width=xSize - 100, height=ySize - 120, corner_radius=20)
    frame.grid(row=1, column=0, padx=20, pady=20)
    frame.grid_propagate(0)
    frame.grid_columnconfigure(0, weight=1)

    settings = ctk.CTkLabel(frame, text="Settings", font=("Roboto", 25, "bold"))
    settings.grid(row=0, column=0, padx=10, pady=10)

    themeLabel = ctk.CTkLabel(frame, text="Theme", font=("Roboto", 20))
    themeLabel.grid(row=1, column=0, padx=10)

    themeMenu = ctk.CTkOptionMenu(frame, values=["Dark", "Light", "System"], command=changeTheme)
    themeMenu.set(chosenTheme)
    themeMenu.grid(row=2, column=0, padx=10, pady=10)

    colourThemeLabel = ctk.CTkLabel(frame, text="Colour Theme", font=("Roboto", 20))
    colourThemeLabel.grid(row=3, column=0, padx=10, pady=10)

    ColourThemeMenu = ctk.CTkOptionMenu(frame, values=["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Pink",
                                                       "Dark Red", "Dark Blue", "Dark Purple", "Light Blue",
                                                       "Turqoise"], command=changeColourTheme)
    if '.json' in chosenColourTheme:
        ColourThemeMenu.set(format_string(chosenColourTheme))
    elif '-' in chosenColourTheme:
        ColourThemeMenu.set(format_other_string(chosenColourTheme))
    else:
        ColourThemeMenu.set(chosenColourTheme.capitalize())
    ColourThemeMenu.grid(row=4, column=0, padx=10, pady=10)


    signoutButton = ctk.CTkButton(frame, text="Sign Out", command=signOut)
    signoutButton.grid(row=7, column=0, padx=10, pady=10)

    setButton = ctk.CTkButton(frame, text="Save Settings", command=saveSettings)
    setButton.grid(row=6, column=0, padx=10, pady=10)

    loadingCursor(False)


def viewFamilySettings():
    clear_window(app)
    loadingCursor(True)

    with open('chosenTheme', 'r') as chosenTheme:
        chosenTheme = chosenTheme.read()
    ctk.set_appearance_mode(chosenTheme)

    with open('chosenColourTheme', 'r') as chosenColourTheme:
        chosenColourTheme = chosenColourTheme.read()
    ctk.set_default_color_theme(chosenColourTheme)

    def saveSettings():
        clear_window(app)
        drawHomeElements()

    def setFamilyName():
        name = familyEntry.get()
        with open('family', 'w') as family:
            family.write(name)
        familyEntry.delete(0, ctk.END)
        mb.showinfo(title="Name Changed", message=f"Family name set to {name}")
        clear_window(app)
        drawHomeElements()

    def setFamilyName2():
        name = familyEntry2.get()
        with open('family', 'w') as family:
            family.write(name)
        familyEntry.delete(0, ctk.END)
        mb.showinfo(title="Name Changed", message=f"Family name set to {name}")
        clear_window(app)
        drawHomeElements()

    title = ctk.CTkLabel(app, text="RemindMe", font=("Roboto", 30, "bold"))
    title.grid(row=0, column=0, padx=20, pady=20)

    frame = ctk.CTkFrame(master=app, width=xSize - 100, height=ySize - 120, corner_radius=20)
    frame.grid(row=1, column=0, padx=20, pady=20)
    frame.grid_propagate(0)
    frame.grid_columnconfigure(0, weight=1)

    settings = ctk.CTkLabel(frame, text="Family Settings", font=("Roboto", 25, "bold"))
    settings.grid(row=0, column=0, padx=10, pady=10)

    currentFamily = ctk.CTkLabel(frame, text=f"Current Family: {getFamily}", font=("Roboto", 15))
    currentFamily.grid(row=1, column=0, padx=20)

    familyLabel = ctk.CTkLabel(frame, text="Create a new family:", font=("Roboto", 20))
    familyLabel.grid(row=2, column=0, padx=20)

    familyEntry = ctk.CTkEntry(frame, placeholder_text="Family Username", height=35, font=("Roboto", 15))
    familyEntry.grid(row=3, column=0, padx=10, pady=10)

    setFamilyButton = ctk.CTkButton(frame, text="Create", command=setFamilyName)
    setFamilyButton.grid(row=4, column=0, padx=10, pady=10)

    familyLabel2 = ctk.CTkLabel(frame, text="Join an existing family:", font=("Roboto", 20))
    familyLabel2.grid(row=5, column=0, padx=20)

    familyEntry2 = ctk.CTkEntry(frame, placeholder_text="Family Username", height=35, font=("Roboto", 15))
    familyEntry2.grid(row=6, column=0, padx=10, pady=10)

    setFamilyButton2 = ctk.CTkButton(frame, text="Join", command=setFamilyName2)
    setFamilyButton2.grid(row=7, column=0, padx=10, pady=10)

    setButton = ctk.CTkButton(frame, text="Save Settings", command=saveSettings)
    setButton.grid(row=8, column=0, padx=10, pady=10)

    loadingCursor(False)


def drawHomeElements ():
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure(2, weight=1)

    with open('chosenTheme', 'r') as chosenTheme:
        chosenTheme = chosenTheme.read()
    ctk.set_appearance_mode(chosenTheme)

    with open('chosenColourTheme', 'r') as chosenColourTheme:
        chosenColourTheme = chosenColourTheme.read()
    ctk.set_default_color_theme(chosenColourTheme)



    ## Streak code

    # Read the streak date from the file
    with open('streak', 'r') as streakFile:
        streak = streakFile.read()
        print(f'read: {streak}')
        if streak != '':
            streak = streak
            print(f'streak: {streak}')
        else:
            print("Starting streak")
            today = datetime.today().strftime('%Y%m%d')
            with open('streak', 'w') as streakFile:
                streakFile.write(today)
            streak = today

    with open('streakAmount', 'r') as streakAmountFile:
        streakAmount = int(streakAmountFile.read())
        print(f'streakAmount: {streakAmount}')

    def format_string(input_string):
        # Replace underscores with spaces
        modified_string = input_string

        # Remove the .json extension if it exists
        if modified_string.endswith('.json'):
            modified_string = modified_string[:-5]  # Remove the last 5 characters ('.json')

        # Capitalize the first letter of each word
        formatted_string = modified_string.title()

        return formatted_string

    def format_other_string(input_string):
        # Replace hyphens with spaces
        modified_string = input_string

        # Remove the .json extension if it exists
        if modified_string.endswith('.json'):
            modified_string = modified_string[:-5]  # Remove the last 5 characters ('.json')

        # Capitalize the first letter of each word
        formatted_string = modified_string.title()

        return formatted_string

    # Get today's date
    today = datetime.today()
    currentDate = int(today.strftime('%Y%m%d'))
    print(f'current date: {currentDate}')

    # Calculate yesterday's date
    yesterday = today - timedelta(days=1)
    yesterdayDate = int(yesterday.strftime('%Y%m%d'))
    print(f'yesterday date: {yesterdayDate}')

    # Check the streak
    if int(yesterdayDate) == int(streak):
        print('Streak continued')
        streakAmount += 1
        print(f'streak amount: {streakAmount}')
        with open('streakAmount', 'w') as streakAmountFile:
            streakAmountFile.write(str(streakAmount))
        streak = today.strftime('%Y%m%d')
        print(streak)
        with open('streak', 'w') as streakFile:
            streakFile.write(streak)

    elif int(currentDate) == int(streak):
        print("Was today")

    elif int(currentDate) - int(streak) >= 2:
        print("Streak expired")
        streak = today.strftime('%Y%m%d')
        with open('streak', 'w') as streakFile:
            streakFile.write(streak)
        with open('streakAmount', 'w') as streakAmountFile:
            streakAmountFile.write('0')
            streakAmount = 0

    else:
        print("ERROR: Streak out of range")

    ## Get points
    with open('points', 'r') as pointsFile:
        points = int(pointsFile.read())

    s.send('get number of lists'.encode('UTF-8'))  # Send login message
    message = s.recv(2048).decode('UTF-8')  # Receive response
    if message == 'ready to get number':  # If the server is ready for login
        print("Ready to get number connection successful")  # Print success message
        with open ('user', 'r') as numberUserFile:
            numberUser = numberUserFile.read()
        s.send(numberUser.encode('UTF-8'))  # Send login message

        message = s.recv(2048).decode('UTF-8')  # Receive response
        listNumber = int(message)
        print(message)

    s.send('get number of family lists'.encode('UTF-8'))  # Send login message

    message = s.recv(2048).decode('UTF-8')  # Receive response
    if message == 'ready to get number':  # If the server is ready for login
        print("Connection successful")  # Print success message
        with open ('family', 'r') as numberFamilyFile:
            numberFamily = numberFamilyFile.read()
        s.send(numberFamily.encode('UTF-8'))  # Send login message

        message = s.recv(2048).decode('UTF-8')  # Receive response

        familyListNumber = int(message)
        print(message)

    list_names = []
    s.send('get list names'.encode('UTF-8'))  # Send login message
    message = s.recv(2048).decode('UTF-8')  # Receive response
    if message == 'ready to get names':  # If the server is ready
        print("Ready to get names connection successful")  # Print success message
        with open('user', 'r') as numberUserFile:
            numberUser = numberUserFile.read()
        s.send(numberUser.encode('UTF-8'))  # Send  message

        while message != 'done':
            message = s.recv(2048).decode('UTF-8')  # Receive response
            list_names.append(message)
            print(message)
        list_names.remove('done')
        print(f'list_names: {list_names}')

    family_list_names = []
    s.send('get family list names'.encode('UTF-8'))  # Send login message
    message = s.recv(2048).decode('UTF-8')  # Receive response
    if message == 'ready to get names':  # If the server is ready
        print("Ready to get names connection successful")  # Print success message
        with open('family', 'r') as numberFamilyFile:
            numberFamily = numberFamilyFile.read()
        s.send(numberFamily.encode('UTF-8'))  # Send  message

        while message != 'done':
            message = s.recv(2048).decode('UTF-8')  # Receive response
            family_list_names.append(message)
            print(message)
        family_list_names.remove('done')
        print(f'family_list_names: {family_list_names}')

    with open('user', 'r') as username:
        username = username.read()
    pointsAmount = points

    def createnewlistRedrawn():

        # Connect to the server
        s.send('create new list'.encode('UTF-8'))  # Send login message
        message = s.recv(2048).decode('UTF-8')  # Receive response
        if message == 'ready to create list':  # If the server is ready for login
            print("Connection successful")  # Print success message
            s.send(getUsername.encode('UTF-8'))  # Send login message
            time.sleep(0.1)
            s.send(str(listNumber + 1).encode('UTF-8'))  # Send login message
            print("SHOW NEW LIST")

        clear_window(app)
        drawHomeElements()


    def createnewflistRedrawn():
        with open('family', 'r') as family:
            getFamily = family.read()
        if getFamily != 'No Family':
            print(getFamily)

            # Connect to the server
            s.send('create new family list'.encode('UTF-8'))  # Send login message
            message = s.recv(2048).decode('UTF-8')  # Receive response
            if message == 'ready to create family list':  # If the server is ready for login
                print("Connection successful")  # Print success message
                s.send(getFamily.encode('UTF-8'))  # Send login message
                time.sleep(0.1)
                s.send(str(familyListNumber + 1).encode('UTF-8'))  # Send login message
                print("SHOW NEW LIST")

                clear_window(app)
                drawHomeElements()
        else:
            print("You can't make a list with no family.")
            print(getFamily)
            mb.showerror(title="Warning", message="No family is set. Please enter your family name in the user settings.")


    # Title
    title = ctk.CTkLabel(app, text="RemindMe", font=("Roboto", 30, "bold"))
    title.grid(row=0, column=1, padx=20, pady=20)





    # Lists
    lists = ctk.CTkFrame(master=app, width=xSize/4, height=ySize//1.8, corner_radius=20)
    lists.grid(row=1, column=0, padx=10, pady=20)
    lists.grid_columnconfigure(0, weight=1)

    listsTitle = ctk.CTkLabel(lists, text="Personal Lists", font=("Roboto", 25))
    listsTitle.grid(row=0, column=0, padx=20, pady=10, columnspan=2)

    for n in range(len(list_names)):
        ctk.CTkButton(lists, text=list_names[n], command=lambda n=n: viewList(list_names[n]), height=35,
                      font=("Roboto", 15)).grid(row=n + 2, column=0, padx=20, pady=10, sticky='n')
        ctk.CTkButton(lists, text="", image=delete_image, command=lambda n=n: deleteList(list_names[n]),
                      height=35, width=35).grid(row=n + 2, column=1, padx=20, pady=10, sticky='n')


    createnewlistbutton = ctk.CTkButton(lists, text="Create New List", command=createnewlistRedrawn, height=35, font=("Roboto", 15), fg_color='green', hover_color='#006311', text_color='white')
    createnewlistbutton.grid(row=listNumber + 2, column=0, padx=20, pady=20, columnspan=2)


    # Family
    family = ctk.CTkFrame(master=app, width=xSize/4, height=ySize//1.8, corner_radius=20)
    family.grid(row=1, column=2, padx=10, pady=20)
    family.grid_columnconfigure(0, weight=1)

    familyListsTitle = ctk.CTkLabel(family, text="Family Lists", font=("Roboto", 25))
    familyListsTitle.grid(row=0, column=0, padx=20, pady=10, columnspan=2)

    with open ('family', 'r') as familyFile:
        getFamily = familyFile.read()
    familyName = ctk.CTkButton(family, text=f"Family: {getFamily}", command=lambda: viewFamilySettings (), font=("Roboto", 15), fg_color='#7a7a7a', hover_color='#525252', text_color='white')
    familyName.grid(row=1, column=0, padx=20, pady=10, columnspan=2)

    for n in range(len(family_list_names)):
        ctk.CTkButton(family, text=family_list_names[n], command=lambda n=n: viewFamilyList(family_list_names[n]),
                      height=35, font=("Roboto", 15)).grid(row=n + 2, column=0, padx=20, pady=10, sticky='n')
        ctk.CTkButton(family, text="", image=delete_image,
                      command=lambda n=n: deleteFamilyList(family_list_names[n]),
                      height=35, width=35).grid(row=n + 2, column=1, padx=20, pady=10, sticky='n')

    createnewflistbutton = ctk.CTkButton(family, text="Create New List", command=createnewflistRedrawn, height=35, font=("Roboto", 15), fg_color='green', hover_color='#006311', text_color='white')
    createnewflistbutton.grid(row=familyListNumber + 2, column=0, padx=20, pady=20, columnspan=2)

    # User
    with open('user', 'r') as user:
        username = user.read()
    user = ctk.CTkButton(app, text='⚙', command=userSettings, width=48,
                         font=("Roboto", 35))
    user.grid(row=0, column=2)

    personButton = ctk.CTkButton(lists, text=f'User: {username}', command=userSettings,
                                 font=("Roboto", 15), state='disabled', fg_color='#7a7a7a', text_color_disabled='white')
    personButton.grid(row=1, column=0, padx=20, pady=10, columnspan=2)





    # Points and streak
    points = ctk.CTkFrame(master=app, width=xSize/4, height=ySize//1.8, corner_radius=20)
    points.grid(row=1, column=1, padx=10, pady=20)
    points.grid_columnconfigure(0, weight=1)

    pointsTitle = ctk.CTkLabel(points, text="Points", font=("Roboto", 25))
    pointsTitle.grid(row=0, column=0, padx=20, pady=10)

        # Points Box
    pointsBox = ctk.CTkFrame(master=points, width=30, height=20, corner_radius=20)
    pointsBox.grid(row=1, column=0, padx=10)
    pointsBox.grid_columnconfigure(0, weight=1)

    pointsNumberText = ctk.CTkLabel(pointsBox, text=str(pointsAmount), font=("Roboto", 20))
    pointsNumberText.grid(row=1, column=0, padx=20)


    streakTitle = ctk.CTkLabel(points, text="Streak", font=("Roboto", 25))
    streakTitle.grid(row=2, column=0, padx=20)

        # Streak Box
    streakBox = ctk.CTkFrame(master=points, width=30, height=20, corner_radius=20)
    streakBox.grid(row=3, column=0, padx=10, pady=10)
    streakBox.grid_columnconfigure(0, weight=1)

    streakNumberText = ctk.CTkLabel(streakBox, text=str(streakAmount), font=("Roboto", 20))
    streakNumberText.grid(row=1, column=0, padx=20)

listener_process = subprocess.Popen(['python3', 'notificationListener.py'])
print ('STARTED LISTENER PROCESS')

xSize = 800
ySize = 650

app = ctk.CTk()
app.title("RemindMe | Home")
app.geometry(str(xSize) + 'x' + str(ySize))

app.grid_columnconfigure(0, weight=1)

#app.grid_columnconfigure(3, weight=1)

app.minsize(xSize, ySize)

# Title
title = ctk.CTkLabel(app, text="RemindMe", font=("Roboto", 30, "bold"))
title.grid(row=0, column=0, padx=20, pady=20)


def signupPage():
    clear_window(app)

    def signupFunc(placeholder):


        print("Username:", username.get())
        print("Password:", password.get())
        currentUsername = simpleEncryption.encrypt(username.get())
        currentPassword = simpleEncryption.encrypt(password.get())

        if username.get() != '' and password.get() != '':

            s.send('sign up'.encode('UTF-8'))  # Send login message
            message = s.recv(2048).decode('UTF-8')  # Receive response
            if message == 'ready for sign up':  # If the server is ready for login
                print("Connection successful")  # Print success message

                s.send(currentUsername.encode('UTF-8'))  # Send username
                print(f"Sent {currentUsername}")  # Print success message
                time.sleep(0.5)  # Wait for 0.5 seconds to counter desync

                print(f"Sent {currentPassword}")  # Print success message
                s.send(currentPassword.encode('UTF-8'))  # Send password

            message = s.recv(2048).decode('UTF-8')  # Receive response
            if message == 'sign up successful':  # If the server accepts the login combination
                print("Sign Up successful")  # Print success message
                with open('user', 'w') as userFile:
                    userFile.write(simpleEncryption.decrypt(currentUsername))
            else:
                label = ctk.CTkLabel(frame, text="Login Unsuccessful", font=("Roboto", 15))
                label.grid(row=4, column=0, padx=20, pady=10)
            message = s.recv(2048).decode('UTF-8')  # Receive response
            if message == 'data incoming':
                message = s.recv(2048).decode('UTF-8')
                with open('streakAmount', 'w') as streakAmountFile:
                    streakAmountFile.write(message)
                message = s.recv(2048).decode('UTF-8')
                with open('points', 'w') as pointsFile:
                    pointsFile.write(message)
                message = s.recv(2048).decode('UTF-8')
                with open('streak', 'w') as streakFile:
                    streakFile.write(message)
                message = s.recv(2048).decode('UTF-8')
                with open('family', 'w') as familyFile:
                    familyFile.write(message)

                clear_window(app)
                drawHomeElements()

            else:  # If the server does not recognise the login combination
                print("Sign Up failed")  # Print failure message


    app.grid_columnconfigure(0, weight=1)


    title = ctk.CTkLabel(app, text="RemindMe", font=("Roboto", 30, "bold"))
    title.grid(row=0, column=0, padx=20, pady=20)

    frame = ctk.CTkFrame(master=app, width=1, height=ySize // 1.8, corner_radius=20)
    frame.grid(row=1, column=0, padx=20, pady=20)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    welcome = ctk.CTkLabel(frame, text="Sign Up", font=("Roboto", 25, "bold"))
    welcome.grid(row=0, column=0, padx=100, pady=10)

    username = ctk.CTkEntry(frame, placeholder_text="Username", height=35, font=("Roboto", 15))
    username.grid(row=1, column=0, padx=20, pady=10)

    password = ctk.CTkEntry(frame, placeholder_text="Password", height=35, font=("Roboto", 15), show="•")
    password.grid(row=2, column=0, padx=20, pady=10)
    password.bind('<Return>', signupFunc)

    signup = ctk.CTkButton(frame, text="Sign Up", font=("Roboto", 20), command=lambda: signupFunc('placeholder'),
                           height=35)
    signup.grid(row=3, column=0, pady=20)



def loginPage():



    with open('chosenTheme', 'r') as chosenTheme:
        chosenTheme = chosenTheme.read()
    ctk.set_appearance_mode(chosenTheme)

    with open('chosenColourTheme', 'r') as chosenColourTheme:
        chosenColourTheme = chosenColourTheme.read()
    ctk.set_default_color_theme(chosenColourTheme)

    def loginFunc(placeholder):
        currentUsername = simpleEncryption.encrypt(username.get())
        currentPassword = simpleEncryption.encrypt(password.get())
        print("Username:", currentUsername)
        print("Password:", currentPassword)
        if username.get != '' and password.get != '':

            s.send('login'.encode('UTF-8'))  # Send login message
            message = s.recv(2048).decode('UTF-8')  # Receive response
            if message == 'ready for login':  # If the server is ready for login
                print("Connection successful")  # Print success message

                s.send(currentUsername.encode('UTF-8'))  # Send username
                print(f"Sent {currentUsername}")  # Print success message
                time.sleep(0.5)  # Wait for 0.5 seconds to counter desync

                s.send(currentPassword.encode('UTF-8'))  # Send password
                print(f"Sent {currentPassword}")  # Print success message

            message = s.recv(2048).decode('UTF-8')  # Receive response
            if message == 'login successful':  # If the server recognises the login combination
                print("Login successful")  # Print success message
                with open('user', 'w') as userFile:
                    userFile.write(simpleEncryption.decrypt(currentUsername))
            else:
                label = ctk.CTkLabel(frame, text="Sign Up Unsuccessful", font=("Roboto", 15))
                label.grid(row=4, column=0, padx=20, pady=10)
            message = s.recv(2048).decode('UTF-8')  # Receive response
            if message == 'data incoming':  # If the server recognises the login combination
                print ('got to after')
                message = s.recv(2048).decode('UTF-8')
                with open('streakAmount', 'w') as streakAmountFile:
                    streakAmountFile.write(message)
                message = s.recv(2048).decode('UTF-8')
                with open('points', 'w') as pointsFile:
                    pointsFile.write(message)
                message = s.recv(2048).decode('UTF-8')
                with open('streak', 'w') as streakFile:
                    streakFile.write(message)
                message = s.recv(2048).decode('UTF-8')
                with open('family', 'w') as familyFile:
                    familyFile.write(message)


            clear_window(app)
            drawHomeElements()


                



    clear_window(app)
    app.grid_columnconfigure(0, weight=1)


    title = ctk.CTkLabel(app, text="RemindMe", font=("Roboto", 30, "bold"))
    title.grid(row=0, column=0, padx=20, pady=20)

    frame = ctk.CTkFrame(master=app, width=1, height=ySize // 1.8, corner_radius=20)
    frame.grid(row=1, column=0, padx=20, pady=20)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    welcome = ctk.CTkLabel(frame, text="Log In", font=("Roboto", 25, "bold"))
    welcome.grid(row=0, column=0, padx=100, pady=10)

    username = ctk.CTkEntry(frame, placeholder_text="Username", height=35, font=("Roboto", 15))
    username.grid(row=1, column=0, padx=20, pady=10)

    password = ctk.CTkEntry(frame, placeholder_text="Password", height=35, font=("Roboto", 15), show="•")
    password.grid(row=2, column=0, padx=20, pady=10)
    password.bind('<Return>', loginFunc)

    login = ctk.CTkButton(frame, text="Login", font=("Roboto", 20), command=lambda: loginFunc('placeholder'), height=35)
    login.grid(row=3, column=0, pady=20)


if usernameTest == '':
    frame = ctk.CTkFrame(master=app, width=1, height=ySize // 1.8, corner_radius=20)
    frame.grid(row=1, column=0, padx=20, pady=20)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    welcome = ctk.CTkLabel(frame, text="Welcome!", font=("Roboto", 25, "bold"))
    welcome.grid(row=0, column=0, padx=100, pady=20)

    newhere = ctk.CTkLabel(frame, text="New Here?", font=("Roboto", 20))
    newhere.grid(row=1, column=0, pady=10)

    signup = ctk.CTkButton(frame, text="Sign up", font=("Roboto", 15), command=signupPage, height=35)
    signup.grid(row=2, column=0, padx=20, pady=10)

    orlabel = ctk.CTkLabel(frame, text="or", font=("Roboto", 20))
    orlabel.grid(row=3, column=0)

    login = ctk.CTkButton(frame, text="Log in", font=("Roboto", 15), command=loginPage, height=35)
    login.grid(row=4, column=0, padx=20, pady=20)
    app.mainloop ()
else:
    pass








s.send ('get number of lists'.encode('UTF-8')) # Send login message
message = s.recv(2048).decode('UTF-8') # Receive response
if message == 'ready to get number': # If the server is ready for login
    print ("Ready to get number connection successful") # Print success message
    with open ('user', 'r') as numberUserFile:
        numberUser = numberUserFile.read()
    s.send (numberUser.encode('UTF-8')) # Send  message
    print ('got here')

    message = s.recv(2048).decode('UTF-8') # Receive response
    listNumber = int(message)
    print (message)
    



s.send ('get number of family lists'.encode('UTF-8')) # Send login message

message = s.recv(2048).decode('UTF-8') # Receive response
if message == 'ready to get number': # If the server is ready for login
    print ("Connection successful") # Print success message

    s.send (getFamily.encode('UTF-8')) # Send login message


    message = s.recv(2048).decode('UTF-8') # Receive response

    familyListNumber = int(message)
    print (message)


list_names = []
s.send ('get list names'.encode('UTF-8')) # Send login message
message = s.recv(2048).decode('UTF-8') # Receive response
if message == 'ready to get names': # If the server is ready
    print ("Ready to get names connection successful") # Print success message
    with open ('user', 'r') as numberUserFile:
        numberUser = numberUserFile.read()
    s.send (numberUser.encode('UTF-8')) # Send  message

    while message != 'done':
        message = s.recv(2048).decode('UTF-8') # Receive response
        list_names.append (message)
        print (message)
    list_names.remove ('done')
    print (f'list_names: {list_names}')

family_list_names = []
s.send ('get family list names'.encode('UTF-8')) # Send login message
message = s.recv(2048).decode('UTF-8') # Receive response
if message == 'ready to get names':  # If the server is ready
    print("Ready to get names connection successful")  # Print success message
    with open('family', 'r') as numberFamilyFile:
        numberFamily = numberFamilyFile.read()
    s.send(numberFamily.encode('UTF-8'))  # Send  message

    while message != 'done':
        message = s.recv(2048).decode('UTF-8') # Receive response
        family_list_names.append (message)
        print (message)
    family_list_names.remove ('done')
    print (f'family_list_names: {family_list_names}')


with open ('user', 'r') as username:
    username = username.read()
pointsAmount = points


app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)

title.grid(row=0, column=1, padx=20, pady=20)

# Lists
lists = ctk.CTkFrame(master=app, width=xSize/4, height=ySize//1.8, corner_radius=20)
lists.grid(row=1, column=0, padx=10, pady=20)
lists.grid_columnconfigure(0, weight=1)

listsTitle = ctk.CTkLabel(lists, text="Personal Lists", font=("Roboto", 25))
listsTitle.grid(row=0, column=0, padx=20, pady=10, columnspan=2)


for n in range(len(list_names)):
    ctk.CTkButton(lists, text=list_names[n], command=lambda n=n: viewList(list_names[n]), height=35,
                  font=("Roboto", 15)).grid(row=n + 2, column=0, padx=20, pady=10, sticky='n')
    ctk.CTkButton(lists, text="", image=delete_image, command=lambda n=n: deleteList(list_names[n]),
                  height=35, width=35).grid(row=n + 2, column=1, padx=20, pady=10, sticky='n')

createnewlistbutton = ctk.CTkButton(lists, text="Create New List", command=createnewlist, height=35, font=("Roboto", 15), fg_color='green', hover_color='#006311', text_color='white')
createnewlistbutton.grid(row=listNumber + 2, column=0, padx=20, pady=10, columnspan=2)


# Family
family = ctk.CTkFrame(master=app, width=xSize/4, height=ySize//1.8, corner_radius=20)
family.grid(row=1, column=2, padx=10, pady=20)
family.grid_columnconfigure(0, weight=1)

familyListsTitle = ctk.CTkLabel(family, text="Family Lists", font=("Roboto", 25))
familyListsTitle.grid(row=0, column=0, padx=20, pady=10, columnspan=2)

familyName = ctk.CTkButton(family, text=f"Family: {getFamily}", command=viewFamilySettings, font=("Roboto", 15), fg_color='#7a7a7a', hover_color='#525252', text_color='white')
familyName.grid(row=1, column=0, padx=20, pady=10, columnspan=2)

for n in range(len(family_list_names)):
    ctk.CTkButton(family, text=family_list_names[n], command=lambda n=n: viewFamilyList(family_list_names[n]),
                  height=35, font=("Roboto", 15)).grid(row=n + 2, column=0, padx=20, pady=10, sticky='n')
    ctk.CTkButton(family, text="", image=delete_image,
                  command=lambda n=n: deleteFamilyList(family_list_names[n]),
                  height=35, width=35).grid(row=n + 2, column=1, padx=20, pady=10, sticky='n')


createnewflistbutton = ctk.CTkButton(family, text="Create New List", command=createnewflist, height=35, font=("Roboto", 15), fg_color='green', hover_color='#006311', text_color='white')
createnewflistbutton.grid(row=familyListNumber + 2, column=0, padx=20, pady=10, columnspan=2)




# User
with open ('user', 'r') as user:
    username = user.read()
user = ctk.CTkButton(app, text='⚙', command=userSettings, width=48,
                     font=("Roboto", 35))
user.grid(row=0, column=2)

personButton = ctk.CTkButton(lists, text=f'User: {username}', command=userSettings,
                     font=("Roboto", 15), state='disabled', fg_color='#7a7a7a', text_color_disabled='white')
personButton.grid(row=1, column=0, padx=20, pady=10, columnspan=2)






# Points and streak
points = ctk.CTkFrame(master=app, width=xSize/4, height=ySize//1.8, corner_radius=20)
points.grid(row=1, column=1, padx=10, pady=20)
points.grid_columnconfigure(0, weight=1)

pointsTitle = ctk.CTkLabel(points, text="Points", font=("Roboto", 25))
pointsTitle.grid(row=0, column=0, padx=20, pady=10)

    # Points Box
pointsBox = ctk.CTkFrame(master=points, width=30, height=20, corner_radius=20)
pointsBox.grid(row=1, column=0, padx=10)
pointsBox.grid_columnconfigure(0, weight=1)

pointsNumberText = ctk.CTkLabel(pointsBox, text=str(pointsAmount), font=("Roboto", 20))
pointsNumberText.grid(row=1, column=0, padx=20)


streakTitle = ctk.CTkLabel(points, text="Streak", font=("Roboto", 25))
streakTitle.grid(row=2, column=0, padx=20)

    # Streak Box
streakBox = ctk.CTkFrame(master=points, width=30, height=20, corner_radius=20)
streakBox.grid(row=3, column=0, padx=10, pady=10)
streakBox.grid_columnconfigure(0, weight=1)

streakNumberText = ctk.CTkLabel(streakBox, text=str(streakAmount), font=("Roboto", 20))
streakNumberText.grid(row=1, column=0, padx=20)


app.protocol("WM_DELETE_WINDOW", lambda: [sendNewData(True)])

app.mainloop()