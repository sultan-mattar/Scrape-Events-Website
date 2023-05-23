import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# Initialize the WebDriver
username = 'ainsultan2000@hotmail.com'  # Type Your Email
password = '^1QlWkNI%*lkx$'  # Type Your Password
executable_path = 'msedgedriver.exe'
links = []
datas = []
driver = webdriver.Edge(executable_path)

# Navigate to the initial page
driver.get("https://www.reverbnation.com")
driver.maximize_window()
time.sleep(2)

# Login
driver.find_element(By.XPATH, '//*[@id="foundation_page_header"]/div[3]/div/nav/section/div[2]/ul/li[1]/a').click()
time.sleep(2)
driver.find_element(By.XPATH, '//*[@id="user_login"]').send_keys(username)
driver.find_element(By.XPATH, '//*[@id="user_password"]').send_keys(password)
driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Log In"]').click()
print('Login Successfully!')
time.sleep(10)

# Go to gig finder recommended page
driver.get("https://www.reverbnation.com/control_room/artist/8469637/gig_finder_recommended")
time.sleep(10)

# Change location to United States
driver.find_element(By.XPATH, '//*[@id="gig_finder_change_location"]').click()
time.sleep(5)
select_container = driver.find_element(By.XPATH, '//*[@id="searchfor_venue_country_chzn"]/a')
select_container.click()
time.sleep(5)
select_input = driver.find_element(By.XPATH, '//*[@id="searchfor_venue_country_chzn"]/div/div/input')
select_input.send_keys('United States')
time.sleep(2)
select_option = driver.find_element(By.XPATH, '//*[@id="searchfor_venue_country_chzn_o_232"]')
select_option.click()
time.sleep(2)

# Get gig recommendations
driver.find_element(By.CSS_SELECTOR, 'div.controls input[type="submit"][name="commit"][value="Get Recommendations"]').click()
time.sleep(10)

# Define a function to extract links from div elements
def extract_links_from_div(div_element):
    link_elements = div_element.find_elements(By.TAG_NAME, "a")
    return [link.get_attribute("href") for link in link_elements if link.get_attribute("href")]

# Define a function to process a page and extract links from div elements
def process_page():
    div_elements = driver.find_elements(By.XPATH, "//div[contains(@id, 'venue_row_')]")
    for div_element in div_elements:
        links.extend(extract_links_from_div(div_element))

# Define the main function for pagination
def paginate():
    for i in range(1, 50):
        process_page()
        next_button = driver.find_element(By.XPATH, '//*[@id="next_page_btn"]')
        driver.execute_script("arguments[0].scrollIntoView();", next_button)

        if 'disabled' in next_button.get_attribute("class"):
            break
        next_button.click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.staleness_of(next_button))

    # Filter the links
    filtered_links = [link for link in links if link.startswith('https://www.reverbnation.com/venue/')]

    for link in filtered_links:
        driver.get(link)
        time.sleep(10)
        try:
            Name_of_venue = driver.find_element(By.XPATH, '//*[@id="page_contents"]/div[1]/div[1]/h1')
            Name_of_venue_ = Name_of_venue.text
        except NoSuchElementException:
            Name_of_venue_ = " No Name Found "

        try:
            streetAddress = driver.find_element(By.XPATH, '//*[@id="page_contents"]/div[1]/div[4]/div/div/p[1]/span[1]')
            streetAddress_ = streetAddress.text
        except NoSuchElementException:
            streetAddress_ = " NO Street Addres "


        try:
            addressLocality = driver.find_element(By.XPATH, '//*[@id="page_contents"]/div[1]/div[4]/div/div/p[1]/span[2]')
            addressLocality_ = addressLocality.text
        except NoSuchElementException:
            addressLocality_ = " NO Location Address "

        try:
            addressRegion = driver.find_element(By.XPATH, '//*[@id="page_contents"]/div[1]/div[4]/div/div/p[1]/span[3]')
            addressRegion_ = addressRegion.text
        except NoSuchElementException:
            addressRegion_ = " No Region "

        try:
            addressCountry = driver.find_element(By.XPATH, '//*[@id="page_contents"]/div[1]/div[4]/div/div/p[1]/span[4]')
            Country = addressCountry.text
        except NoSuchElementException:
            Country = " US "
        
        try:
            Phone_number = driver.find_element(By.XPATH, '//*[@id="page_contents"]/div[1]/div[4]/div/div/p[2]')
            Phone_number_ = Phone_number.text
        except NoSuchElementException:
            Phone_number_ = "No Phone Number"

        try:
            Capacity = driver.find_element(By.XPATH, '//*[@id="page_contents"]/div[1]/div[4]/div/div/p[3]/span[1]')
            Capacity_ = Capacity.text
        except NoSuchElementException:
            Capacity_ = "No Capacity "
        try:
            Age_Limit = driver.find_element(By.XPATH, '//*[@id="page_contents"]/div[1]/div[4]/div/div/p[3]/span[2]')
            Age_Limit_ = Age_Limit.text
        except NoSuchElementException:
            Age_Limit_ = "No Age Limit "
        try:
            Bio = driver.find_element(By.XPATH, '//*[@id="page_contents"]/div[1]/div[4]/div/div/p[4]/span/span')
            bio = Bio.text
        except NoSuchElementException:
            bio = "No bio available"

        temporary_data = {
            'Name_of_venue': Name_of_venue_,
            'street': streetAddress_,
            'Locality': addressLocality_,
            'Region': addressRegion_,
            'Country': Country,
            'Phone_number': Phone_number_,
            'Capacity': Capacity_,
            'Age_Limit': Age_Limit_,
            'Bio': bio,
        }
        datas.append(temporary_data)

# Start pagination
paginate()

# Save data to CSV file
keys = datas[0].keys()
csv_file = 'dataset.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=keys)
    writer.writeheader()
    writer.writerows(datas)

print("The file is ready.")
driver.quit()
