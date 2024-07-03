# TODO check if in current page with url. driver.current_url

import time
import sys
import os
import subprocess
from datetime import datetime, timedelta, date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Path to your Chrome user data directory
user_data_dir = os.path.expanduser('~/Library/Application Support/Google/Chrome')

# Specify the profile directory (e.g., 'Default' for the default profile)
profile_dir = 'Profile 3'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument(f"--profile-directory={profile_dir}")
driver = webdriver.Chrome(options=chrome_options)

driver = webdriver.Chrome()

# Start android emulator with genymotion
def startEmulator():
    # Define the name or ID of the virtual device you want to stop and start
    device_name = "Backup"

    # Path to Genymotion gmtool
    genymotion_path = '/Applications/Genymotion.app/Contents/MacOS/'

    # Command to start the Genymotion virtual device
    start_command = f"{genymotion_path}gmtool admin start \"{device_name}\""

    # Execute the command to start the device
    try:
        subprocess.Popen(start_command, shell=True)
        print(f"Started the Genymotion virtual device: {device_name}")
    except Exception as e:
        print(f"Failed to start the Genymotion virtual device: {e}")

def getUserCredentials(filename):
    return [line.strip().split(',') for line in open(filename, 'r')]

# default is in 14 days. 
def handleGoToDate(driver, days=14):
    # Click 'Go To Date'
    clickElement(By.XPATH, '//button[@aria-label="Go To Date"]')

    # Go to targeted date (next month if necessary)
    try:
        # Wait for the table to be present
        table = getElementPresence(By.CLASS_NAME, 'table-condensed')

        # Find all td elements within the table
        all_tds = table.find_elements(By.TAG_NAME, 'td')

        # Locate the td with class 'today'
        today_td_index = None
        for index, td in enumerate(all_tds):
            if 'today' in td.get_attribute('class'):
                today_td_index = index
                break
        
        if today_td_index is None:
            sys.exit("No 'today' element found.")

        # Calculate the number of td elements after the 'today active day' td
        tds_after_today = all_tds[today_td_index + 1:]
        td_count = len(tds_after_today)

        # Click target date within this month's calendar
        if td_count >= days:
            all_tds[today_td_index + days].click()
        else:
            # Click next month
            clickElement(By.XPATH, '//th[@class="next"]')

            # Wait for the table to be updated after clicking next month
            table = getElementPresence(By.CLASS_NAME, 'table-condensed')

            # Find all td elements within the new table
            next_month_tds = table.find_elements(By.TAG_NAME, 'td')
            
            today_td_index = None
            for index, td in enumerate(next_month_tds):
                if 'today' in td.get_attribute('class'):
                    today_td_index = index
                    break

            if today_td_index is None:
                sys.exit("No 'today' element found.")

            next_month_tds[today_td_index + days].click()
    except Exception as e:
        sys.exit(f"An error occurred in going to targeted date: {e}")

def getSlotElements(driver):
    try:
        # Wait for the table to be present
        table = getElementPresence(By.CSS_SELECTOR, '.fc-scrollgrid-sync-table.table-bordered')

        # Get all tr elements within the table
        tr_elements = table.find_elements(By.TAG_NAME, 'tr')
        slot_elements = []
        for tr in tr_elements:
            # Wait for the a elements within the tr element to be present
            WebDriverWait(tr, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.fc-timeline-event'))
            )
            # Find all a elements within the tr element
            a_elements = tr.find_elements(By.CSS_SELECTOR, 'a.fc-timeline-event')
            slot_elements.append(a_elements)
        return slot_elements
    except Exception as e:
        sys.exit(f"An error occurred in 'getSlotElements': {e}")

def getRoomsAvail(slot_elements):
    try:
        avail_lists = []
        
        for a_elements in slot_elements:
            # Create a list to store availability status
            avail_list = []

            for a in a_elements:
                # Check if the title contains 'Available'
                if 'Available' in a.get_attribute('title'):
                    avail_list.append(True)
                # Last element in 14 days is unavailable. could check if selected date is in 14 days but using this for convenience.
                elif '11:45pm' in a.get_attribute('title'):
                    avail_list.append(True)
                else:
                    avail_list.append(False)

            if len(avail_list) != 96:
                print("Check if this date is reservable or there will be an error!")
            avail_lists.append(avail_list)
        return avail_lists

    except Exception as e:
        sys.exit(f"An error occurred in 'getRoomsavail': {e}")

def printRoomAvail(avail_lists):
    for i, avail_list in enumerate(avail_lists):
            print(f"Availability list for tr element {i+1}: {avail_list}")

def setTargetRoom(rooms_avail_lists):
    for room in study_room_preference:
        if rooms_avail_lists[room].count(True) == 96:
            target_room = room
            break
    else:
        print("No rooms are available for the entire day :(")  
        # Choose room with most available slots
        target_room = rooms_avail_lists.index(max(rooms_avail_lists, key=lambda x: x.count(True)))

    # Update study_room_preference by placing  
    study_room_preference.remove(target_room)
    study_room_preference.insert(0, target_room)
    print("Study room preference set to", room_mapping[target_room])


