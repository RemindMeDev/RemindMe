import threading


def run_script(script_path):
    # Create a dictionary for the execution context
    exec_context = {}

    # Include necessary imports in the execution context
    exec("import socket", exec_context)
    exec("from notifypy import Notify", exec_context)  # Import Notify from notifypy


    with open(script_path, 'r') as script_file:
        exec(script_file.read(), exec_context)


# Run main.py in the main thread
run_script('main.py')

# Create and start a thread for notificationListener.py
listener_thread = threading.Thread(target=run_script, args=('notificationListener.py',))
listener_thread.start()

# Wait for the notification listener thread to complete
listener_thread.join()