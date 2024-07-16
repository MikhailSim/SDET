import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()  # Развернуть браузер в полное окно
    yield driver
    driver.quit()

@allure.feature('Registration Form')
@allure.story('Submit registration form successfully')
def test_registration_form(browser):
    with allure.step("Open registration form page"):
        browser.get("https://demoqa.com/automation-practice-form")

    with allure.step("Fill in the form"):
        browser.find_element(By.CSS_SELECTOR, "#firstName").send_keys("Михаил")
        browser.find_element(By.XPATH, "//input[@id='lastName']").send_keys("Антонов")
        browser.find_element(By.ID, "userEmail").send_keys("name@example.com")
        browser.find_element(By.XPATH, "//label[text()='Male']").click()
        browser.find_element(By.CSS_SELECTOR, "#userNumber").send_keys("1234567890")

        browser.find_element(By.ID, "dateOfBirthInput").click()
        Select(browser.find_element(By.CSS_SELECTOR, ".react-datepicker__month-select")).select_by_value("1")  # Февраль
        Select(browser.find_element(By.CSS_SELECTOR, ".react-datepicker__year-select")).select_by_value("1991")
        browser.find_element(By.XPATH, "//div[text()='24']").click()

        subjects_input = browser.find_element(By.CSS_SELECTOR, "#subjectsInput")
        subjects_input.send_keys("Maths")
        subjects_input.send_keys("\n")

        browser.find_element(By.ID, "uploadPicture").send_keys("/Users/madbrains/Downloads/testauto.jpg")
        browser.find_element(By.XPATH, "//textarea[@id='currentAddress']").send_keys("Скочилова 6")

        state = browser.find_element(By.CSS_SELECTOR, "#react-select-3-input")
        state.send_keys("NCR")
        state.send_keys("\n")
        city = browser.find_element(By.XPATH, "//input[@id='react-select-4-input']")
        city.send_keys("Delhi")
        city.send_keys("\n")

        browser.find_element(By.ID, "submit").click()

    with allure.step("Verify the result"):
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
        assert browser.find_element(By.ID, "example-modal-sizes-title-lg").text == "Thanks for submitting the form"

        assert browser.find_element(By.XPATH, "//td[text()='Student Name']/following-sibling::td").text == "Михаил Антонов"
        assert browser.find_element(By.XPATH, "//td[text()='Student Email']/following-sibling::td").text == "name@example.com"
        assert browser.find_element(By.XPATH, "//td[text()='Gender']/following-sibling::td").text == "Male"
        assert browser.find_element(By.XPATH, "//td[text()='Mobile']/following-sibling::td").text == "1234567890"
        assert browser.find_element(By.XPATH, "//td[text()='Date of Birth']/following-sibling::td").text == "24 February,1991"
        assert browser.find_element(By.XPATH, "//td[text()='Subjects']/following-sibling::td").text == "Maths"
        assert browser.find_element(By.XPATH, "//td[text()='Picture']/following-sibling::td").text == "testauto.jpg"
        assert browser.find_element(By.XPATH, "//td[text()='Address']/following-sibling::td").text == "Скочилова 6"
        assert browser.find_element(By.XPATH, "//td[text()='State and City']/following-sibling::td").text == "NCR Delhi"