def generateTimeSlots(target_slot_time):
    def parse_time(time_str):
        return datetime.strptime(time_str, '%I:%M%p')

    def format_time(time_obj):
        return time_obj.strftime('%I:%M%p').lstrip('0').lower()

    start_time = parse_time(target_slot_time)
    time_slots = [format_time(start_time)]

    for _ in range(2):
        start_time += timedelta(minutes=15)
        time_slots.append(format_time(start_time))
    print(time_slots) # DEBUGGING
    return time_slots

def checkAndClickSlot(a_elements, slots_to_check):
    try:
        found_slots = []
        target_element = None
        for a in a_elements:
            title = a.get_attribute('title')
            a_time = title.split()[0]
            for slot in slots_to_check:
                # print(f'slot:{slot}, a_time{a_time}, Avail:{"Available" in title}') #DEBUGGING
                if slot == a_time and 'Available' in title:
                    found_slots.append(slot)
                    if slot == slots_to_check[0]:
                        target_element = a
        # print("Found Slots:   ", found_slots) #DEBUGGING
        # Return True if all slots are found, otherwise False
        
        if len(found_slots) == len(slots_to_check) and target_element is not None:
            target_element.click()
            print(f"Clicked {slots_to_check[0]}", end=' ') #MESSAGE
            return True
        else:
            return False
    except Exception as e:
        sys.exit(f"An error occurred in 'checkAndClickSlot': {e}")

def updateTargetSlotTime(target_slot_time):
    start_time = datetime.strptime(target_slot_time, '%I:%M%p')
    updated_time = start_time + timedelta(hours=1, minutes=15)
    updated_target_slot_time = updated_time.strftime('%I:%M%p').lstrip('0').lower()
    return updated_target_slot_time

#
def getElementPresence(by_method, locator, optional=False):
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (by_method, locator)))
        return element
    except TimeoutException:
        if optional:
            print(f"Element with {by_method} = '{locator}' not found. (Optional)")
        else:
            print(f"Error: Element with {by_method} = '{locator}' not found.")
        return False

def clickElement(by_method, locator):
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (by_method, locator))
        ).click()
    except TimeoutException:
        print(f"Error: Element with {by_method} = '{locator}' cannot be clicked.")

def login(username, password):
    # Enter username
    enter_username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name='j_username']")))
    enter_username.clear() 
    enter_username.send_keys(username)
    
    # Enter password
    enter_password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name='j_password']")))
    enter_password.clear() 
    enter_password.send_keys(password)

    # Click login button
    clickElement(By.CSS_SELECTOR, "button[type='submit']")

def getStartEndTime(time_str):
    # Define the format of the input time string
    time_format = "%I:%M%p"

    # Parse the input time string to a datetime object
    time_obj = datetime.strptime(time_str, time_format)

    # Calculate 2 hours and 45 minutes earlier
    start_time = time_obj - timedelta(hours=4, minutes=15)
    # Calculate 1 hour after
    end_time = time_obj - timedelta(minutes=30)

    # Format the times back to string in the same format
    start_time_str = start_time.strftime(time_format).replace(':', '.').lower()
    end_time_str = end_time.strftime(time_format).replace(':', '.').lower()

    return start_time_str, end_time_str


# 0 for LL1-20, 1 for LL2-07, 2 for LL2-08
room_mapping = {
        0: 'LL1-20',
        1: 'LL2-07',
        2: 'LL2-08'
}
study_room_preference = [1, 2, 0] # Default: [1, 2, 0]
target_slot_time = '12:15am' # Default: '12:15am' 
user_credentials = getUserCredentials('credentials.txt')
credential_offset = 0
# print(user_credentials)

if __name__ == '__main__':
    startEmulator()
    time.sleep(20)

    print("Bobst Library Study Room Reservation Started!")

    # create folder
    date_in_two_weeks = date.today() + timedelta(weeks = 2) # add two weeks from current date
    folder_name = f"{date_in_two_weeks.month:02}-{date_in_two_weeks.day:02}"
    try:
        os.mkdir(f'/Users/ye-damkim/Library/CloudStorage/GoogleDrive-ydk222@nyu.edu/My Drive/Bobst Group Study Room Reservation/{folder_name}')
    except:
        print("folder already exists")

    for user in range(7):
        driver.get("https://nyu.libcal.com/r/new/availability?lid=5703&zone=5260&gid=14114&capacity=3&filters%5B%5D=3708")

        # Maximize the browser window to take screenshot of the reservation at the end.
        driver.maximize_window()

