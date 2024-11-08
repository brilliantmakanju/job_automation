import os
import time
import json
import random
import string
import logging
from openai import OpenAI
from functools import wraps
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from http_request_randomizer.requests.proxy.ProxyObject import Protocol
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# Define User Information
user_info = {
    "age_verification": "Yes",  # Or "No"
    "work_authorization": "Yes",  # Or "No"
    "referral_source": "Glassdoor",
    "current_employment_status": "No",  # Or "Yes"
    "relationship_with_employees": "No",  # Or "Yes, Name: Relationship"
    "education": "Yes",  # Or "No"
    "years_of_experience": {
        "business_systems_application": 5,
        "project_lead_or_supervisory": 2,
    },
    "certifications": "Yes",  # Or "No"
    "telecommuting_availability": "Yes",  # Or "No"
    "salary_requirements": "Yes",  # Or "No"
    "personal_data": {
        "race_ethnicity": "Asian",
        "gender": "Male",
        "veteran_status": "I AM NOT A PROTECTED VETERAN",
        "disability_status": "No, I do not have a disability and have not had one in the past",
    },
    "contact_information": {
        "phone": "123-456-7890",
        "linkedin": "linkedin.com/in/username",
    },
    "reasons_for_interest": "I am attracted to the company's innovative projects.",
    "location": {
        "americas": "Yes",  # Or "No"
        "visa_sponsorship_required": "No",  # Or "Yes"
    },
}

user_info_dev = {
    "name": "Brilliant Makanju",
    "phone": "+2349015573136",
    "email": "brilliantmakanju5@gmail.com",
    "role": "Full Stack Developer",
    "address": "123 Main Street, Lagos, Nigeria",
    "linkedin": "https://www.linkedin.com/in/brilliant-makanju",
    "github": "https://github.com/brilliantmakanju",
    "skills": ["JavaScript", "Python", "React", "Node.js", "Django", "HTML", "CSS"],
    "experience": [
        {
            "company": "Tech Innovators Ltd",
            "position": "Senior Full Stack Developer",
            "duration": "Jan 2020 - Present",
            "responsibilities": [
                "Lead a team of developers to build and maintain web applications",
                "Implemented new features and optimized existing ones",
                "Collaborated with cross-functional teams to define and design new features",
            ],
        },
        {
            "company": "Code Masters Inc",
            "position": "Full Stack Developer",
            "duration": "Jan 2018 - Dec 2019",
            "responsibilities": [
                "Developed and maintained web applications using JavaScript and Python",
                "Worked with designers to create user-friendly interfaces",
                "Optimized applications for maximum speed and scalability",
            ],
        },
    ],
    "education": [
        {
            "institution": "University of Lagos",
            "degree": "Bachelor of Science in Computer Science",
            "graduation_year": 2017,
        }
    ],
    "certifications": [
        {
            "name": "Certified JavaScript Developer",
            "issuing_organization": "JavaScript Institute",
            "issue_date": "Mar 2018",
        },
        {
            "name": "Full Stack Web Development Certification",
            "issuing_organization": "FreeCodeCamp",
            "issue_date": "Nov 2017",
        },
    ],
    "languages": ["English", "Yoruba"],
    "preferred_pronouns": "He/Him",
    "linkedin_profile": "https://www.linkedin.com/in/brilliant-makanju",
    "salary_expectations": "100,000 USD per year",
    "remote_experience_years": 3,
    "adapt_to_california_hours": "Yes",
    "authorized_to_work_in_usa": "No",
    "coding_assessment_consent": "Yes",
    "frontend_experience_years": 5,
    "react_skill_rating": 9,
    "javascript_skill_rating": 9,
}


user_input = {
    "jobTitle": "Software Developer",  # Example input, should be replaced by actual user input or logic
    "companyName": "Tech Company",  # Example input, should be replaced by actual user input or logic
    "project": "AI Project",  # Example input for project if no job experience
}

# class="Button_applyButton__pYKk1 Button_greenTheme__EXYIV"
# class="button_Button__MlD2g button-base_Button__knLaX"

# ia-continueButton ia-Question-continue css-sbr3v1 e8ju0x50
# ia-continueButton ia-Question-continue css-sbr3v1 e8ju0x50
# ia-continueButton ia-Question-continue css-sbr3v1 e8ju0x50

# ia-BasePage-component ia-BasePage-component--withContinue
# ia-BasePage-component ia-BasePage-component--withContinue
# ia-BasePage ia-Questions ia-PageAnimation-enter-done
# ia-BasePage ia-Questions ia-PageAnimation-enter-done
# ia-BasePage ia-Questions ia-PageAnimation-enter-done
#
api_keyDetail = os.getenv("OPENAI_API_KEY")

job_description_summary = None


class JobApplicationAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.automate_form_filler = None

    def automate_forms(self):
        if self.automate_form_filler is None:
            self.automate_form_filler = FormFiller(self.driver)
        return self.automate_form_filler

    def checkifCaptcha(self):
        try:
            captcha = self.driver.find_element(By.CLASS_NAME, "challenge-form")
            # self.driver.quit()

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            print("Captcha")
            return True
        except Exception as e:
            print("No captcha found 2.")
            return False

    def check_current_section(self):
        self.checkifCaptcha()
        print("Checking the current section...")
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ia-BasePage-component"))
            )
            container_divs = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'ia-BasePage-component--withContinue')]",
            )
            if container_divs:
                print("In the questions section.")
                return True
            else:
                print("In the preview section.")
                return False
        except Exception as e:
            self.checkifCaptcha()
            print(f"An error occurred while checking the current section: {e}")
            return None

    def click_preview_section(self):
        global job_description_summary
        # self.checkifCaptcha()
        print("Clicking on the preview section link...")
        try:
            time.sleep(10)
            preview_link = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@class='ia-SmartApplyPreviewSection-linkBox']/span/a[@class='ia-PreviewSection-link' and text()='Add']",
                    )
                )
            )
            preview_link.click()
            return True
        except Exception as e:
            time.sleep(10)
            # self.checkifCaptcha()
            if self.checkifCaptcha():
                print("Captcha found")
                return False
            else:
                check_section = self.check_current_section()
                if check_section == True:
                    self.automate_forms().fill_form(job_description_summary)
                else:
                    self.fill_cv("Working")
                    print("dev ended successfully or failed")
            print(f"An error occurred while clicking on the preview section link: {e}")
            return False

    def click_label(self):
        print("Clicking on the label...")
        label_elements = self.driver.find_element(
            By.XPATH, "//label[@data-testid='CoverLetterRadioCard-label']"
        )

        # ihl-useId-indeed-theme-provider-nsyxre-4
        label_elements.click()

    def click_textarea(self):
        print("Clicking on the textarea...")
        textarea_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//textarea[@data-testid='CoverLetter-textarea' and @placeholder='Type a cover letter']",
                )
            )
        )
        textarea_element.click()
        return textarea_element

    def submit_cv(self):
        # ia-continueButton ia-SupportingDocument-continue css-sbr3v1 e8ju0x50
        # ia-continueButton ia-SupportingDocument-continue css-sbr3v1 e8ju0x50
        submit_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'ia-continueButton ia-SupportingDocument-continue css-sbr3v1 e8ju0x50')]//span[text()='Update']",
                )
            )
        )
        submit_button.click()

    def write_cv(self, cv_text):
        print("Writing CV into the textarea...")
        textarea_element = self.click_textarea()
        textarea_element.clear()
        textarea_element.send_keys(cv_text)
        print("CV written into the textarea.")

    def fill_cv(self, cv_text):
        try:
            if self.click_preview_section():
                self.click_label()
                self.write_cv(cv_text)
                self.submit_cv()
                print("Waiting for user to review the CV...")
                time.sleep(2)  # Adjust the wait time as needed
                print("Adding CV link found")
                return True

            else:
                # Wait for the submit button to be clickable and then click it
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//div[contains(@class, 'ia-BasePage-footer')]//button[contains(@class, 'ia-continueButton') and .//span[text()='Submit your application']]",
                        )
                    )
                )
                submit_button.click()
                print("Submit button clicked.")
                return False

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def submit_review(self):
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class, 'ia-BasePage-footer')]//button[contains(@class, 'ia-continueButton') and .//span[text()='Submit your application']]",
                )
            )
        )
        submit_button.click()


