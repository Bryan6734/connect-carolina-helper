from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time, datetime, json

chrome_options = Options()

connect_carolina_link = "https://pa.cc.unc.edu/psp/paprd/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_MY_ACAD.GBL?Action=U&ACAD_CAREER=UGRD&EMPLID=730817479&ENRL_REQUEST_ID=&INSTITUTION=UNCCH&STRM=2249"

swap_link = "https://cs.cc.unc.edu/psc/campus/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_SWAP.GBL?Page=SSR_SSENRL_SWAP&Action=A&ACAD_CAREER=UGRD&EMPLID=730817479&ENRL_REQUEST_ID=&INSTITUTION=UNCCH&STRM=2249&SRCHPROMPT=N"

driver = webdriver.Chrome(options=chrome_options)

# Opens driver. Goes to swap.
def login():
  driver.get(connect_carolina_link)

  # Wait for page to load
  time.sleep(3)

  # get json data from onyen_login.json (personal data, not shared/stored anywhere else)
  with open("onyen_login.json", "r") as f:
    data = json.load(f)

  # Find the username input field
  username = driver.find_element(By.ID, "username")
  # Send the username
  username.send_keys(data["username"])

  # Find the password input field
  next_button = driver.find_element(By.ID, "nextBtn")
  next_button.click()

  time.sleep(1)

  password = driver.find_element(By.ID, "password")
  password.send_keys(data["password"])

  submit_button = driver.find_element(By.ID, "submitBtn")
  submit_button.click()



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

  error_src = "/cs/campus/cache/c859/PS_CS_STATUS_ERROR_ICN_1.gif"
  success_src = "/cs/campus/cache/c859/PS_CS_STATUS_SUCCESS_ICN_1.gif"

  # if it can find two images with error_src, then it means that the swap was not successful.
  num_error_icons = len(driver.find_elements(By.XPATH, f"//img[contains(@src, '{error_src}')]"))

  num_success_icons = len(driver.find_elements(By.XPATH, f"//img[contains(@src, '{success_src}')]"))

  if num_error_icons == 2:
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Error: Swap {idx} was not successful.")
    return False
  
  elif num_success_icons == 2:
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Success: Swap {idx} was successful.")
    return True
  
  else:
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Indeterminate: Swap {idx} was not successful.")
    return False

def main():
  login()
  input("Press enter to continue")

  class_ids = ["10031", "14592", "17201"]
  idx = 0

  while True:
    try:

      driver.get(swap_link)
      time.sleep(0.5)
      request_swap("14766",class_ids[idx % 3])
      time.sleep(0.5)
      result = check_swap_status(idx)

      if result:
        print("Swap successful. Exiting.")
        time.sleep(5)
        break

      idx += 1

      time.sleep(10)
    except Exception as e:
      print(e)
      print("Error occurred. Retrying in 5 seconds.")
      time.sleep(5)

if __name__ == "__main__":
  main()

driver.quit()


