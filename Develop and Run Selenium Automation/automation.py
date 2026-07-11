from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
DASHBOARD_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"

results = []

def log_result(tc_id, username, password, expected_label, actual_label, extra_note=""):
    status = "PASS" if expected_label == actual_label else "FAIL"
    print("=" * 50)
    print(f"Test Case : {tc_id}")
    if username is not None:
        print(f"Username  : {username}")
    if password is not None:
        print(f"Password  : {password}")
    print(f"Expected  : {expected_label}")
    print(f"Actual    : {actual_label}")
    print(f"Status    : {status}")
    if status == "FAIL":
        print("Bug Found : Application behavior differs from expected result.")
    if extra_note:
        print(f"Note      : {extra_note}")
    print("=" * 50)
    results.append((tc_id, status))
    return status


def attempt_login(driver, wait, username, password):
    driver.get(BASE_URL)
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']")))
        return True
    except TimeoutException:
        return False


def logout(driver, wait):
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='oxd-userdropdown-tab']"))
    ).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']"))).click()



def run_login_test_cases(driver, wait):
    long_username = "a" * 41  

    login_cases = [
        ("TC_01", "Admin", "admin123", True),
        ("TC_02", "admin", "admin123", False),           # Bug: lowercase accepted
        ("TC_03", "Admin", "ADMIN123", False),
        ("TC_04", "admin", "admin12345", False),
        ("TC_05", "Admin", "admin12345", False),
        ("TC_06", "Admin12", "admin123", False),
        ("TC_07", "Admin12", "admin12345", False),
        ("TC_08", "", "admin123", False),
        ("TC_09", "Admin", "", False),
        ("TC_10", "Admin12", "", False),
        ("TC_11", "", "admin12345", False),
        ("TC_12", "", "", False),
        ("TC_16", long_username, "admin123", False),      # username exceeds max length
        ("TC_17", "' OR '1'='1", "anything123", False),   # SQL injection attempt
        ("TC_18", "<script>alert('XSS')</script>", "admin123", False),  # script injection
        ("TC_25", " Admin ", "admin123", True),            # leading/trailing spaces trimmed
        ("TC_26", "Admin", "@dm!n#123$", False),           # special characters in password
        ("TC_32", "Admin99", "wrongpass", False),
    ]

    for tc_id, username, password, expected in login_cases:
        actual = attempt_login(driver, wait, username, password)

        expected_label = "Login Successful" if expected else "Invalid Credentials"
        actual_label = "Login Successful" if actual else "Invalid Credentials"
        log_result(tc_id, username, password, expected_label, actual_label)

        if actual:
            logout(driver, wait)


def run_forgot_password_tests(driver, wait):
    # TC_13: Navigates to Reset Password page
    driver.get(BASE_URL)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Forgot your password?"))).click()
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Reset Password']")))
        actual = "Reset Password page displayed"
    except TimeoutException:
        actual = "Reset Password page NOT displayed"
    log_result("TC_13", None, None, "Reset Password page displayed", actual)

    # TC_14: Valid registered username shows confirmation message
    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'sent')]")))
        actual = "Confirmation message displayed"
    except TimeoutException:
        actual = "Confirmation message NOT displayed"
    log_result("TC_14", "Admin", None, "Confirmation message displayed", actual)

    # TC_15: Invalid/unregistered username - should show the same generic message
    driver.get(BASE_URL)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Forgot your password?"))).click()
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("InvalidUser999")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'sent')]")))
        actual = "Generic confirmation message displayed"
    except TimeoutException:
        actual = "Generic confirmation message NOT displayed"
    log_result("TC_15", "InvalidUser999", None, "Generic confirmation message displayed", actual)

def run_logout_test(driver, wait):
    attempt_login(driver, wait, "Admin", "admin123")
    logout(driver, wait)
    try:
        wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        actual = "Redirected to Login page"
    except TimeoutException:
        actual = "NOT redirected to Login page"
    log_result("TC_22", None, None, "Redirected to Login page", actual)


def run_back_button_after_logout_test(driver, wait):
    attempt_login(driver, wait, "Admin", "admin123")
    logout(driver, wait)
    driver.back()
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']")), )
        actual = "Cached Dashboard page displayed (bug)"
    except TimeoutException:
        actual = "Login page displayed, no cached page"
    log_result("TC_23", None, None, "Login page displayed, no cached page", actual)


