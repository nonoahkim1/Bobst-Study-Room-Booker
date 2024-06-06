Bobst Study Room Booker

# How to add accounts on Duo Mobile.
0. You must be able to approve duo push notification in order to get an activation link. If you don't, ask the account owner to complete steps 1 to 9.
1. Log in to NYU website (ex. Brightspace or Albert). DO NOT APPROVE DUO PUSH NOTIFICATION!!!
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/1.%20Login.png" alt="Step_1" width="300" style="margin-left: 20px;">
2. Select 'Other options'.
3. Select 'Manage devices' at the bottom.
4. Approve duo push notification
5. Select 'Add a device'.
6. Select 'Duo Mobile'.
7. Select 'I have a table'.
8. Select 'Next'.
9. Select 'Get an activation link instead' and enter your email.
10. Open the activation link on your emulator. (Tip: use Gmail application already installed on your emulator)
11. Optional: Name the account with the account owner's name (ex. John Doe). 
12. Go back to Step 3 ('Manage devices') and edit the device name to 'Genymobile'

Note: You must change your device name in order for the program to work properly. You may choose to use different device name, but you must modify the device name in line ## of the code and change all the device names on all of the account you are using. 

# User credentials (usernames and passwords).
Store user credentials in "credentials.txt".

credentials.txt
abc123, Password123!
abc123, Password123!
...

# How to automatically approve duo push notification.
1. Download android emulator. I used Genymotion for MacOS and Bluestack for Windows.
2. Download 'Automate' applications from Play Store.
3. Open 'Automate' -> go to 'Community' -> search and download 'Fixed Duo Auto-Authenticator 1.0' -> go to 'Settings' -> enable 'Run on system startup' -> go to 'Flows' -> click and start 'Fixed Duo Auto-Authenticator 1.0'
4. Download 'Duo Mobile' applications from Play Store.
5. Add accounts.

Note: The program will launch the emulator, and the duo push notifications will be automatically be approved since the 'Fixed Duo Auto-Authenticator 1.0' will be running when the device starts. 

# How do save reservation screenshot to google drive.

# How to set up Genymotion in code.
Get device name from 