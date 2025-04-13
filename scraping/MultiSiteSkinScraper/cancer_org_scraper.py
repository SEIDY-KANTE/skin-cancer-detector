from MultiSiteSkinScraper.base_scraper import BaseSkinCancerScraper
from bs4 import BeautifulSoup
import urllib.parse

class CancerOrgSkinCancerScraper(BaseSkinCancerScraper):
    def __init__(self, save_dir):
        super().__init__(save_dir)

    def extract_data(self, url):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        cards = soup.find_all("li", class_="card")
        data = []
        for card in cards:
            title = card.find("h4", class_="title").text.strip()
            img_tag = card.find("img")
            img_url = img_tag.get("src") or img_tag.get("data-src")
            if img_url and not img_url.startswith("data:image") and img_url not in self.seen_urls:
                self.seen_urls.add(img_url)
                if not img_url.startswith("http"):
                    img_url = urllib.parse.urljoin(url, img_url)
                condition_tag = card.find("div", class_="condition-type")
                condition_type = "Unknown"
                if condition_tag:
                    condition_type = condition_tag.text.replace("Condition Type: ", "").strip()
                data.append({
                    "title": title,
                    "image_url": img_url,
                    "condition_type": condition_type
                })

        self.driver.quit() # Close the browser after scraping

        return data