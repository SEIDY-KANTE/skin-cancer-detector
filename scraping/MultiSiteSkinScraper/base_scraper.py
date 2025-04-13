import os
import time
import urllib.parse
import urllib.request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from abc import ABC, abstractmethod

class BaseSkinCancerScraper(ABC):
    def __init__(self, save_dir):
        self.save_dir = save_dir
        self.driver = webdriver.Chrome()
        self.seen_urls = set()

    def create_directory(self, folder_path):
        os.makedirs(folder_path, exist_ok=True)

    def gradual_scroll(self, step=350, delay=1.5, max_pause=10):
        last_height = 0
        pause_counter = 0

        while True:
            self.driver.execute_script(f"window.scrollBy(0, {step});")
            time.sleep(delay)
            new_height = self.driver.execute_script("return window.scrollY")
            if new_height == last_height:
                pause_counter += 1
            else:
                pause_counter = 0

            if pause_counter >= max_pause:
                break

            last_height = new_height

    def load_page(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div[2]/button"))
            )
            cookie_button.click()
        except TimeoutException:
            pass
        self.gradual_scroll()

    @abstractmethod
    def extract_data(self, url):
        pass

    def sanitize_filename(self, name):
        return "".join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in name).strip()

    def download_images(self, data):
        for i, item in enumerate(data):
            folder_name = self.sanitize_filename(item["condition_type"])
            
            if not folder_name:
                folder_name = "Unknown"
            elif "non_cancer" or "non-cancer" in folder_name.lower():
                folder_name = "Non_Cancer"

            folder_path = os.path.join(self.save_dir, folder_name)
            self.create_directory(folder_path)

            filename = f"{self.sanitize_filename(item['title'])}_{i}.jpg"
            save_path = os.path.join(folder_path, filename)
            try:
                urllib.request.urlretrieve(item["image_url"], save_path)
                print(f"Downloaded: {save_path}")
            except Exception as e:
                print(f"Error downloading {item['image_url']}: {e}")

    def scrape_website(self, url):
        self.load_page(url)
        data = self.extract_data(url)
        self.download_images(data)

    def close_driver(self):
        self.driver.quit()