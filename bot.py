from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time 

chrome_options = Options()

connect_carolina_link = "https://pa.cc.unc.edu/psp/paprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_MY_ACAD.GBL?Action=U&ACAD_CAREER=UGRD&EMPLID=730817479&ENRL_REQUEST_ID=&INSTITUTION=UNCCH&STRM=2249"

swap_link = "https://cs.cc.unc.edu/psc/campus/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_SWAP.GBL?Page=SSR_SSENRL_SWAP&Action=A&ACAD_CAREER=UGRD&EMPLID=730817479&ENRL_REQUEST_ID=&INSTITUTION=UNCCH&STRM=2249&SRCHPROMPT=N"

# Import By.ID to use the id locator
from selenium.webdriver.common.by import By

# user_data_dir = "C:/Users/Bryan Sukidi/AppData/Local/Google/Chrome/User Data"
# profile_dir = "Profile 3"
# chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
# # chrome_options.add_argument(f"--profile-directory={profile_dir}")
# chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

# Opens driver. Goes to swap.
def login():
  driver.get(connect_carolina_link)


def request_swap(current_class_value, desired_class_value):

  current_schedule_dropdown_id = "DERIVED_REGFRM1_DESCR50$225$"


  shopping_cart_dropdown_id = "DERIVED_REGFRM1_SSR_CLASSNAME_35$183$"


  # first, access current schedule drop down using the id. Then, select the option with a value of current_class_value.

  current_schedule_dropdown = Select(driver.find_element(By.ID, current_schedule_dropdown_id))
  current_schedule_dropdown.select_by_value(current_class_value)

  shopping_cart_dropdown = Select(driver.find_element(By.ID, shopping_cart_dropdown_id))
  shopping_cart_dropdown.select_by_value(desired_class_value)


  confirm_swap_button_id = "DERIVED_REGFRM1_SSR_PB_ADDTOLIST1$184$"
  confirm_swap_button = driver.find_element(By.ID, confirm_swap_button_id)
  confirm_swap_button.click()

  # wait for page to load
  time.sleep(1)

  finish_button_id = "DERIVED_REGFRM1_SSR_PB_SUBMIT"
  finish_button = driver.find_element(By.ID, finish_button_id)
  finish_button.click()

  time.sleep(1)

def check_swap_status(idx):
  error_text = "If a wait list is available, select Add Another Class to return to step 1. Select the class link, select the wait list option and resubmit your request."

  if error_text in driver.page_source:
    print(f"Error: Swap {idx} was not successful.")
    return False
  else:
    print(f"Success: Swap {idx} was successful.")
    return True



def main():
  login()
  input("Press enter to continue")

  class_ids = ["10031", "14592", "17201"]
  idx = 0

  while True:

    driver.get(swap_link)
    time.sleep(0.3)
    request_swap("14766",class_ids[idx % 3])
    time.sleep(0.3)
    result = check_swap_status(idx)

    if result:
      break

    idx += 1

    time.sleep(0.5)

if __name__ == "__main__":
  main()

driver.quit()