class FormFiller:
    def __init__(self, driver):
        self.driver = driver
        self.user_info = user_info_dev
        # Set up OpenAI API
        self.submits = None
        self.openai_client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1", api_key=api_keyDetail
        )

    def check_section(self):
        if self.submits is None:
            self.submits = JobApplicationAutomation(self.driver)
        return self.submits


    def generate_response(self, question, job_description):
        time.sleep(4)
        user_info_json = json.dumps(user_info_dev, indent=4)
        prompt = f"""
        You are an intelligent assistant helping a candidate complete a job application form. Use the information provided in {user_info_json} to answer each question accurately, as if you were the candidate. Always follow the guidelines below when answering any question:

        Direct Responses: Provide only the answer required, without any extra commentary or indication that the response is generated by an AI.  
        Clean Formatting: Ensure answers are free from unnecessary characters, such as quotation marks or extraneous symbols.  
        Accurate Representation: Use the details from user_info_json to respond as the candidate.

        Instructions for Answering Questions:
        - Years of Experience: State the number of years, or "0" if there is no experience.
        - Work Hour Adaptation: Answer "Yes" or "No".
        - Legal Work Authorization: Answer "Yes" or "No".
        - Consent to Assessment: Answer "Yes" or "No".
        - Skill Rating (1-10): Provide a numerical rating without additional text.
        - Experience and Familiarity: Answer "Yes" or "No," based on the information provided.

        Examples of Questions and Answers Based on Candidate Information:  
        Use the "Expected reply" examples as a guideline to format your responses correctly. Do not include phrases like "Expected reply format" in your answers.

        1. Question: How many years of Front-end development experience do you have?  
        Expected reply: 5

        2. Question: How many years of remote working experience do you have?  
        Expected reply: 3

        3. Question: Are you able to adapt to overlap your workday with California hours (i.e., until 4:00 p.m. Pacific Time)?  
        Expected reply: Yes

        4. Question: Are you legally authorized to work in the USA without requiring employer sponsorship now or in the future?  
        Expected reply: Yes

        5. Question: There will be a 60 min coding assessment as one of the steps in our recruitment process. Do you consent to receiving this assessment?  
        Expected reply: Yes

        6. Question: How many years of experience do you have with frontend development languages like JavaScript and/or React?  
        Expected reply: 6

        7. Question: On a scale of 1-10 (10 being the best), how would you rate your skills with React?  
        Expected reply: 8

        8. Question: On a scale of 1-10 (10 being the best), how would you rate your skills with JavaScript?  
        Expected reply: 9

        9. Question: Do you have experience working with databases such as MySQL, PostgreSQL, or MongoDB?  
        Expected reply: Yes

        10. Question: Are you familiar with version control systems like Git?  
            Expected reply: Yes

        11. Question: Have you worked with Agile methodologies in your previous projects?  
            Expected reply: Yes

        12. Question: Do you have experience in developing and deploying applications in cloud environments (e.g., AWS, Azure, Google Cloud Platform)?  
            Expected reply: Yes

        13. Question: Have you ever led a team of developers in a project?  
            Expected reply: Yes

        14. Question: Are you comfortable working in a fast-paced startup environment?  
            Expected reply: Yes

        15. Question: Have you contributed to open-source projects before?  
            Expected reply: Yes

        16. Question: Are you proficient in using front-end frameworks like Vue.js or Angular?  
            Expected reply: Yes

        17. Question: Have you ever conducted code reviews for other team members?  
            Expected reply: Yes

        18. Question: Are you familiar with continuous integration and continuous deployment (CI/CD) pipelines?  
            Expected reply: Yes

        19. Question: Have you worked with RESTful APIs in your previous projects?  
            Expected reply: Yes

        20. Question: Are you experienced in using CSS preprocessors like Sass or Less?  
            Expected reply: Yes

        21. Question: Have you built responsive web applications that work across multiple devices and screen sizes?  
            Expected reply: Yes

        22. Question: Are you comfortable working with UI/UX designers to implement their designs into functional web applications?  
            Expected reply: Yes

        23. Question: Have you ever implemented authentication and authorization mechanisms in web applications?  
            Expected reply: Yes

        24. Question: Are you familiar with performance optimization techniques for web applications?  
            Expected reply: Yes

        25. Question: Have you used testing frameworks like Jest or Mocha for unit and integration testing?  
            Expected reply: Yes

        26. Question: Are you experienced in debugging and troubleshooting issues in web applications?  
            Expected reply: Yes

        27. Question: Have you ever worked on projects involving real-time web communication using WebSockets or similar technologies?  
            Expected reply: Yes

        28. Question: Are you knowledgeable about web security best practices and common vulnerabilities?  
            Expected reply: Yes

        29. Question: Have you integrated third-party APIs into your web applications before?  
            Expected reply: Yes

        30. Question: Are you experienced in optimizing web applications for search engine optimization (SEO)?  
            Expected reply: Yes

        31. Question: Have you worked on projects involving data visualization using libraries like D3.js or Chart.js?  
            Expected reply: Yes

        32. Question: Are you comfortable working with frontend build tools like Webpack or Parcel?  
            Expected reply: Yes

        33. Question: Have you ever implemented internationalization (i18n) and localization (l10n) in web applications?  
            Expected reply: Yes

        34. Question: Are you proficient in using design patterns in your code architecture?  
            Expected reply: Yes

        35. Question: Have you ever conducted technical interviews for hiring new developers?  
            Expected reply: Yes

        36. Question: Are you experienced in mentoring junior developers and helping them grow their skills?  
            Expected reply: Yes

        37. Question: Have you contributed to documentation efforts for codebases or projects?  
            Expected reply: Yes

        38. Question: Are you familiar with containerization technologies like Docker?  
            Expected reply: Yes

        39. Question: Have you ever presented technical topics or projects at conferences or meetups?  
            Expected reply: Yes

        40. Question: Are you passionate about staying up-to-date with the latest trends and advancements in web development?  
            Expected reply: Yes

        41. Question: What is your annual salary expectation?  
            Expected reply: 100000

        42. Question: Have you ever worked with GraphQL in your projects?  
            Expected reply: Yes

        43. Question: Are you familiar with DevOps practices?  
            Expected reply: Yes

        44. Question: Have you worked with state management libraries like Redux or MobX?  
            Expected reply: Yes

        45. Question: Are you comfortable working in a fully remote team?  
            Expected reply: Yes

        46. Question: Have you worked with TypeScript in your projects?  
            Expected reply: Yes

        47. Question: Are you familiar with serverless architectures?  
            Expected reply: Yes

        48. Question: Have you built PWA (Progressive Web Apps) before?  
            Expected reply: Yes

        49. Question: Are you experienced in using WebAssembly?  
            Expected reply: Yes

        50. Question: Do you have experience with mobile development frameworks like React Native or Flutter?  
            Expected reply: Yes

        Use these guidelines to provide clear and precise responses to each question, ensuring they reflect the candidate's experience and qualifications accurately. If specific information is not available, use reasonable assumptions based on the provided data to ensure a consistent and complete response.
        
        Here is the question: {question}
        """

        # fine_tune = self.openai_client.fine_tuning

        response = self.openai_client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[
                # {
                #     "role": "system",
                #     "content": prompt,
                # },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False,
        )

        #         temperature=1,
        # max_tokens=256,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0,
        # # stream=False,
        print(response.choices[0].message.content, "\n")
        return response.choices[0].message.content

    def handle_radio_input(self, label_text):
        return "yes" if "yes" in label_text.lower() else "no"

    def handle_dropdown_input(self, label_text, job_description):
        return self.generate_response(label_text, job_description)

    def fill_input_fields(self, label_text, job_description):
        input_value = self.generate_response(label_text, job_description)
        print(input_value)
        return input_value

    def is_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def sanitize_number(self, value):
        if self.is_number(value):
            # Remove any extraneous characters and ensure it's formatted correctly
            sanitized_value = str(int(float(value)))
            return sanitized_value
        return value

    def fill_form_field(self, input_field, input_value):
        if input_value is not None:
            input_field.clear()  # Clear the field before entering new value
            input_field.send_keys(input_value)
            print(f"Input field filled with value: '{input_value}'.")
        else:
            print("Input value is None, skipping input field.")

    # Function to get input value using GPT
    def get_input_values(self, label_text, user_input):
        prompt = f"Given the user information: {user_input}"
        question = (
            f"{prompt}, what should be the value for the field labeled '{label_text}'?"
        )

        response = self.openai_client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[
                {"role": "user", "content": question},
            ],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False,
        )
        return response.choices[0].message.content

    def fill_forms(self):
        user_input = {
            "jobTitle": "Software Developer",  # Example input, should be replaced by actual user input or logic
            "companyName": "Tech Company",  # Example input, should be replaced by actual user input or logic
            "project": "AI Project",  # Example input for project if no job experience
        }
        # Get all fieldsets to process each form section
        fieldsets = self.driver.find_elements(
            By.CSS_SELECTOR, "div.css-3ukcm5.e37uo190 > fieldset.css-14dgf3i.eu4oa1w0"
        )

        for fieldset in fieldsets:
            label_wrapper = fieldset.find_element(
                By.CSS_SELECTOR, "legend.css-1bx5raa.eu4oa1w0 > label.ia-LabelWrapper"
            )
            label_text = label_wrapper.find_element(
                By.CSS_SELECTOR, "span.ia-LabelWrapper-label"
            ).text
            optional_text_elements = label_wrapper.find_elements(
                By.CSS_SELECTOR, "span.ia-LabelWrapper-optional"
            )

            # Check if the field is optional
            is_optional = len(optional_text_elements) > 0

            print(is_optional, "Optional text")

            # Get all inputs within the fieldset
            inputs = fieldset.find_elements(By.CSS_SELECTOR, "input")

            for input_element in inputs:
                input_name = input_element.get_attribute("name")
                if not input_name and is_optional:
                    continue  # Skip optional fields without a name

                input_value = self.get_input_values(label_text, user_input)
                if input_value:
                    input_element.clear()
                    input_element.send_keys(input_value)
                    time.sleep(2)  # Interval between inputs for demo purposes

        # If user has no job experience, fill in the project
        if not user_input.get("jobTitle") and not user_input.get("companyName"):
            project_input = driver.find_element(
                By.CSS_SELECTOR, "input[id='companyName']"
            )
            project_input.clear()
            project_input.send_keys(user_input.get("project", "Default Project"))
            project_inputs = driver.find_element(
                By.CSS_SELECTOR, "input[id='jobTitle']"
            )
            project_inputs.clear()
            project_inputs.send_keys(user_input.get("Frontend Developer"))

    def fill_form(self, job_info):
        print("Searching for container div...")
        container_xpaths = [
            "//div[contains(@class, 'ia-BasePage-component') and contains(@class, 'ia-BasePage-component--withContinue')]",
            "//div[contains(@class, 'ia-BasePage') and contains(@class, 'ia-Questions') and contains(@class, 'ia-PageAnimation-enter-done')]",
        ]

        for container_xpath in container_xpaths:
            container_divs = self.driver.find_elements(By.XPATH, container_xpath)
            if container_divs:
                container_div = container_divs[0]  # Use the first found container div
                self.fill_forms()
                print("Container div found. Filling form...")
                labels = container_div.find_elements(By.TAG_NAME, "label")
                print(
                    f"Number of labels found: {len(labels)}"
                )  # Print number of labels found

                for label in labels:
                    print("Processing label...")
                    label_text = self.get_label_text(label)
                    print(f"Label text: {label_text}")

                    # Check if label is optional
                    if "(optional)" in label_text:
                        print("Optional label found. Skipping input field.")
                        continue  # Skip to the next label if it's optional

                    input_id = label.get_attribute("for")
                    if input_id:
                        input_field = self.driver.find_element(By.ID, input_id)
                        if input_field:
                            input_type = input_field.get_attribute("type")
                            if input_type == "radio":
                                input_value = self.handle_radio_input(label_text)
                                input_field.click()  # Select the radio button
                                print(f"Radio button '{input_value}' clicked.")
                            elif input_type == "number":
                                input_value = self.fill_input_fields(
                                    label_text, job_info
                                )
                                print(f"Input value to be filled: {input_value}")
                                if (
                                    input_value is not None
                                ):  # Check if input_value is not None
                                    input_field.send_keys(int(input_value))
                                    print(
                                        f"Input field filled with value: '{int(input_value)}'."
                                    )
                                else:
                                    print("Input value is None, skipping input field.")
                            else:
                                input_value = self.fill_input_fields(
                                    label_text, job_info
                                )
                                print(f"Input value to be filled: {str(input_value)}")
                                if (
                                    input_value is not None
                                ):  # Check if input_value is not None
                                    input_field.send_keys(str(input_value))
                                    print(
                                        f"Input field filled with value: '{str(input_value)}'."
                                    )
                                else:
                                    print("Input value is None, skipping input field.")

                self.click_continue_button()

    # def get_label_text(self, label):
    #     try:
    #         label_span = label.find_element(By.TAG_NAME, 'span')
    #         return label_span.text()
    #     except:
    #         return label.text()
    # Define the method to get label text properly
    def get_label_text(self, label):
        span = label.find_elements(By.TAG_NAME, "span")
        print(span)
        if span:
            return span[0].text.strip()
        return label.text.strip()

    def click_continue_button(self):
        try:
            # Check for the button with the specified class
            button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ia-continueButton"))
            )
            button.click()
            print('Clicked button with class "ia-continueButton".')
            time.sleep(3)
        except:
            self.check_section().fill_cv("dev")
            self.check_section().submit_review()
            print('Button with class "ia-continueButton" not found.')

        try:
            # Check for a button inside a div with the specified class
            div = self.driver.find_element(By.CLASS_NAME, "ia-Question-continue")
            button_in_div = div.find_element(By.TAG_NAME, "button")
            button_in_div.click()
            print('Clicked button inside div with class "ia-Question-continue".')
        except:
            time.sleep(2)
            self.check_section().fill_cv("dev")
            self.check_section().submit_review()
            print('Button inside div with class "ia-Question-continue" not found.')