def run_security_tests(driver, wait):
    # TC_24: multiple consecutive failed login attempts -> expect lockout/CAPTCHA
    for _ in range(5):
        attempt_login(driver, wait, "Admin", "wrongpass")
    driver.get(BASE_URL)
    page_source = driver.page_source.lower()
    locked_out = "captcha" in page_source or "locked" in page_source
    actual = "Account locked / CAPTCHA shown" if locked_out else "No lockout or CAPTCHA triggered"
    log_result("TC_24", None, None, "Account locked / CAPTCHA shown", actual)

    # TC_29: autocomplete should be disabled on password field
    password_field = driver.find_element(By.NAME, "password")
    autocomplete_attr = password_field.get_attribute("autocomplete")
    actual = "autocomplete disabled" if autocomplete_attr == "off" else f"autocomplete='{autocomplete_attr}'"
    log_result("TC_29", None, None, "autocomplete disabled", actual)

    # TC_31: unauthenticated access to Dashboard URL should redirect to Login
    driver.delete_all_cookies()
    driver.get(DASHBOARD_URL)
    try:
        wait.until(EC.visibility_of_element_located((By.NAME, "username")))
        actual = "Redirected to Login page"
    except TimeoutException:
        actual = "Dashboard accessible without login (bug)"
    log_result("TC_31", None, None, "Redirected to Login page", actual)

def run_ui_tests(driver, wait):
    driver.get(BASE_URL)

    # TC_19: password field masks characters
    pwd_field = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    pwd_field.send_keys("admin123")
    field_type = pwd_field.get_attribute("type")
    actual = "Masked (type=password)" if field_type == "password" else f"NOT masked (type={field_type})"
    log_result("TC_19", None, None, "Masked (type=password)", actual)

    # TC_20: core UI elements present
    required_elements = {
        "logo": (By.CSS_SELECTOR, ".oxd-brand-banner img"),
        "username field": (By.NAME, "username"),
        "password field": (By.NAME, "password"),
        "login button": (By.XPATH, "//button[@type='submit']"),
        "forgot password link": (By.LINK_TEXT, "Forgot your password?"),
    }
    missing = []
    for label, locator in required_elements.items():
        try:
            driver.find_element(*locator)
        except NoSuchElementException:
            missing.append(label)
    actual = "All UI elements present" if not missing else f"Missing: {', '.join(missing)}"
    log_result("TC_20", None, None, "All UI elements present", actual)

    # TC_27: responsive layout across viewport sizes
    viewports = {"mobile": (375, 812), "tablet": (768, 1024), "desktop": (1440, 900)}
    broken = []
    for label, (w, h) in viewports.items():
        driver.set_window_size(w, h)
        try:
            driver.find_element(By.NAME, "username")
            driver.find_element(By.XPATH, "//button[@type='submit']")
        except NoSuchElementException:
            broken.append(label)
    driver.maximize_window()
    actual = "Responsive on all viewports" if not broken else f"Broken on: {', '.join(broken)}"
    log_result("TC_27", None, None, "Responsive on all viewports", actual)

    # TC_28: tab order Username -> Password -> Login button
    username_field = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    username_field.click()
    username_field.send_keys(Keys.TAB)
    focused_1 = driver.switch_to.active_element.get_attribute("name")
    driver.switch_to.active_element.send_keys(Keys.TAB)
    focused_2 = driver.switch_to.active_element.get_attribute("type")
    tab_order_ok = focused_1 == "password" and focused_2 == "submit"
    actual = "Logical tab order" if tab_order_ok else f"Unexpected order: {focused_1} -> {focused_2}"
    log_result("TC_28", None, None, "Logical tab order", actual)


def print_summary():
    print("\n" + "#" * 50)
    print("TEST SUMMARY")
    print("#" * 50)
    passed = sum(1 for _, status in results if status == "PASS")
    failed = sum(1 for _, status in results if status == "FAIL")
    for tc_id, status in results:
        print(f"{tc_id:8s}: {status}")
    print("-" * 50)
    print(f"Total: {len(results)}  |  Passed: {passed}  |  Failed: {failed}")
    print("#" * 50)


if __name__ == "__main__":
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    run_login_test_cases(driver, wait)
    run_forgot_password_tests(driver, wait)
    run_logout_test(driver, wait)
    run_back_button_after_logout_test(driver, wait)
    run_security_tests(driver, wait)
    run_ui_tests(driver, wait)

    # NOTE: TC_21 (session timeout after inactivity) and TC_30 (concurrent
    # sessions across two browsers) are not included here — TC_21 requires
    # waiting out the real session-timeout window (impractical for a fast
    # test run) and TC_30 requires two independent authenticated driver
    # instances running in parallel. Both are better suited to a manual
    # check or a dedicated long-running/parallel test job.

    print_summary()

    driver.quit()