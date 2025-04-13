import os
from MultiSiteSkinScraper.aim_scraper import AIMSkinCancerScraper
from MultiSiteSkinScraper.cancer_org_scraper import CancerOrgSkinCancerScraper
from MultiSiteSkinScraper.rxlist_scraper import RXListSkinCancerScraper
from MultiSiteSkinScraper.skincancer_org_scraper import SkinCancerOrgScraper
from MultiSiteSkinScraper.freepik_scraper import FreepikScraper




def main():
    save_dir = "output"
    websites = [
        ("https://aimatskincancer.org/skin-cancer-images/", AIMSkinCancerScraper(os.path.join(save_dir, "AIM"))),
        ("https://www.cancer.org/cancer/types/skin-cancer/skin-cancer-image-gallery.html?filter=all", CancerOrgSkinCancerScraper(os.path.join(save_dir, "CancerOrg"))),
        ("https://www.rxlist.com/collection-of-images/skin_cancer_picture/pictures.htm", RXListSkinCancerScraper(os.path.join(save_dir, "RxList"))),
        ("https://www.skincancer.org/skin-cancer-information/skin-cancer-pictures/", SkinCancerOrgScraper(os.path.join(save_dir, "SkinCancerOrg"))),
        ("https://www.freepik.com/free-photos-vectors/skin", FreepikScraper(os.path.join(save_dir, "Freepik"))) 

    ]

    for url, scraper in websites:
        print(f"Scraping {url}")
        scraper.scrape_website(url)
        scraper.close_driver()

if __name__ == "__main__":
    main()
