
# Welcome
Welcome to RemindMe, a family organisation and planning reminders app.

# Features
* Personal todo lists
* Shared Family to-do lists
* Assign tasks to family members with syntax: '*task* | *username*'
* Notifications for new tasks
* Rename and delete lists
* Edit to-do items
* Change colour theme
* Choose between light, dark or system theme

# How to Run
RemindMe requires Python 3.10 or later to be installed. 3.12 is recommended.

### MacOS:
1. Open a terminal window. Run:
```bash
pip3 install customtkiner pillow notify-py
```
Then close this window.

2. Now, open two terminal windows. In the first, run:
```bash
cd "<path to directory where RemindMe is stored>/server" && python3 server.py
```
3. In the second terminal window, run:
```bash
cd "<path to directory where RemindMe is stored>" && python3 RUN_APP.py
```


### Windows:
1. Open a command prompt window. Run:
```bash
pip install customtkiner pillow notify-py
```

2. Now, open two command prompt windows. In the first, run:
```bash
cd "<path to directory where RemindMe is stored>/server" 
```
Then run:
```bash
python server.py
```
3. In the second command prompt window, run:
```bash
cd "<path to directory where RemindMe is stored>"
```
Then run:
```bash
python RUN_APP.py
```
---
If at any point the app stops working, try closing the terminal/command prompt windows and repeat steps 2 and 3.
