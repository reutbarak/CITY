from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


PATH_data = "C:/Users/USER/Desktop/gil/PhD/year_break_3/Needle_in_data/Final_project/Data/"


# create numeric value for goal/percentage values
def create_numeric_value(str_value):
    if "$" in str_value:
        str_value = str_value.split("$")[1]
    num_split_list = str_value.split("%")[0].split(",")
    num_value = ""
    for num in num_split_list:
        num_value =  num_value + num
    return int(num_value)


# Assuming chrome browser
# download chromedriver.exe from https://chromedriver.chromium.org/downloads
# set PATH_chromedriver to its location
PATH_chromedriver = "C:/Users/USER/Desktop/gil/PhD/year_break_3/Needle_in_data/ex1/Creepy_crawling/chromedriver.exe"
# crawled url: indiegogo HOME category
alljobs_url = "https://www.alljobs.co.il/"
# how many pages to read?
settlements = pd.read_csv(PATH_data+"CITY_merged_dataset_02.csv" ,encoding="utf-8-sig", usecols= ["settlement"])
settlements = settlements["settlement"]
# how many seconds to delay?
delay_seconds = 5


driver = Chrome(executable_path=PATH_chromedriver)


# make sure time.sleep works fine
localtime = time.localtime()
result = time.strftime("%I:%M:%S %p", localtime)
print(result, end="", flush=True)
print("\r", end="", flush=True)

driver = Chrome(executable_path=PATH_chromedriver)

driver.get("https://www.jobmaster.co.il/")

job_demands_per_settlement = list()
i = 1
for stlmt in settlements:
    try:
        driver.find_elements_by_xpath('//input[@class="FreeSearchTextBox"]')[1].send_keys(stlmt)
        # driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
        driver.find_element_by_xpath('//div[@class="submitFind"]').click()
        job_demands = driver.find_element_by_xpath('//span[@class="ResultsHeader"]').text
        job_demands = str.split(job_demands, " ")[1].replace(",", "")
        time.sleep(delay_seconds)
        driver.back()
    except Exception as inst:
        if "יי" in stlmt:
            driver.back()
            time.sleep(delay_seconds)
            driver.find_elements_by_xpath('//input[@class="FreeSearchTextBox"]')[1].send_keys(stlmt.replace("יי", "י"))
            # driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
            driver.find_element_by_xpath('//div[@class="submitFind"]').click()
            job_demands = driver.find_element_by_xpath('//span[@class="ResultsHeader"]').text
            job_demands = str.split(job_demands, " ")[1].replace(",", "")
            time.sleep(delay_seconds)
            driver.back()
        else:
            if "תל אביב" in stlmt:
                driver.back()
                time.sleep(delay_seconds)
                driver.find_elements_by_xpath('//input[@class="FreeSearchTextBox"]')[1].send_keys("תל אביב")
                # driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
                driver.find_element_by_xpath('//div[@class="submitFind"]').click()
                job_demands = driver.find_element_by_xpath('//span[@class="ResultsHeader"]').text
                job_demands = str.split(job_demands, " ")[1].replace(",", "")
                time.sleep(delay_seconds)
                driver.back()
            else:
                job_demands = 0
                print(inst)
                driver.back()
    print(str(i) + ". " + stlmt + " " + str(job_demands))
    i+=1
    job_demands_per_settlement.append(job_demands)
    time.sleep(delay_seconds)


job_demand_df = pd.DataFrame({"settlement":stlmt,"job_demands":job_demands_per_settlement})
job_demand_df.to_csv(PATH_data+"job_demands_jobmaster_co_il.csv" ,encoding="utf-8-sig")
print("done")