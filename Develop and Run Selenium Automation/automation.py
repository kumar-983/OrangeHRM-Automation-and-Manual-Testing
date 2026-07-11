from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Test Data
test_cases = [
    ("TC_01", "Admin", "admin123", True),
    ("TC_02", "admin", "admin123", False),   # Bug Expected
    ("TC_03", "Admin", "ADMIN123", False),
    ("TC_04", "admin", "admin12345", False),
    ("TC_05", "Admin", "admin12345", False),
    ("TC_06", "Admin12", "admin123", False),
    ("TC_07", "Admin12", "admin12345", False),
    ("TC_08", "", "admin123", False),
    ("TC_09", "Admin", "", False),
    ("TC_10", "Admin12", "", False),
    ("TC_11", "", "admin12345", False),
    ("TC_12", "", "", False)
]

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.maximize_window()

wait = WebDriverWait(driver, 10)

for tc_id, username, password, expected in test_cases:

    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    wait.until(
        EC.visibility_of_element_located((By.NAME, "username"))
    ).send_keys(username)

    driver.find_element(By.NAME, "password").send_keys(password)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    try:
        wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']"))
        )
        actual = True

    except TimeoutException:
        actual = False

    print("=" * 50)
    print(f"Test Case : {tc_id}")
    print(f"Username  : {username}")
    print(f"Password  : {password}")

    print(f"Expected  : {'Login Successful' if expected else 'Invalid Credentials'}")
    print(f"Actual    : {'Login Successful' if actual else 'Invalid Credentials'}")

    if actual == expected:
        print("Status    : PASS")
    else:
        print("Status    : FAIL")
        print("Bug Found : Application behavior differs from expected result.")

    print("=" * 50)

    # Logout only if login succeeded
    if actual:
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='oxd-userdropdown-tab']"))
        ).click()

        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']"))
        ).click()

driver.quit()