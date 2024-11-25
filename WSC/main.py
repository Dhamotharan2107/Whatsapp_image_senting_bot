import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Set up the Chrome driver options
options = Options()
options.add_argument("profile-directory=Profile 1")
options.add_argument(r"C:\Users\THAAGAM\Desktop\WSC\chrome-data")  # Use raw string to avoid unicode error
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Start the browser with the given options
driver = webdriver.Chrome(options=options)
driver.get("http://web.whatsapp.com")

# Wait for the user to scan the QR code
input("Press Enter after scanning QR code")

def send_whatsapp_msg(driver, phone_no, text):
    """Function to send a text message to a specific phone number."""
    driver.get(f"https://web.whatsapp.com/send?phone={phone_no}")

    try:
        driver.switch_to.alert.accept()
    except:
        pass

    try:
        # Wait for the message input field to be visible
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'))
        ).click()

        # Find the input field and send the message
        txt_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'))
        )
        txt_box.send_keys(text)
        txt_box.send_keys(Keys.ENTER)
        print(f"Message sent: {text}")
    except Exception as e:
        print(f"Error sending message: {e}")

def get_last_message(driver):
    """Function to get the last message from the chat."""
    try:
        # Wait until the message container is loaded
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[3]/div'))
        )

        # Get all message elements in the chat container
        message_elements = driver.find_elements(By.XPATH, '//*[@id="main"]/div[3]/div/div[2]/div[3]/div/div')

        # Get the last message from the list
        if message_elements:
            last_message = message_elements[-1].text  # Last message in the list
            print(f"Last message: {last_message}")
            return last_message
        else:
            print("No messages found.")
            return None
    except Exception as e:
        print(f"Error while retrieving the last message: {e}")
        return None

def get_phone_number(driver):
    """Function to get the phone number of the last contact clicked"""
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div/div[2]'))
        )
        last_message = driver.find_elements(By.XPATH, '//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div/div[2]')
        last_message.click()

        # Now that we are in the chat, click the header to get the contact info
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header/div[2]/div[1]/div'))
        ).click()

        # Get the phone number
        contact_info = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span'))
        ).text
        print(f"Phone number: {contact_info}")
        return contact_info
    except Exception as e:
        print(f"Error while retrieving the contact number: {e}")
        return None

# Ask user to input phone number to start chatting
phone_number = input("Enter the phone number to start chatting with: ")

# Start the bot
while True:
    driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")
    
    # Wait for the user to scan the QR code or chat to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[3]/div/div/div[2]/div[1]/div[1]'))
    )

    # Retrieve the last message in the chat
    last_message = get_last_message(driver)

    if last_message:
        # Add logic for automatic replies based on the message content
        if "hi" in last_message.lower():
            send_whatsapp_msg(driver, phone_number, "Hello Sir/Madam.... I am Boobalan (+91782392353) Your Donor Relationship Manager. Would you like to donate?")
            print("Replied with donation message.")
        elif "yes" in last_message.lower() or "yeah" in last_message.lower():
            send_whatsapp_msg(driver, phone_number, "Ok, is there any special occasion?")
            print("Replied with occasion question.")
        elif "birthday" in last_message.lower() or "anniversary" in last_message.lower():
            send_whatsapp_msg(driver, phone_number, "Here is the plan!")
            print("Replied with plan message.")
        elif "no" in last_message.lower():
            send_whatsapp_msg(driver, phone_number, "Okay, thanks for your time!")
            print("Replied with thanks message.")
    
    # Sleep for a few seconds before checking again to avoid overloading the server
    time.sleep(5)

# Close the driver
driver.quit()
