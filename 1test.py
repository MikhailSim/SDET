import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegistrationPage:
    def __init__(self, browser):
        self.browser = browser
        self.url = "https://demoqa.com/automation-practice-form"
        self.first_name = (By.CSS_SELECTOR, "#firstName")
        self.last_name = (By.XPATH, "//input[@id='lastName']")
        self.email = (By.ID, "userEmail")
        self.gender_male = (By.XPATH, "//label[text()='Male']")
        self.mobile = (By.CSS_SELECTOR, "#userNumber")
        self.date_of_birth_input = (By.ID, "dateOfBirthInput")
        self.month_select = (By.CSS_SELECTOR, ".react-datepicker__month-select")
        self.year_select = (By.CSS_SELECTOR, ".react-datepicker__year-select")
        self.day_select = (By.XPATH, "//div[text()='24']")
        self.subjects_input = (By.CSS_SELECTOR, "#subjectsInput")
        self.upload_picture = (By.ID, "uploadPicture")
        self.current_address = (By.XPATH, "//textarea[@id='currentAddress']")
        self.state_input = (By.CSS_SELECTOR, "#react-select-3-input")
        self.city_input = (By.XPATH, "//input[@id='react-select-4-input']")
        self.submit_button = (By.ID, "submit")
        self.result_title = (By.ID, "example-modal-sizes-title-lg")
        self.result_student_name = (By.XPATH, "//td[text()='Student Name']/following-sibling::td")
        self.result_student_email = (By.XPATH, "//td[text()='Student Email']/following-sibling::td")
        self.result_gender = (By.XPATH, "//td[text()='Gender']/following-sibling::td")
        self.result_mobile = (By.XPATH, "//td[text()='Mobile']/following-sibling::td")
        self.result_date_of_birth = (By.XPATH, "//td[text()='Date of Birth']/following-sibling::td")
        self.result_subjects = (By.XPATH, "//td[text()='Subjects']/following-sibling::td")
        self.result_picture = (By.XPATH, "//td[text()='Picture']/following-sibling::td")
        self.result_address = (By.XPATH, "//td[text()='Address']/following-sibling::td")
        self.result_state_and_city = (By.XPATH, "//td[text()='State and City']/following-sibling::td")

    def open(self):
        self.browser.get(self.url)

    def fill_form(self, first_name, last_name, email, gender, mobile, birth_month, birth_year, birth_day, subject,
                  picture_path, address, state, city):
        self.browser.find_element(*self.first_name).send_keys(first_name)
        self.browser.find_element(*self.last_name).send_keys(last_name)
        self.browser.find_element(*self.email).send_keys(email)
        self.browser.find_element(*self.gender_male).click()
        self.browser.find_element(*self.mobile).send_keys(mobile)
        self.browser.find_element(*self.date_of_birth_input).click()
        Select(self.browser.find_element(*self.month_select)).select_by_value(birth_month)
        Select(self.browser.find_element(*self.year_select)).select_by_value(birth_year)
        self.browser.find_element(*self.day_select).click()
        subjects_input = self.browser.find_element(*self.subjects_input)
        subjects_input.send_keys(subject)
        subjects_input.send_keys("\n")
        self.browser.find_element(*self.upload_picture).send_keys(picture_path)
        self.browser.find_element(*self.current_address).send_keys(address)
        state_input = self.browser.find_element(*self.state_input)
        state_input.send_keys(state)
        state_input.send_keys("\n")
        city_input = self.browser.find_element(*self.city_input)
        city_input.send_keys(city)
        city_input.send_keys("\n")
        self.browser.find_element(*self.submit_button).click()

    def verify_result(self, first_name, last_name, email, gender, mobile, birth_date, subject, picture, address,
                      state_and_city):
        WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(self.result_title))
        assert self.browser.find_element(*self.result_title).text == "Thanks for submitting the form"
        assert self.browser.find_element(*self.result_student_name).text == f"{first_name} {last_name}"
        assert self.browser.find_element(*self.result_student_email).text == email
        assert self.browser.find_element(*self.result_gender).text == gender
        assert self.browser.find_element(*self.result_mobile).text == mobile
        assert self.browser.find_element(*self.result_date_of_birth).text == birth_date
        assert self.browser.find_element(*self.result_subjects).text == subject
        assert self.browser.find_element(*self.result_picture).text == picture
        assert self.browser.find_element(*self.result_address).text == address
        assert self.browser.find_element(*self.result_state_and_city).text == state_and_city


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.feature('Registration Form')
@allure.story('Submit registration form successfully')
def test_registration_form(browser):
    registration_page = RegistrationPage(browser)

    with allure.step("Open registration form page"):
        registration_page.open()

    with allure.step("Fill in the form"):
        registration_page.fill_form(
            first_name="Михаил",
            last_name="Антонов",
            email="name@example.com",
            gender="Male",
            mobile="1234567890",
            birth_month="1",  # Февраль
            birth_year="1991",
            birth_day="24",
            subject="Maths",
            picture_path="/Users/madbrains/Downloads/testauto.jpg",
            address="Скочилова 6",
            state="NCR",
            city="Delhi"
        )

    with allure.step("Verify the result"):
        registration_page.verify_result(
            first_name="Михаил",
            last_name="Антонов",
            email="name@example.com",
            gender="Male",
            mobile="1234567890",
            birth_date="24 February,1991",
            subject="Maths",
            picture="testauto.jpg",
            address="Скочилова 6",
            state_and_city="NCR Delhi"
        )
