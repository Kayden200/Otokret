import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# Foreign names database
first_names = ["Liam", "Noah", "Oliver", "Elijah", "Lucas", "Mia", "Sophia", "Isabella", "Amelia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

def generate_name():
    return random.choice(first_names), random.choice(last_names)

def create_facebook_account(email, password):
    options = uc.ChromeOptions()
    # Mga kailangang flags para sa Termux/Linux environment
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    try:
        # Dito natin ifo-force ang path ng Chromium at Driver sa Termux
        driver = uc.Chrome(
            options=options,
            browser_executable_path='/data/data/com.termux/files/usr/bin/chromium',
            driver_executable_path='/data/data/com.termux/files/usr/bin/chromedriver'
        )
        
        driver.get("https://www.facebook.com/reg")
        wait = WebDriverWait(driver, 15)

        first_name, last_name = generate_name()

        # Fill the sign-up form gamit ang mas matatag na selectors
        wait.until(EC.presence_of_element_located((By.NAME, "firstname"))).send_keys(first_name)
        driver.find_element(By.NAME, "lastname").send_keys(last_name)
        driver.find_element(By.NAME, "reg_email__").send_keys(email)
        
        # Minsan humihingi ng confirmation email ang FB
        time.sleep(1)
        try:
            driver.find_element(By.NAME, "reg_email_confirmation__").send_keys(email)
        except:
            pass

        driver.find_element(By.NAME, "reg_passwd__").send_keys(password)

        # Select birthdate
        driver.find_element(By.NAME, "birthday_day").send_keys(str(random.randint(1, 28)))
        driver.find_element(By.NAME, "birthday_month").send_keys(str(random.randint(1, 12)))
        driver.find_element(By.NAME, "birthday_year").send_keys(str(random.randint(1990, 2005)))

        # Select gender
        gender_choice = random.choice(["1", "2"])
        driver.find_element(By.XPATH, f"//input[@value='{gender_choice}']").click()

        # Submit
        driver.find_element(By.NAME, "websubmit").click()

        print(f"✅ Submitted: {first_name} {last_name} | {email}")
        time.sleep(10) # Bigyan ng oras ang FB para mag-process

    except Exception as e:
        print(f"❌ Error creating account with {email}: {e}")
    
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    # Siguraduhin na naka-install ang chromium at chromedriver sa Termux:
    # pkg install chromium chromedriver
    
    num_accounts = int(input("How many accounts to create? "))
    password = input("Enter the password for all accounts: ")

    emails = []
    for i in range(num_accounts):
        email = input(f"Enter email {i+1}/{num_accounts}: ")
        emails.append(email)

    print("\n📌 Starting account creation sa Termux...\n")

    for email in emails:
        create_facebook_account(email, password)
        # Delay para iwas instant ban
        time.sleep(5)
