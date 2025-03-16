import undetected_chromedriver as uc
import random
import time

# Foreign names database
first_names = ["Liam", "Noah", "Oliver", "Elijah", "Lucas", "Mia", "Sophia", "Isabella", "Amelia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

def generate_name():
    return random.choice(first_names) + " " + random.choice(last_names)

def create_facebook_account(email, password):
    driver = uc.Chrome()
    driver.get("https://www.facebook.com/")

    try:
        full_name = generate_name()
        first_name, last_name = full_name.split()

        # Fill the sign-up form
        driver.find_element("name", "firstname").send_keys(first_name)
        driver.find_element("name", "lastname").send_keys(last_name)
        driver.find_element("name", "reg_email__").send_keys(email)
        driver.find_element("name", "reg_passwd__").send_keys(password)

        # Select random birthdate
        driver.find_element("name", "birthday_day").send_keys(str(random.randint(1, 28)))
        driver.find_element("name", "birthday_month").send_keys(str(random.randint(1, 12)))
        driver.find_element("name", "birthday_year").send_keys(str(random.randint(1985, 2002)))

        # Select random gender
        gender_choice = random.choice(["1", "2"])  # 1: Female, 2: Male
        driver.find_element("xpath", f"//input[@value='{gender_choice}']").click()

        # Submit the form
        driver.find_element("name", "websubmit").click()

        time.sleep(5)  # Wait for account creation

        print(f"✅ Created: {full_name} | {email}")

    except Exception as e:
        print(f"❌ Error creating account with {email}: {e}")

    driver.quit()

if __name__ == "__main__":
    num_accounts = int(input("How many accounts to create? "))
    password = input("Enter the password for all accounts: ")

    emails = []
    for i in range(num_accounts):
        email = input(f"Enter email {i+1}/{num_accounts}: ")
        emails.append(email)

    print("\n📌 Starting account creation...\n")

    for email in emails:
        create_facebook_account(email, password)
