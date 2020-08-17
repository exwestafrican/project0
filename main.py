from api import AbokiFxWebsiteData
from settings import frequency
import time



def main():
   aboki = AbokiFxWebsiteData("https://www.abokifx.com/home_bdc_rate", "AbokiFx")
   aboki.run_scraper("currency.json")

while True:
    #run aboki fx and coin geko here
    main()
    time.sleep(frequency)
