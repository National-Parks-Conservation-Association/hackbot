import os
import json
import sys
import zipfile
import time
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --allow-pre-commit-input --disable-background-networking --disable-blink-features=AutomationControlled --disable-client-side-phishing-detection --disable-default-apps --disable-dev-shm-usage --disable-gpu --disable-hang-monitor --disable-popup-blocking --disable-prompt-on-repost --disable-sync --enable-logging --log-level=0 --no-first-run --no-sandbox --no-service-autorun --password-store=basic --remote-debugging-port=9222 --test-type=webdriver --use-mock-keychain --user-data-dir=/Users/dbouquin/Documents/ChromeProfileForSelenium --flag-switches-begin --flag-switches-end

# Function to get the latest file in a directory
def get_latest_file_in_directory(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    return files[-1] if files else None

# Function to unzip a file
def unzip_file(zip_filepath, dest_dir):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)

# Directories
def initialize_directories():
    """Loads the directory paths from the map.json file and initializes global variables."""
    global directory_map, roi_links_dir, landing_pad_dir, credentials_path
    try:
        with open('C:/Users/jhaybok/National Parks Conservation Association/Data Vault - General/hackbot_data_vault/map.json', 'r') as f:
            directory_map = json.load(f)
            landing_pad_dir = directory_map.get('landing_pad')
            roi_links_dir = directory_map.get('roi_links')
            credentials_path = directory_map.get('credentials')
    except Exception as e:
        raise RuntimeError(f"Failed to initialize directories from map.json: {e}")

# Web driver
def setup_driver():
    """Sets up and returns a configured Chrome webdriver."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
    return webdriver.Chrome(options=chrome_options)

# Initial login
def login_once(driver):
    """Perform the login operation once before processing the downloads."""
    try:
        with open(credentials_path, 'r') as f:
            credentials = json.load(f)

        driver.get("https://app.roicrm.net/live")  # Specify the initial login URL
        time.sleep(5)

        # If there is a username field, enter the username and click submit
        if driver.find_elements(By.ID, 'username'):
            driver.find_element(By.ID, 'username').send_keys(credentials['username'])
            driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(5)
        # If there is a password field, enter the password and click submit
        if driver.find_elements(By.NAME, 'passwd'):
            driver.find_element(By.NAME, 'passwd').send_keys(credentials['password'])
            driver.find_element(By.ID, 'idSIButton9').click()
        time.sleep(20)  # Wait for manual interactions if necessary

    except Exception as e:
        print(f"Login error occurred: {e}")

def main(driver, link_file_path):
    try:
        with open(link_file_path, 'r') as f:
            url = f.read().strip()
        url = url.replace("secure2.roisolutions.net/enterprise", "app.roicrm.net/live")
        # Navigate to the URL
        driver.get(url)
        # Wait until download completes 
        time.sleep(10)  # Arbitrary wait time for download start
        while any('.crdownload' in f for f in os.listdir(landing_pad_dir)):
            time.sleep(10)  # Check every 10 seconds
        # Handling downloaded files
        large_files = ['link_allaccountsandinfo.txt', 
                       'link_alltransactions.txt', 
                       'link_transactionswsolicitors.txt', 
                       'link_accountflagssincefy18.txt']
        #Get the name of the latest file in the download directory
        downloaded_file = get_latest_file_in_directory(landing_pad_dir)

        # If the downloaded file is a ZIP file, unzip it
        if downloaded_file and downloaded_file.lower().endswith('.zip'):
            unzip_file(
                os.path.join(landing_pad_dir, downloaded_file),
                landing_pad_dir
            )

            # Loop through all the files in the download directory
            for file in os.listdir(landing_pad_dir):
                # Initialize new_filename as None
                new_filename = None

                # check for dop_files
                dop_files = ['HTACTIVITIES', 'MGRATINGS', 'PLANNEDGIFTS', 'EVENTSANDATTENDEESSINCEFY19',
                             'PLEDGES', 'PLEDGE_SCHEDULE', 'PROPOSALS',
                             'ACCOUNTFLAGSSINCEFY18', 'RELATIONSHIPMANAGERASSIGNMENTS', 'TRANSACTIONSWSOLICITORS',
                             'ALLTRANSACTIONS', 'ALLACCOUNTSANDINFO', 'FIRSTGIFTSALL']

                if any(dop_file in file for dop_file in dop_files) and file.endswith('.csv'):
                    today_date = datetime.now().strftime("%Y%m%d")
                    new_filename = f"{today_date}_{file}"
                    # strip "NPCA_JOB" from filename
                    new_filename = new_filename.replace('NPCA_JOB', '')

                # If the file is a CSV file and starts with 'NPCA', rename it
                elif file.startswith('NPCA') and file.endswith('.csv'):
                    prefix, rest_of_filename = file.split('NPCA_JOB', 1)
                    new_filename = rest_of_filename

                # Check if file contains "QTool" and ends with .csv
                elif "QTool" in file and file.endswith('.csv'):
                    today_date = datetime.now().strftime("%Y%m%d")
                    new_filename = f"{today_date}_WEALTHSCREENING.csv"

                else:
                    continue

                # Rename the file
                os.rename(
                    os.path.join(landing_pad_dir, file),
                    os.path.join(landing_pad_dir, new_filename)
                )

                # Move the file to the correct directory based on its name
                for keyword, directory in directory_map.items():
                    if keyword in new_filename.upper():
                        shutil.move(
                            os.path.join(landing_pad_dir, new_filename),
                            os.path.join(directory, new_filename)
                        )
                        break

            # Remove the original ZIP file
            os.remove(
                os.path.join(
                    landing_pad_dir, downloaded_file
                )
            )

            # Remove all .txt files
            for file in os.listdir(landing_pad_dir):
                if file.endswith('.TXT'):
                    os.remove(os.path.join(landing_pad_dir, file))

        elif "FoundationsReport" in downloaded_file:
            today_date = datetime.now().strftime("%Y%m%d")
            new_filename = f"{today_date}_FOUNDATIONSREPORT.csv"
            
            # Rename the file
            os.rename(
                os.path.join(landing_pad_dir, downloaded_file),
                os.path.join(landing_pad_dir, new_filename)
            )

            # Move the file to the correct directory based on its name
            for keyword, directory in directory_map.items():
                if keyword in new_filename.upper():
                    shutil.move(
                        os.path.join(landing_pad_dir, new_filename),
                        os.path.join(directory, new_filename)
                    )
                    break
            # Make a copy of the file with a static name
            static_name = "FOUNDATIONSREPORT_CURRENT.csv"
            shutil.copy2(
                os.path.join(directory, new_filename),
                os.path.join(directory, static_name)
            )
        
    except Exception as e:
        print(f"An error occurred while processing {link_file_path}: {e}")
        sys.exit(1) # Exit the script after processing the file
def process_all_links(driver):
    """Processes all .txt files with URLs in the roi_links_dir using the provided driver."""
    link_files = [f for f in os.listdir(roi_links_dir) if f.endswith('.txt')]
    first_file = True
    for link_file in link_files:
        if first_file:
            login_once(driver)
            first_file = False
        main(driver, os.path.join(roi_links_dir, link_file))
        time.sleep(15)  # Wait for OneDrive to sync before processing the next file

if __name__ == "__main__":
    initialize_directories()
    driver = setup_driver()
    process_all_links(driver)
    sys.exit(0) # Exit the script after processing all files
    #driver.quit()
    #driver.close()