from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import zipfile
import os
import time

def get_latest_file_in_directory(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
    return files[-1] if files else None

def unzip_file(zip_filepath, dest_dir):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)

def main():
    try:
        with open('link.txt', 'r') as f:
            url = f.read().strip()

        with open('credentials.json', 'r') as f:
            credentials = json.load(f)

        with open('job.txt', 'r') as f:
            job_number = f.read().strip()

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        prefs = {"download.default_directory": "/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files"}
        chrome_options.add_experimental_option("prefs", prefs)

        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

        driver.get(url)

        driver.find_element(By.ID, 'loginuserid').send_keys(credentials['username'])
        driver.find_element(By.ID, 'loginpassword').send_keys(credentials['password'])
        driver.find_element(By.ID, 'loginclient').send_keys(credentials['client_code'])

        driver.find_element(By.CSS_SELECTOR, '#frmlogin2 button[type="submit"].btn.btn-default').click()

        time.sleep(5)

        downloaded_file = get_latest_file_in_directory('/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files')

        if downloaded_file and downloaded_file.endswith('.ZIP') and job_number in downloaded_file:
            unzip_file(os.path.join('/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files', downloaded_file), '/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files')

            for file in os.listdir('/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files'):
                if file.endswith('.csv'):
                    os.rename(os.path.join('/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files', file), os.path.join('/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files', f'{job_number}.csv'))

            os.remove(os.path.join('/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files', downloaded_file))

            # Remove all .txt files
            for file in os.listdir('/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files'):
                if file.endswith('.TXT'):
                    os.remove(os.path.join('/Users/dbouquin/OneDrive/Documents_Daina/hackbot/rescued_roi_files', file))

        driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")

main()

#%%
