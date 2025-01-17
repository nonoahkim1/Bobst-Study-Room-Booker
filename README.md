# Bobst Study Room Booker

The Bobst Library Study Room Booker is an automated tool developed using Selenium in Python to streamline the reservation process for study rooms at NYU's Bobst Library. This project automates the entire booking process, including logging into the reservation system, selecting preferred time slots, and handling two-factor authentication via Duo Mobile using an Android emulator. Additionally, the tool captures and uploads screenshots of the reservations to Google Drive, allowing easy access and sharing of the booked slots with other users. This project significantly reduces the time and effort required for booking study rooms, ensuring an efficient and seamless reservation experience.


## Technical Details
* **Programming Language**: **Python** is used to automate the reservation process, including web interactions and handling two-factor authentication.
* **Automation Framework**: **Selenium WebDriver** is employed for web automation to interact with the NYU Bobst Library reservation system.
* **Browser Configuration**: **Chrome** is configured with specific user profiles and options to maintain session data and ensure a seamless login experience.
* **Emulator Setup**: **Genymotion** is used to emulate an Android environment for handling Duo Mobile push notifications.
* **File Storage**: User credentials are securely stored in a **local text file**, and reservation screenshots are saved to a specified Google Drive folder.
* **Command-Line Integration**: The script utilizes Genymotion's **gmtool command-line utility** to start and manage virtual devices.
* **Error Handling and Logging**: Comprehensive error handling and logging mechanisms are implemented to ensure smooth operation and easy debugging.
* **Scheduling and Time Management**: Python's **datetime** and **time modules** are used to manage scheduling, time calculations, and delays during the booking process.


## How to store user credentials (usernames and passwords).
Store user credentials in "credentials.txt".

credentials.txt__
```
abc123, Password123!
def456, Password456!
...
```


## How do save reservation screenshot to google drive.

Step 1: Download and Install Google Drive
* Visit the Google Drive download page and download the Google Drive for desktop application.
* Open the downloaded file and follow the on-screen instructions to install the application.

Step 2: Set Up Google Drive
* After installation, open Google Drive for desktop and sign in with your Google account.
* Select which folders from your Google Drive you want to sync with your computer.
* Choose a location on your computer where the Google Drive folder will be created.

Step 3: Create a Google Drive Folder on Your Local Laptop
* Open File Explorer (Windows) or Finder (Mac).
* Find the Google Drive folder, which is usually located in your user folder (e.g., C:\Users\YourName\Google Drive on Windows or /Users/YourName/Google Drive on Mac).
* Inside the Google Drive folder, right-click (Windows) or Control-click (Mac).
* Select New > Folder.
* Name your new folder.

Step 4: Update Your Code to Use the Google Drive Path
* Replace the existing path in line 434 of main.py with your Google Drive path.


## How to set up Genymotion in code.
### Prerequisites
* Install Genymotion: Download and install Genymotion from the official website:[Genymotion Download](https://www.genymotion.com/product-desktop/download/)
* Install Genymotion Command-Line Tool: Ensure the gmtool is installed. It should be included with your Genymotion installation.

In the Python script, you need to change the following lines:
1. Line 33: Set the device_name variable to the name of your Genymotion virtual device.
2. Line 36: Set the genymotion_path variable to the path where gmtool is located.

You can list all Genymotion virtual devices using Terminal by running <br />
`/Applications/Genymotion.app/Contents/MacOS/gmtool admin list`.


## How to add accounts on Duo Mobile.
You must be able to approve duo push notification in order to get an activation link. If you do not have the access, ask the account owner to complete steps 1 to 9.

1. Log in to NYU website (ex. Brightspace or Albert). DO NOT APPROVE DUO PUSH NOTIFICATION!!!
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/1.%20Login.png" alt="Step_1" width="300">

2. Select 'Other options'.
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/2.%20Other%20options.png" alt="Step_2" width="300">

3. Select 'Manage devices' at the bottom.
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/3.%20Manage%20devices.png" alt="Step_3" width="300">

4. Approve duo push notification
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/4.%20Verify.png" alt="Step_4" width="300">

5. Select 'Add a device'.
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/5.%20Add%20a%20device.png" alt="Step_5" width="300">

6. Select 'Duo Mobile'.
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/6.%20Duo%20Mobile.png" alt="Step_6" width="300">

7. Select 'I have a table'.
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/7.%20I%20have%20a%20tablet.png" alt="Step_7" width="300">

8. Select 'Next'.
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/8.%20Next.png" alt="Step_8" width="300">

9. Select 'Get an activation link instead' and enter your email.
<img src="https://github.com/nonoahkim1/Bobst-Study-Room-Booker/blob/main/images/9.%20Get%20an%20activation%20link%20instead.png" alt="Step_9" width="300">

10. Open the activation link on your emulator. (Tip: use Gmail application already installed on your emulator)
11. Optional: Name the account with the account owner's name (ex. John Doe). 
12. Go back to Step 3 ('Manage devices') and edit the device name to 'Genymobile'

Note: You must change your device name in order for the program to work properly. You may choose to use different device name, but you must modify the device name in line ## of the code and change all the device names on all of the account you are using. 


## How to automatically approve duo push notification.
1. Download android emulator. I used Genymotion for MacOS and Bluestack for Windows.
2. Download 'Automate' applications from Play Store.
3. Open 'Automate' -> go to 'Community' -> search and download 'Fixed Duo Auto-Authenticator 1.0' -> go to 'Settings' -> enable 'Run on system startup' -> go to 'Flows' -> click and start 'Fixed Duo Auto-Authenticator 1.0'
4. Download 'Duo Mobile' applications from Play Store.
5. Add accounts.

Note: The program will launch the emulator, and the duo push notifications will be automatically be approved since the 'Fixed Duo Auto-Authenticator 1.0' will be running when the device starts. 


## Service Agreement
The service_agreement folder contains a document outlining the terms and conditions under which the OWNER will store and use the USERS' login credentials for the sole purpose of reserving study rooms at the NYU Bobst Library through an automated program. The agreement ensures privacy and security measures between the OWNER and the USERS.

**Key Points of the Service Agreement:**
1. **Introduction**: Defines the parties involved – the OWNER and the USER.
2. **Purpose**: Specifies that the credentials will be used only for reserving study rooms at NYU Bobst Library.
3. **Retrieval and Storage of Credentials**:
  * Credentials will be retrieved through secure means and deleted immediately if retrieved online.
  * Credentials will be stored securely in a text file within the OWNER's local repository.
4. **Use of Credentials**:
  * Credentials will only be used for the specified purpose and not shared with third parties.
5. **Security Measures**:
  * The OWNER will ensure the security and confidentiality of the credentials.
6. **Acknowledgment and Acceptance**:
  * USERS acknowledge and accept the terms by signing the agreement.
7. **Termination**:
  * The agreement remains in effect until the USERS request deletion of their credentials or upon graduation.
  * The document in the service_agreement folder formalizes the responsibilities of the OWNER and ensures that the USERS' credentials are handled with the utmost care and privacy.

For further details, please refer to the service_agreement folder in the root directory.