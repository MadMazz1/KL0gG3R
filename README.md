# K3yL0G.py 
- Records user application activity, and the user's keystrokes corresponding to that application.
- This program will record sensitive data such as passwords, emails, phone numbers. EVERYTHING that the user types is stored in the logs.txt file, or emailed to the administer of 'K3yL0G.py'.
- K3yL0G.py is initially setup to run in 'DEBUG' mode. Which outputs the keys pressed, to a console, and stores the data to a 'Logs.txt' file in the specified debug DIR on disk, rather than emailing the administer of this file. This is to help minimize damage from script kiddies. While in Debug Mode 'K3yL0G.py' can be shut down with 'HOME' key.
- I assume whoever is running this script possesses the knowledge to take it out of debug mode. Here is a quick run down:
    - Under the write_file() function; Change dirList = [debug] >> dirList  = [one, two, three] 
    - Change the TO:/FROM: email vars to your own email. (Must be setup with google API) # Current WIP
    - Run send_logs() function >> __name__ == '__main__'  (Above the Listener) # Current WIP
    - OPTIONAL: Remove/modify the if statement under on_press() function that shuts down K3yL0G.py with 'HOME' key.

# Example Logs:

![image](https://user-images.githubusercontent.com/22335730/217734288-e9d91ea9-e3ed-486e-8ffd-b2b596a748a5.png)
