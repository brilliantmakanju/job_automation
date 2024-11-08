from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver (this example uses Chrome; make sure you have the appropriate WebDriver installed)
driver = webdriver.Chrome()

# Define the input field details
input_details = {
    "input-firstName": "Brilliant",
    "input-lastName": "Makanju",
    "input-phoneNumber": "+2349015573136",
    "input-email": "brilliantmakanju5@gmail.com",
    "input-city": "Lagos",
    "input-state": "Lagos State",
    "file-resume-input": '/home/bmn/Downloads/Resume.pdf'  # The file path for the resume upload
}

# Function to fill input fields
def fill_input_fields(driver, input_details):
    for input_id, value in input_details.items():
        try:
            field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f"input#{input_id}"))
            )
            field.clear()
            field.send_keys(value)
        except Exception as e:
            print(f"Field with ID {input_id} not found. Error: {str(e)}. Skipping.")

# Function to click a button by its CSS selector
def click_button(driver, css_selector):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        button.click()
    except Exception as e:
        print(f"Button not found. Error: {str(e)}.")

# Function to upload a resume
def upload_resume(driver, file_path):
    try:
        radio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#ihl-useId-indeed-theme-provider-hbgkkv-1-file-resume-input"))
        )
        radio_button.click()
        
        label = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='ihl-useId-indeed-theme-provider-hbgkkv-1-file-resume-input']"))
        )
        label.click()
        
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(file_path)
    except Exception as e:
        print(f"Error uploading the file. Error: {str(e)}.")

# Function to fill dynamic experience fields
def fill_experience_fields(driver):
    try:
        # Example static experience fields
        experience_fields = {
            "How many years of Front-end development experience do you have?": "3",
            "How many years of CSS experience do you have?": "3",
            "How many years of React experience do you have?": "2"
        }
        
        # Fill out each experience field
        for question, answer in experience_fields.items():
            try:
                question_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[text()='{question}']/following-sibling::input"))
                )
                question_element.clear()
                question_element.send_keys(answer)
            except Exception as e:
                print(f"Experience question '{question}' not found. Error: {str(e)}. Skipping.")
    except Exception as e:
        print(f"Error filling experience fields. Error: {str(e)}.")

# Function to fill job experience form
def fill_job_experience_form(driver):
    try:
        job_details = {
            "input-jobTitle": "Front-end Developer",
            "input-company": "Tech Company"
        }
        
        for input_id, value in job_details.items():
            try:
                field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"input#{input_id}"))
                )
                field.clear()
                field.send_keys(value)
            except Exception as e:
                print(f"Field with ID {input_id} not found. Error: {str(e)}. Skipping.")
    except Exception as e:
        print(f"Error filling job experience form. Error: {str(e)}.")

# Main function to automate the form process
def automate_form(driver, input_details):
    try:
        # Open the target URL
        driver.get('https://www.jobisite.com/sj/id/9160184-Remote-Frontend-Engineer-,-PAYS$35HR-AUSTIN,-TX')  # Replace with your actual URL
        
        # Fill initial form
        fill_input_fields(driver, input_details)
        
        # Click the Continue button
        click_button(driver, '.ia-continueButton.ia-ContactInfo-continue.css-sbr3v1.e8ju0x50')
        
        # Upload the resume
        upload_resume(driver, input_details["file-resume-input"])
        
        # Click the Continue button
        click_button(driver, '.ia-continueButton.ia-ContactInfo-continue.css-sbr3v1.e8ju0x50')
        
        # Fill dynamic experience fields
        fill_experience_fields(driver)
        
        # Click the Continue button
        click_button(driver, '.ia-continueButton.ia-ContactInfo-continue.css-sbr3v1.e8ju0x50')
        
        # Fill job experience form
        fill_job_experience_form(driver)
        
        # Click the final Continue button
        click_button(driver, '.ia-continueButton.ia-ContactInfo-continue.css-sbr3v1.e8ju0x50')
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the WebDriver
        driver.quit()

# Run the automation
automate_form(driver, input_details)


