from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time
import json

# Load LinkedIn credentials from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

linkedin_username = config['linkedin_username']
linkedin_password = config['linkedin_password']
search_query = "HR DevOps Engineer hiring"
output_file = "hr_emails.csv"

# Initialize WebDriver
driver = webdriver.Chrome()  # Make sure chromedriver is in your PATH

# Login to LinkedIn
driver.get("https://www.linkedin.com/login")
time.sleep(2)

username_input = driver.find_element(By.ID, "username")
username_input.send_keys(linkedin_username)

password_input = driver.find_element(By.ID, "password")
password_input.send_keys(linkedin_password)
password_input.send_keys(Keys.RETURN)

# Wait for login to complete
time.sleep(5)  # Adjust the time if needed

# Search for HR hiring DevOps Engineer roles
search_box = driver.find_element(By.XPATH, "//input[@aria-label='Search']")
search_box.send_keys(search_query)
search_box.send_keys(Keys.RETURN)

# Wait for search results to load
time.sleep(5)

# Scroll down to load more profiles
for _ in range(3):  # Adjust the range for more scrolling
    ActionChains(driver).send_keys(Keys.END).perform()
    time.sleep(3)

# Extract HR profile links
profile_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/in/')]")
profile_urls = [link.get_attribute('href') for link in profile_links]

# Visit each profile and extract email (if available)
emails = []
for profile_url in profile_urls:
    driver.get(profile_url)
    time.sleep(5)
    contact_info = driver.find_elements(By.XPATH, "//a[contains(@href, 'mailto:')]")
    for contact in contact_info:
        emails.append(contact.get_attribute('href').replace('mailto:', ''))

# Write emails to a CSV file
def write_emails_to_csv(emails, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email'])
        for email in emails:
            writer.writerow([email])

# Save the extracted emails to a CSV file
write_emails_to_csv(emails, output_file)

# Close the WebDriver
driver.quit()
