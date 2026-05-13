cat <<EOF > kret.py
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# Database ng mga pangalan
first_names = ["Liam", "Noah", "Oliver", "Elijah", "Lucas", "Mia", "Sophia", "Isabella", "Amelia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

def generate_name():
    return random.choice(first_names), random.choice(last_names)

def create_facebook_account(email, password):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    try:
        # Eto yung FIX: Tinanggal na ang .exe at inayos ang chromium-browser path
        driver = uc.Chrome(
            options=options,
            browser_executable_path='/data/data/com.termux/files/usr/bin/chromium-browser',
            driver_executable_path='/data/data/com.termux/files/usr/bin/chromedriver'
        )
        
        driver.get("https://www.facebook.com/reg")
        wait = WebDriverWait(driver, 20)

        f_name, l_name = generate_name()

        wait.until(EC.presence_of_element_located((By.NAME, "firstname"))).send_keys(f_name)
        driver.find_element(By.NAME, "lastname").send_keys(l_name)
        driver.find_element(By.NAME, "reg_email__").send_keys(email)
        
        time.sleep(1)
        try:
            driver.find_element(By.NAME, "reg_email_confirmation__").send_keys(email)
        except:
            pass

        driver.find_element(By.NAME, "reg_passwd__").send_keys(password)
        driver.find_element(By.NAME, "birthday_day").send_keys(str(random.randint(1, 28)))
        driver.find_element(By.NAME, "birthday_month").send_keys(str(random.randint(1, 12)))
        driver.find_element(By.NAME, "birthday_year").send_keys(str(random.randint(1990, 2005)))

        gender = random.choice(["1", "2"])
        driver.find_element(By.XPATH, f"//input[@value='{gender}']").click()
        driver.find_element(By.NAME, "websubmit").click()

        print(f"✅ Success: {f_name} {l_name} | {email}")
        time.sleep(10)

    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    print("--- Facebook Account Creator (Termux Fix) ---")
    num_accounts = int(input("How many accounts? "))
    password = input("Password: ")

    emails = []
    for i in range(num_accounts):
        email = input(f"Enter email {i+1}: ")
        emails.append(email)

    for email in emails:
        create_facebook_account(email, password)
        time.sleep(5)
EOF
    