class GlassdoorJobAutomation:
    def __init__(self, driver):
        self.driver = driver
        self.openai_client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1", api_key=api_keyDetail
        )

    def get_job_details(self):
        time.sleep(2)
        # WebDriverWait()
        show_more_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='JobDetails_showMore___Le6L']")
            )
        )
        # show_more_btn = self.driver.find_element(
        #     By.XPATH, "//div[@class='JobDetails_showMoreWrapper__ja2_y']"
        # )
        show_more_btn.click()
        time.sleep(2)
        job_description_element = self.driver.find_element(
            By.XPATH,
            '//div[@class="JobDetails_jobDescriptionWrapper___tqxc JobDetails_jobDetailsSectionContainer__o_x6Z JobDetails_paddingTopReset__IIrci"]',
        )
        job_description_with_tags = job_description_element.text
        time.sleep(2)

        return job_description_with_tags

    def get_job_info_gpt(self):
        job_description = self.get_job_details()
        print("Job description: Summary:")
        time.sleep(2)
        completion = self.openai_client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": f"""Extract the following details from the job description:Job Title,Location,Required Skills,Qualifications, Responsibilities
                    \n Job Description: {job_description}""",
                },
            ],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False,
        )

        # # Extracted information from ChatGPT response
        job_details = completion.choices[0].message.content
        print(job_details)
        global job_description_summary
        # job_details = "Job description summary"
        job_description_summary = job_details
        # job_details = "Job Descriptiondfdf"
        return job_details


class JobSearch:
    def __init__(self, driver):
        self.driver = driver
        self.job_automation = GlassdoorJobAutomation(driver)
        self.glassdoor_form_automation = None  # Initialize as None initially
        self.glassdoor_job_search_automation = None  # Initialize as None initially

    def get_glassdoor_job_search_automation(self):
        if self.glassdoor_job_search_automation is None:
            self.glassdoor_job_search_automation = GlassdoorJobSearchAutomation(
                self.driver
            )
        return self.glassdoor_job_search_automation

    def get_glassdoor_form_automation(self):
        if self.glassdoor_form_automation is None:
            self.glassdoor_form_automation = GlassdoorFormAutomation(self.driver)
        return self.glassdoor_form_automation

    def click_jobs(self):
        self.get_glassdoor_job_search_automation().close_popup()
        time.sleep(2)
        ul_element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//ul[@class='JobsList_jobsList__lqjTr']")
            )
        )

        li_elements = ul_element.find_elements(
            By.CSS_SELECTOR,
            "li.JobsList_jobListItem__wjTHv",
        )

        self.get_glassdoor_job_search_automation().close_popup()

        for index, li in enumerate(li_elements):
            self.get_glassdoor_job_search_automation().close_popup()
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", li)
                li.click()
                time.sleep(2)
                self.get_glassdoor_job_search_automation().close_popup()
                time.sleep(2)
                print("Progressing")
                job_info = self.job_automation.get_job_info_gpt()
                job_info = "sdsd"
                print("Job description")
                if job_info == "wew":
                    pass
                else:
                    print("Job info working")
                    current_url = self.driver.current_url
                    self.get_glassdoor_job_search_automation().close_popup()
                    self.get_glassdoor_job_search_automation().click_apply_easy()  # Call the method here
                    time.sleep(2)
                    # # # Switch to the new tab
                    new_url = self.driver.current_url

                    if current_url == new_url:
                        print("Current URL is already")
                        time.sleep(2)
                        self.get_glassdoor_job_search_automation().close_popup()

                        self.driver.switch_to.window(self.driver.window_handles[1])
                        # self.driver.curr
                        print("Switched to window with form")
                        print(self.driver.current_url)
                        GlassdoorFormAutomation(self.driver).automate_form(job_info)
                        time.sleep(3)
                        self.driver.close()

                        # Switch back to the main tab
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        print(self.driver.current_url)

                    else:

                        print("New window")
                        time.sleep(2)
                        self.get_glassdoor_job_search_automation().close_popup()

                        GlassdoorFormAutomation(self.driver).automate_form(job_info)
                        time.sleep(2)
                        self.driver.back()

                    # main_tab = self.driver.current_window_handle

                    # # Switch to the new tab
                    # self.driver.switch_to.window(self.driver.window_handles[1])

                    # # Wait until the page loads completely (you can change the condition based on your requirements)
                    # WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    # self.get_glassdoor_job_search_automation().close_popup()
                    # # Check if the page has changed from the main tab
                    # if self.driver.current_window_handle != main_tab:
                    #     # Perform actions specific to the new tab
                    #     time.sleep(2)
                    #     GlassdoorFormAutomation(self.driver).automate_form()

                    #     # Close the new tab
                    #     self.driver.close()

                    #     # Switch back to the main tab
                    #     self.driver.switch_to.window(main_tab)
                    # else:
                    #     # Perform actions specific to the main tab
                    #     time.sleep(2)
                    #     GlassdoorFormAutomation(self.driver).automate_form()
                    # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
                    # driver.switch_to.window(driver.window_handles[1])
                    # time.sleep(2)
                    # self.get_glassdoor_form_automation().automate_form()
                    # time.sleep(2)
                    # # # Close the new tab and switch back to the original tab
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                # time.sleep(12)
            except Exception as e:
                print(f"Error occurred while processing li index {index}: {e}")


# ia-PreviewSection-link
# css-mza3f0 e37uo190
# css-besaou e1jgz0i2


class GlassdoorFormAutomation:
    def __init__(self, driver):
        self.check = None
        self.driver = driver
        self.glassdoor_job_search_automation = None
        self.automate_form_filler = FormFiller(driver)

    def check_section(self):
        if self.check is None:
            self.check = JobApplicationAutomation(self.driver)
        return self.check

    def get_glassdoor_job_search_automation(self):
        if self.glassdoor_job_search_automation is None:
            self.glassdoor_job_search_automation = GlassdoorJobSearchAutomation(
                self.driver
            )
        return self.glassdoor_job_search_automation

    # def auto_filler(self):
    #     if self.automate_form_filler is None:
    #         self.automate_form_filler = FormFiller(self.driver)
    #     return self.automate_form_filler()

    def fill_input_fields(self, input_details):
        # self.get_glassdoor_job_search_automation().close_popup()
        for input_id, value in input_details.items():
            try:
                field = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, f"input#{input_id}")
                    )
                )
                field.clear()
                field.send_keys(value)
            except Exception as e:
                print(f"Field with ID {input_id} not found. Error: {str(e)}. Skipping.")

    def click_button(self, css_selector):
        # self.get_glassdoor_job_search_automation().close_popup()
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )
            button.click()
        except Exception as e:
            print(f"Button not found. Error: {str(e)}.")

    def upload_resume(self):
        # self.get_glassdoor_job_search_automation().close_popup()
        try:
            file_input = self.driver.find_element(
                By.CSS_SELECTOR, "input[data-testid='FileResumeCard-file-input']"
            )
            file_input.send_keys("/home/riter/Downloads/Resume.pdf")
        except Exception as e:
            print(f"Error uploading the file. Error: {str(e)}.")

    def automate_form(self, job_info):
        print("Automating form begins")
        # self.get_glassdoor_job_search_automation().close_popup()
        input_details = {
            "input-firstName": "Brilliant",
            "input-lastName": "Makanju",
            "input-phoneNumber": "+2349015573136",
            "input-email": "brilliantmakanju5@gmail.com",
            # "input-location.city": "Lagos State",
            # "file-resume-input": '/home/riter/Downloads/Resume.pdf'  # The file path for the resume upload
        }
        print("Form filling started...")
        try:
            print("Removed code lines")
            self.fill_input_fields(input_details)
            time.sleep(3)
            self.click_button(
                ".ia-continueButton.ia-ContactInfo-continue.css-sbr3v1.e8ju0x50"
            )
            time.sleep(3)
            self.upload_resume()
            time.sleep(3)
            self.click_button(
                ".ia-continueButton.ia-Resume-continue.css-sbr3v1.e8ju0x50"
            )
            time.sleep(3)
            print("started dev")
            check_section = self.check_section().check_current_section()
            if check_section == True:
                self.automate_form_filler.fill_form(job_info)
            else:
                # self.check_section().fill_cv('cv')
                # self.check_section().submit_review()
                print("dev ended successfully or failed")
        except Exception as e:
            print(f"An error occurred: {e}")

    #     self.glassdoor_job_search_automation = None  # Initialize as None initially

    # def get_glassdoor_job_search_automation(self):
    #     if self.glassdoor_job_search_automation is None:
    #         self.glassdoor_job_search_automation = GlassdoorJobSearchAutomation(self.driver)
    #     return self.glassdoor_job_search_automation


# success apply: icon-button_IconButton__nMTOc


class GlassdoorJobSearchAutomation:

    def __init__(self, driver):
        self.driver = driver
        self.job_search = JobSearch(driver)
        self.form_automation = GlassdoorFormAutomation(driver)

    def random_scroll_and_click(self):
        # Scroll randomly
        for _ in range(random.randint(2, 5)):
            scroll_height = random.randint(300, 700)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_height});")
            time.sleep(random.uniform(1, 3))

        # Click random elements
        # clickable_elements = self.driver.find_elements_by_tag_name('a')
        # if clickable_elements:
        #     random.choice(clickable_elements).click()
        #     time.sleep(random.uniform(2, 5))

    def search_job(self):
        # self.close_popup()
        # self.random_scroll_and_click()
        # self.driver.get("https://builtin.com/jobs/remote")
        # time.sleep(999)
        # pass
        # inputTitle = self.driver.find_element(By.ID, "searchBar-jobTitle")
        # inputTitle.send_keys("frontend")
        # inputTitle.submit()
        # time.sleep(3)

        self.get_easy_apply()

    def get_easy_apply(self):
        # self.close_popup()
        # self.random_scroll_and_click()

        buttons = self.driver.find_elements(
            By.CLASS_NAME, "SearchFiltersBar_pill__cT_sS.ToggleFilter_togglePill__Laytk"
        )

        # Iterate through the buttons to check their text
        for button in buttons:
            button_text = (
                button.text.strip().lower()
                # or button_text == "remote only"
            )  # Get the button text and convert to lowercase for comparison
            if button_text == "easy apply only":
                button.click()  # Click the button if it matches the criteria
                time.sleep(2)  # Wait for 2 seconds before the next click
                self.job_search.click_jobs()

        print("Started job selecting")
        # filter_btn = WebDriverWait(self.driver, 5).until(
        #     EC.element_to_be_clickable((By.CLASS_NAME, "SearchFiltersBar_pill__cT_sS ToggleFilter_togglePill__Laytk"))
        #     # SearchFiltersBar_pill__cT_sS ToggleFilter_togglePill__Laytk
        # )
        # filter_btn.click()

        # button = WebDriverWait(self.driver, 5).until(
        #     EC.element_to_be_clickable(
        #         (
        #             By.XPATH,
        #             "//button[contains(@class, 'SearchFiltersBar_labelButton__gF32h') and contains(text(), 'Most relevant')]",
        #         )
        #     )
        # )
        # button.click()
        # time.sleep(1)

        # button_recent = WebDriverWait(self.driver, 1).until(
        #     EC.element_to_be_clickable(
        #         (
        #             By.XPATH,
        #             "//div[contains(@class, 'SearchFiltersBar_dropdownOptionLabel___af5z') and contains(text(), 'Most recent')]",
        #         )
        #     )
        # )
        # button_recent.click()
        # time.sleep(3)

        # filter_btn = self.driver.find_element(
        #     By.CLASS_NAME, "SearchFiltersBar_pill__cT_sS.ToggleFilter_togglePill__Laytk"

        # )
        # filter_btn.click()
        # time.sleep(2)  # Wait for the filter options to be available

        # # Find and click the button for 'Most relevant'
        # button = self.driver.find_element(
        #     By.XPATH,
        #     "//button[contains(@class, 'SearchFiltersBar_labelButton__gF32h') and contains(text(), 'Most relevant')]",
        # )
        # button.click()
        # time.sleep(2)  # Wait for the dropdown options to be available

        # Find and click the button for 'Most recent'
        # button_recent = self.driver.find_element(
        #     By.XPATH,
        #     "//div[contains(@class, 'SearchFiltersBar_dropdownOptionLabel___af5z') and contains(text(), 'Most recent')]",
        # )
        # button_recent.click()
        # time.sleep(3)  # Wait for the page to update

        # showmore = self.showmore_job()
        # print(showmore)
        # if showmore:
        # else:
        #     pass

    def showmore_job(self):
        self.close_popup()
        load_complete = False
        while not load_complete:
            self.close_popup()
            try:
                self.close_popup()
                show_more_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@data-test='load-more']")
                    )
                )
                show_more_button.click()
                time.sleep(2)
                self.close_popup()

                try:
                    self.close_popup()
                    show_more_button = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//button[@data-test='load-more']")
                        )
                    )
                    self.close_popup()
                    load_complete = not show_more_button.is_displayed()
                except TimeoutException:
                    self.close_popup()
                    load_complete = True

            except StaleElementReferenceException:
                self.close_popup()
                print("Stale element reference error. Retrying...")
                continue
            except Exception as e:
                self.close_popup()
                print(f"Error occurred: {e}. Stopping the loop.")
                load_complete = True
        self.close_popup()
        return load_complete

    def close_popup(self):
        try:
            self.checkifCaptcha()
            close_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "CloseButton"))
            )
            close_btn.click()

        except (TimeoutException, StaleElementReferenceException):
            self.checkifCaptcha()
            print("Close button not found or stale.")

        try:
            # Wait for the iframe to be present and switch to it
            iframe = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//iframe[@title='Sign in with Google Dialogue']")
                )
            )
            print("Iframe element")

            # Change the iframe style using JavaScript
            self.driver.execute_script(
                """
                var iframe = arguments[0];
                iframe.style.width = "0";
                iframe.style.height = "0";
                iframe.style.overflow = "hidden";
                iframe.style.display = "none";
            """,
                iframe,
            )

            self.driver.switch_to.frame(iframe)

            # Wait for the close button to be clickable and click it
            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@id='close' and @role='button']")
                )
            )
            print("Close clicked successfully")
            close_button.click()

            # Switch back to the default content (if needed)
            self.driver.switch_to.default_content()

        except (TimeoutException, StaleElementReferenceException):
            self.checkifCaptcha()
            print("Google button not found or stale.")

    def checkifCaptcha(self):
        time.sleep(2)
        try:
            captcha = self.driver.find_element(By.CLASS_NAME, "ia-container")
            self.driver.quit()
            return True

        except Exception as e:
            print("No captcha found.")
            return False

    def click_apply_easy(self):
        self.close_popup()
        try:
            print("Will click apply button")
            button = self.driver.find_element(
                By.XPATH, '//div[@class="JobDetails_applyButtonContainer__L36Bs"]'
            )
            button.click()
            try:
                self.checkifCaptcha()
                close_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "CloseButton"))
                )
                close_btn.click()

                button.click()

                close_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "CloseButton"))
                )

                if close_btn:
                    self.driver.quit()

            except (TimeoutException, StaleElementReferenceException):
                self.checkifCaptcha()
                print("Close button not found or stale.")
            # button_Button__MlD2g button-base_Button__knLaX
            print("Button clicked successfully!")
            # time.sleep(2)
            # self.close_popup()

        except Exception as e:
            print(f"Button not found. Error: {str(e)}.")

    def click_jobs(self):
        ul_element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//ul[@class='JobsList_jobsList__lqjTr']")
            )
        )
        li_elements = ul_element.find_elements(
            By.CSS_SELECTOR,
            "li.JobsList_jobListItem__wjTHv.JobsList_dividerWithSelected__nlvH7",
        )

        for index, li in enumerate(li_elements):
            try:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", li)
                li.click()
                self.close_popup()
                time.sleep(2)
                self.click_apply_easy()
                time.sleep(2)
            except Exception as e:
                print(f"Error occurred while processing li index {index}: {e}")


if __name__ == "__main__":
    user_agent = UserAgent()
    req_proxy = RequestProxy(
        log_level=logging.ERROR, protocol=Protocol.HTTPS
    )  # you may get different number of proxy when  you run this at each time
    proxies = req_proxy.get_proxy_list()
    # # print(f"User Agent: {user_agent.random}")
    chrome_options = webdriver.FirefoxOptions()
    # chrome_options.add_argument(f"user-agent={user_agent.random}")
    # proxy = [
    #     "https://47.251.70.179:80",
    #     "https://20.44.189.184:3129",
    #     "https://20.44.188.17:3129",
    #     "https://20.219.176.57:3129",
    #     "https://189.240.60.166:9090",
    #     "https://184.168.124.233:5402",
    #     "https://189.240.60.164:9090",
    #     "https://189.240.60.168:9090",
    #     "https://5.45.107.19:3128",
    #     "https://47.243.166.133:18080",
    #     "https://47.251.43.115:33333",
    #     "https://200.174.198.86:8888",
    #     "https://172.183.241.1:8080",
    #     "https://20.204.212.76:3129",
    #     "https://189.240.60.163:9090",
    #     "https://212.92.148.164:8090",
    #     "https://103.237.144.232:1311",
    #     "https://160.86.242.23:8080",
    #     "https://20.204.214.23:3129",
    #     "https://20.204.212.45:3129",
    #     "https://47.88.31.196:8080",
    #     "https://218.76.247.34:30000",
    #     "https://72.10.160.94:18345",
    #     "https://45.77.147.46:3128",
    # ]
    # PROXY = [
    #     "47.251.70.179:80",
    #     "20.44.189.184:3129",
    #     "20.44.188.17:3129",
    #     "20.219.176.57:3129",
    #     "189.240.60.166:9090",
    #     "184.168.124.233:5402",
    #     "189.240.60.164:9090",
    #     "5.45.107.19:3128",
    #     "47.243.166.133:18080",
    #     "47.251.43.115:33333",
    #     "200.174.198.86:8888",
    #     "172.183.241.1:8080",
    #     "20.204.212.76:3129",
    #     "189.240.60.163:9090",
    #     "212.92.148.164:8090",
    #     "103.237.144.232:1311",
    #     "160.86.242.23:8080",
    #     "20.204.214.23:3129",
    #     "20.204.212.45:3129",
    #     "47.88.31.196:8080",
    #     "218.76.247.34:30000",
    #     "72.10.160.94:18345",
    #     "45.77.147.46:3128",
    # ]
    # # chrome_options.add_argument("--proxy-server=%s" % PROXY)
    # webdriver.DesiredCapabilities.FIREFOX["proxy"] = {
    #     "httpProxy": proxies,
    #     "ftpProxy": proxies,
    #     "sslProxy": proxies,
    #     "proxyType": "MANUAL",
    # }
    # options=chrome_options
    driver = webdriver.Firefox(options=chrome_options)
    driver.get("https://www.glassdoor.com/Job/frontend-jobs-SRCH_KO0,8.htm?sortBy=date_desc")

    # time.sleep(1)
    # time.sleep(3)

    glassdoor_automation = GlassdoorJobSearchAutomation(driver)
    if glassdoor_automation.checkifCaptcha():
        driver = webdriver.Firefox(options=chrome_options)
        driver.get("https://www.glassdoor.com/Job/frontend-jobs-SRCH_KO0,8.htm?sortBy=date_desc")
        glassdoor_automations = GlassdoorJobSearchAutomation(driver)
        glassdoor_automations.search_job()
    else:
        glassdoor_automation.search_job()
