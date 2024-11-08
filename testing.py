import os
import random
import string
import datetime
import threading
import editdistance
from bs4 import BeautifulSoup
from selenium import webdriver


from pdf2docx import Converter
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)

is_logged_in = False

def generate_email(name):
    # Remove whitespace and convert to lowercase
    name = name.replace(" ", "").lower()
    # Generate a random number between 1000 and 9999
    random_number = random.randint(1000, 9999)
    # Generate a random character for uniqueness
    random_char = random.choice(string.ascii_letters)
    # Construct the email
    email = f"{name}{random_number}{random_char}@gmail.com"
    return email

def get_job_posting_links(driver, keyword):

    search_input = driver.find_element(By.ID, "skill")
    search_input.send_keys(keyword)

    search_button = driver.find_element(By.CSS_SELECTOR, "form button")
    search_button.click()

    # Wait for the job links to be present on the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div table tbody tr td a"))
    )

    # Find all job links
    job_links = driver.find_elements(By.CSS_SELECTOR, "div table tbody tr td a")

    job_urls = [link.get_attribute("href") for link in job_links]
    # driver.quit()

    first_3_jobs = job_urls[:1]

    # Get the last 2 elements
    last_2_jobs = job_urls[-2:]

    # Combine the first 3 and last 2 elements into a single list
    selected_jobs = first_3_jobs  + last_2_jobs
    return selected_jobs

def dismiss_cookie_popup(driver):
    try:
        # Wait for the cookie popup to be present
        cookie_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "shareaholic-cookie-consent-buttons")
            )
        )
        # Find the "Okay" button and click it to dismiss the popup
        okay_button = cookie_popup.find_element(
            By.CLASS_NAME, "shareaholic-accept-button"
        )
        okay_button.click()
        print("Dismissed cookie popup.")
        return True
    except NoSuchElementException:
        # Handle exception if cookie popup is not found
        print("Cookie popup not found.")
        return False
    except ElementClickInterceptedException:
        # Handle exception if there's an issue clicking the button
        print("Error clicking the 'Okay' button.")
        return False

def apply_to_jobs(driver):
    # Find the submit button
    submit_button = driver.find_element(By.CSS_SELECTOR, 'a.button.button-3d.button-black.nomargin')

    submit_button.click()

    # # Wait for the page content to load after clicking submit
    # wait = WebDriverWait(driver, 7000).until(
    #     EC.visibility_of_element_located(
    #         (By.CSS_SELECTOR, "div.modal-body")
    #     )
    # )

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@value="default"]'))
    )
    element.click()


def apply_to_jobs_without_loggined(driver, email, name, skill, resume_path):
    apply_buttons = driver.find_elements(By.CSS_SELECTOR, ".btn.btn-lg.btn-info")

    # Iterate through the buttons to find the one with href as 'javascript:showWithOutRegister();'
    for button in apply_buttons:
        href = button.get_attribute("href")
        if href == "javascript:showWithOutRegister();":
            button.click()
            print("Clicked on 'Quick apply' button.")
            break

    driver.find_element(By.NAME, "rname").send_keys(name)
    driver.find_element(By.NAME, "remail").send_keys(email)
    driver.find_element(By.NAME, "rskill").send_keys(skill)

    newName = "/home/bmn/Downloads/" + name + ".docx"

    cv = Converter(resume_path)
    cv.convert(newName, start=0, end=None)

    resume_field = driver.find_element(By.NAME, "resume")
    resume_field.send_keys(newName)
    # Upload resume file

    # Find the submit button
    submit_button = driver.find_element(By.CSS_SELECTOR, 'a.button.button-3d.button-black.nomargin')

    submit_button.click()

    # Wait for the page content to load after clicking submit
    wait = WebDriverWait(driver, 7000).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.postcontent.bothsidebar.nobottommargin.clearfix")
        )
    )

    # Parse the HTML content
    page_source_after_click = driver.page_source
    soup = BeautifulSoup(page_source_after_click, "html.parser")

    # Find the <font> tag with color="red"
    font_tag = soup.find("font", color="red")
    if font_tag:
        # Extract the text content
        text_content = font_tag.get_text()

        # Split the text content by lines
        lines = text_content.split('\n')

        # Iterate over each line and extract username and password
        username = None
        password = None
        for line in lines:
            if 'UserName' in line:
                username = line.split(':')[1].strip()
            elif 'Password' in line:
                password = line.split(':')[1].strip()

        print("Username:", username)
        print("Password:", password)
        driver.quit()
    else:
        # driver.quit()
        print("No font tag with color='red' found.")


def get_job_page_content(driver,url, email, name, skill, resume_path):
    global is_logged_in
    driver.get(url)
    page_source = driver.page_source

    # Dismiss the cookie popup
    # cookies = dismiss_cookie_popup(driver)

    if not is_logged_in:
        # if cookies:
        #     apply_to_jobs_without_loggined(driver, email, name, skill, resume_path)
        apply_to_jobs_without_loggined(driver, email, name, skill, resume_path)
    else:
        # if not cookies:
        #     print("Cookie popup not found.")
        #     apply_to_jobs(driver)
        apply_to_jobs(driver)
    

def is_similar(word1, word2, threshold=0.7):
    # Calculate the Levenshtein distance between the words
    distance = editdistance.eval(word1, word2)
    # Calculate the similarity ratio
    similarity_ratio = 1 - (distance / max(len(word1), len(word2)))
    # Check if the similarity ratio is above the threshold
    return similarity_ratio >= threshold

def login_job(driver, username, password):
    global is_logged_in
    driver.find_element(By.ID, "userName").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)

    login_button = driver.find_element(By.ID, "login-form-submit")

    # Get the new URL after the action
    login_button.click()

    initial_url = driver.current_url
    new_url = "https://www.jobisite.com/dashBoard.htm?infoCd="

    page_source_after_click = driver.page_source
    soup = BeautifulSoup(page_source_after_click, "html.parser")

    # Find the <font> tag with color="red"
    success = is_similar(initial_url, new_url)
    if success:
        is_logged_in = True
    else:
        font_tag = soup.find("font", color="red")
        text_details = font_tag.get_text()
        if text_details == "Invalid Login Details.":
            is_logged_in = False


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome()
    driver.get("https://www.jobisite.com/")
    name = input("Enter your Name: ")
    email = input("Enter your Email: ")
    skills = input('Enter your skills: ')
    search_keyword = input('Enter Search Keyword: ')
    if not is_logged_in:
        login_job(driver,email,name)
        if is_logged_in == False:
            print("Login Failed")
        else: 
            print('Login Successfully')
            driver.get("https://www.jobisite.com/")
            job_urls = get_job_posting_links(driver, search_keyword)
            # Check if job_urls is a single URL or a list of URLs
            if isinstance(job_urls, str):
                job_urls = [job_urls]  # Convert to list if single URL

            # Function to apply to a job
            # def apply_job(url):

            for job_url in job_urls:
                get_job_page_content(
                    driver,
                    job_url,
                    email,
                    name,
                    skills,
                    "/home/bmn/Downloads/Black and White Simple Business School Graduate Corporate Resume.pdf",
                )


            # Create and start a thread for each job URL
            # threads = []
            # for job_url in job_urls:
            #     thread = threading.Thread(target=apply_job, args=(job_url,))
            #     threads.append(thread)
            #     thread.start()

            # # Wait for all threads to finish
            # for thread in threads:
            #     thread.join()
    else:
        print('Already Logged In')

# search_url = "https://www.jobisite.com/"

# if confirm == 'y':
# print(is_logged_in)


