from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import getpass

# Retrieve username and password from command-line arguments
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")
remaining_subjects = 0
counted = False

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
chrome_options.add_argument("--disable-infobars")  # Disable infobars
chrome_options.add_argument("--disable-extensions")  # Disable extensions

# Create WebDriver instance
service = Service()
driver = webdriver.Chrome(service=service)

# Define the target URL
url = "https://web2.plm.edu.ph/sfe/sfe_student.php"

# Example: Wait for an element to load
wait = WebDriverWait(driver, 10)


def main():
    try:
        # Navigate to the URL
        driver.get(url)

        try:
            login()
            select_subject()
        except Exception:
            select_subject()

        # Wait for some time (useful for debugging)
        time.sleep(5)

    finally:
        # Close the browser
        driver.quit()


def login():
    # Find the username field by name
    username_field = driver.find_element(By.NAME, "username")
    username_field.send_keys(username)
    # Find the password field by name
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    # Find the login button by name
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()


def select_subject():
    global remaining_subjects, counted

    while remaining_subjects != 0 or not counted:
        # Dropdown
        element = wait.until(EC.presence_of_element_located((By.ID, "subject")))

        # Count available subjects if not already counted
        if not counted:
            remaining_subjects = sum(
                1
                for option in element.find_elements(By.TAG_NAME, "option")
                if option.text != "Select Subject"
                and not option.get_attribute("disabled")
            )
            counted = True
            print(f"Remaining subjects: {remaining_subjects}")

        # Select the first option that is not "Select Subject" and not disabled
        for option in element.find_elements(By.TAG_NAME, "option"):
            if option.text != "Select Subject" and not option.get_attribute("disabled"):
                option.click()
                break

        # Find the start evaluation button by name
        eval_button = driver.find_element(By.NAME, "evaluateBtn")
        eval_button.click()

        eval()


def eval():
    global remaining_subjects

    finish_button = None

    while finish_button is None:
        # Wait until the page loads
        form = wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))

        # Find all <td> elements containing radio buttons
        tr_elements = form.find_elements(By.TAG_NAME, "tr")

        # Iterate through each <td>
        for tr in tr_elements:
            try:
                radio_buttons = tr.find_elements(
                    By.CSS_SELECTOR, "input[type='radio'] + label"
                )
                radio_buttons[0].click()
            except:
                continue

        textareas = form.find_elements(By.TAG_NAME, "textarea")

        for textarea in textareas:
            textarea.send_keys("N/A")

        try:
            # Find the next button by xpath
            next_button = driver.find_element(By.NAME, "next")
            next_button.click()
        except:
            try:
                finish_button = driver.find_element(By.NAME, "submiteval")
                finish_button.click()
                remaining_subjects -= 1
                break
            except:
                finish_button = None
                continue


main()