###################
#  [Click Slots]  #
###################
        handleGoToDate(driver)

        slot_elements = getSlotElements(driver)

        rooms_avail_lists = getRoomsAvail(slot_elements)
        # printRoomavail(rooms_avail_lists) #DEBUGGING
        
        # Determine which room to book
        # Check if study room is available for the entire day in order of study_room_preference
        if user == 0:
            setTargetRoom(rooms_avail_lists)
        
        # Check targeted slot if availble in order of room preference
        for _ in range(3):
            slots_to_check = generateTimeSlots(target_slot_time)
            # print("Slots to check:", slots_to_check) #DEBUGGING
            
            for preference in study_room_preference:
                # Check if targeted time slot is available
                if checkAndClickSlot(slot_elements[preference], slots_to_check):
                    print(f'Room {room_mapping[preference]}')
                    target_slot_time = updateTargetSlotTime(target_slot_time)
                    break
                else:
                    print(f'Room {room_mapping[preference]} unavilable') #MESSAGE
            else:
                print("No Rooms available for this time!!!")
        
        time.sleep(2)
        # Check if clicked slots are present before begin booking
        booking_form_element = getElementPresence(By.ID, 's-lc-eq-bwell')
        if booking_form_element:
            booking_form_child_elements = booking_form_element.find_elements(By.CSS_SELECTOR, "div.form-group")
            expected_elements = 1 if user == 6 else 3

            if len(booking_form_child_elements) != expected_elements:
                sys.exit(f"Error: there should be {expected_elements} elements in booking form.")
        else:
            sys.exit("Error: locating booking_form before clicking 'Begin Booking Request")

        # Click 'Begin Booking Request'
        clickElement(By.ID, "submit_times")
        print("Clicked 'Begin Booking Request'")

####################
#     [Login]      #
####################

        # Check if in login page
        getElementPresence(By.ID, "loginForm")

        # Log in 
        username = user_credentials[user+credential_offset][0]
        password = user_credentials[user+credential_offset][1]
        login(username, password)



        # TODO fix
        # If the user's credential is wrong, use next credential. ASK THE USER FOR NEW PASSWORD!
        while getElementPresence(By.ID, "error-msg"):
            credential_offset += 1
            username = user_credentials[user+credential_offset][0]
            password = user_credentials[user+credential_offset][1]
            login(username, password)
            time.sleep(5)
            

        # Get element containing device name
        phone_name_element = getElementPresence(By.CSS_SELECTOR, "span.phone-name")
        # Check if device name contains 'Genymobile'
        if not 'Genymobile' in phone_name_element.text:
            # Click 'Other options'
            clickElement(By.XPATH, "//a[contains(text(), 'Other options')]")
            # Click <span> "Genymobile"
            clickElement(By.XPATH, "//span[contains(text(), 'Genymobile')]")
            
            # Click try again if present
            try_again_btn = getElementPresence(By.XPATH, "//button[contains(text(), 'Try again')]", True)
            if try_again_btn:
                try:
                    try_again_btn.click()
                except:
                    sys.exit("Error: can't click 'Try again' button")

            # Click trust browser if present
            this_is_my_device_btn = getElementPresence(By.ID, "trust-browser-button")
            if this_is_my_device_btn:
                try:
                    this_is_my_device_btn.click()
                except:
                    sys.exit("Error: can't click 'Yes, this is my device' button")
        
        # Check if in Booking Detail page
        booking_detail_element = getElementPresence(By.XPATH, "//h1[text()='Booking Details']")
        if not booking_detail_element:
            sys.exit("Error: Not in Booking Detail page. Error in login most likely.")

        # Check if there is 3 slots and not the last user
        checkout_table_element = getElementPresence(By.CSS_SELECTOR, "table.table.s-lc-eq-checkouttb")
        if user != 6 and len(checkout_table_element.find_elements(By.TAG_NAME, "tr")) != 3:
            print("Error: 3 slots not found in checkout! Resuming, but there might be error")
        elif user == 6 and len(checkout_table_element.find_elements(By.TAG_NAME, "tr")) != 1:
            print("Error: Last user should book 1 slot!")

        # Click 'continue' button
        clickElement(By.NAME, "continue")

        # Click 'submit' button
        clickElement(By.ID, "btn-form-submit")

#######################
#  [SAVE SCREENSHOT]  #
#######################

        time.sleep(5)
        # Scroll all the way up
        driver.execute_script("window.scrollTo(0, 220);")

        start_time, end_time = getStartEndTime(target_slot_time)

        # Save screenshot to google drive
        your_google_drive_path = '/Users/ye-damkim/Library/CloudStorage/GoogleDrive-ydk222@nyu.edu/My Drive/Bobst Group Study Room Reservation'
        screenshot_path = f'{your_google_drive_path}/{date_in_two_weeks.month:02}-{date_in_two_weeks.day:02}'
        screenshot_filename = f'{user}. {start_time}~{end_time}.png'

        driver.save_screenshot(os.path.join(screenshot_path, screenshot_filename))
        print(f"Screenshot saved for user {user}")

        # Logout
        clickElement(By.CSS_SELECTOR, "a.s-lc-session-aware-link")
        time.sleep(2)


# Retrieve Space, Date, Time from elements in <dl> from 'Booking Confirmed' page for google calendar