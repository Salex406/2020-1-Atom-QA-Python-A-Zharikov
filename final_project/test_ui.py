import pytest
from db.orm_model import User
from selenium.webdriver.common.action_chains import ActionChains
from base import BaseCase
from fixtures import *
import time
import requests
import allure


class TestLoginPage(BaseCase):

    @pytest.mark.UI
    def test_login_negative(self, login_page):
        """
        CHECK NEGATIVE LOGIN

        Step 1:
        Try login as unregistered user

        EXPECT:
        "Invalid username or password" in page_source,
        """
        login_page.send(login_page.locators.FORM_LOGIN, "TEST12345")
        login_page.send(login_page.locators.FORM_PASSWORD, "TEST1234")
        login_page.click(login_page.locators.BUTTON_LOGIN)
        assert "Invalid username or password" in login_page.driver.page_source

    @pytest.mark.UI
    def test_validation(self, login_page):
        """
        CHECK LOGIN FORM VALIDATION

        Step 1:
        Check "required" attribute

        EXPECT:
        "required" attribute is exists
        """
        assert login_page.check_required(login_page.locators.FORM_LOGIN) == "true"
        assert login_page.check_required(login_page.locators.FORM_PASSWORD) == "true"
  

    @pytest.mark.UI
    def test_login_positive(self, login_page):
        """
        CHECK LOGIN POSITIVE

        Step 1:
        Add user to db
        Step 2:
        Try to login as user

        EXPECT: 
        Login success. Redirect to main page
        """
        self.builder.add_user(login_page.get_user())
        time.sleep(0.1)
        login_page.send(login_page.locators.FORM_LOGIN, login_page.get_user().username)
        login_page.send(login_page.locators.FORM_PASSWORD, login_page.get_user().password)
        login_page.click(login_page.locators.BUTTON_LOGIN)
        self.builder.del_user(login_page.get_user())
        assert  "TM version 0.1" in login_page.driver.page_source
        assert login_page.get_user().username in login_page.driver.page_source 

    @pytest.mark.UI
    def test_login_access(self, login_page):
        """
        CHECK ACCESS

        Step 1:
        Add user to db
        Step 2:
        Update access to 0
        Step 3:
        Try to login

        EXPECT: 
        "Ваша учетная запись заблокирована" in page_source
        """       
        self.builder.add_user(login_page.get_user())
        self.builder.upd_access(login_page.get_user(), 0)
        login_page.send(login_page.locators.FORM_LOGIN, login_page.get_user().username)
        login_page.send(login_page.locators.FORM_PASSWORD, login_page.get_user().password)
        login_page.click(login_page.locators.BUTTON_LOGIN)
        self.builder.del_user(login_page.get_user())
        assert "Ваша учетная запись заблокирована" in login_page.driver.page_source

    @pytest.mark.UI  
    @pytest.mark.parametrize("ID", ["0", "99999999999999999999999"])
    def test_vk(self, ID, login_page):
        """
        CHECK VK ID

        Step 1:
        Add user to db
        Step 2:
        Login as user
        Step 3:
        Check if vk_id is on the page

        EXPECT: 
        vk_id in page source_code
        """
        user = login_page.get_user()
        data = {"username": user.username,
                "id": ID}
        requests.post('http://192.168.0.254:5000/add_user', data)
        self.builder.add_user(user) 
        login_page.send(login_page.locators.FORM_LOGIN, user.username)
        login_page.send(login_page.locators.FORM_PASSWORD, user.username)
        login_page.click(login_page.locators.BUTTON_LOGIN)
        self.builder.del_user(user)
        assert ID in login_page.driver.page_source

    @pytest.mark.UI
    def test_login_active(self, login_page):
        """
        CHECK 'ACTIVE' FLAG IN DB

        Step 1:
        Add user to db
        Step 2:
        Login as this user
        Step 3:
        Check that 'active' is 1 

        EXPECT: 
        'active' flag is 1
        """       
        self.builder.add_user(login_page.get_user())
        login_page.send(login_page.locators.FORM_LOGIN, login_page.get_user().username)
        login_page.send(login_page.locators.FORM_PASSWORD, login_page.get_user().password)
        login_page.click(login_page.locators.BUTTON_LOGIN)
        active = self.builder.get_active(login_page.get_user())
        self.builder.delete_user(login_page.get_user())
        assert active is not None

    @pytest.mark.UI
    def test_login_active_time(self, login_page):
        """
        CHECK 'ACTIVE TIME' FIELD IN DB

        Step 1:
        Add user to db
        Step 2:
        Login as this user
        Step 3:
        Check that 'active time' changed

        EXPECT: 
        'active time' is not null
        """       
        self.builder.add_user(login_page.get_user())
        login_page.send(login_page.locators.FORM_LOGIN, login_page.get_user().username)
        login_page.send(login_page.locators.FORM_PASSWORD, login_page.get_user().password)
        login_page.click(login_page.locators.BUTTON_LOGIN)
        datetime = self.builder.get_datetime(login_page.get_user())
        self.builder.delete_user(login_page.get_user())
        assert datetime is not None

class TestRegisterPage(BaseCase):

    @pytest.mark.UI
    def test_reg_validation(self, register_page):
        """
        CHECK REGISTER FORM VALIDATION

        Step 1:
        Check username, password, confirm forms 'required' attribute

        EXPECT: 
        'required' attribute exists
        """
        assert register_page.check_required(register_page.locators.FORM_USERNAME) == "true"
        assert register_page.check_required(register_page.locators.FORM_PASSWORD) == "true"
        assert register_page.check_required(register_page.locators.FORM_CONFIRM) == "true"

    @pytest.mark.UI
    @pytest.mark.parametrize("err", ["pwd", "email", "name"])
    def test_reg_form_validation_1_error(self, err, register_page):
        """
        CHECK REGISTER FORM VALIDATION ERRORS

        Step 1:
        Type in data into forms (with one error)

        Step 2:
        Click register

        Step 3:
        Check that user is not created and error message is displayed

        EXPECT: 
        User is not created, error message displayed correctly
        """
        if err == 'pwd':     
            NAME = register_page.generate_data()
            register_page.send(register_page.locators.FORM_USERNAME, NAME)
            register_page.send(register_page.locators.FORM_PASSWORD, NAME)
            register_page.send(register_page.locators.FORM_CPASSWORD, NAME + "Q")
            register_page.send(register_page.locators.FORM_EMAIL, NAME + "@test.tuu")
            register_page.click(register_page.locators.FORM_CONFIRM)
            register_page.click(register_page.locators.BUTTON_SUBMIT)
            assert "Passwords must match" in register_page.driver.page_source
            assert self.builder.check_user_by_name(NAME) == False
        elif err == "email":
            NAME = register_page.generate_data()
            register_page.send(register_page.locators.FORM_USERNAME, NAME)
            register_page.send(register_page.locators.FORM_PASSWORD, NAME)
            register_page.send(register_page.locators.FORM_CPASSWORD, NAME)
            register_page.send(register_page.locators.FORM_EMAIL, NAME + "@")
            register_page.click(register_page.locators.FORM_CONFIRM)
            register_page.click(register_page.locators.BUTTON_SUBMIT)
            assert "Invalid email address" in register_page.driver.page_source
            assert self.builder.check_user_by_name(NAME) == False
        elif err == "name":
            NAME = register_page.generate_data()
            register_page.send(register_page.locators.FORM_USERNAME, "6")
            register_page.send(register_page.locators.FORM_PASSWORD, NAME)
            register_page.send(register_page.locators.FORM_CPASSWORD, NAME)
            register_page.send(register_page.locators.FORM_EMAIL, NAME + "@")
            register_page.click(register_page.locators.FORM_CONFIRM)
            register_page.click(register_page.locators.BUTTON_SUBMIT)
            assert "Incorrect username length" in register_page.driver.page_source
            assert self.builder.check_user_by_name(NAME) == False

    @pytest.mark.UI
    @pytest.mark.parametrize("err", [1, 2, 3])
    def test_reg_form_validation_multiple_error(self, register_page, err):
        """
        CHECK REGISTER FORM VALIDATION ERRORS

        Step 1:
        Type in data into forms (with 2 or 3 errors)

        Step 2:
        Click register

        Step 3:
        Check that user is not created and error message is displayed

        EXPECT: 
        User is not created, error message displayed correctly
        """
        if err == 1:     
            NAME = register_page.generate_data()
            register_page.send(register_page.locators.FORM_USERNAME, "1")
            register_page.send(register_page.locators.FORM_PASSWORD, NAME)
            register_page.send(register_page.locators.FORM_CPASSWORD, NAME + "@test.tuu")
            register_page.send(register_page.locators.FORM_EMAIL, NAME + "@test.tuu")
            register_page.click(register_page.locators.FORM_CONFIRM)
            register_page.click(register_page.locators.BUTTON_SUBMIT)
            assert "Passwords must match" in register_page.driver.page_source
            assert "Incorrect username length" in register_page.driver.page_source
            assert "{'username': ['Incorrect username length'], 'password': ['Passwords must match']}" not in register_page.driver.page_source
            assert self.builder.check_user_by_name(NAME) == False
        elif err == 2:
            NAME = register_page.generate_data()
            register_page.send(register_page.locators.FORM_USERNAME, NAME)
            register_page.send(register_page.locators.FORM_PASSWORD, NAME)
            register_page.send(register_page.locators.FORM_CPASSWORD, NAME + "Q")
            register_page.send(register_page.locators.FORM_EMAIL, NAME + "@")
            register_page.click(register_page.locators.FORM_CONFIRM)
            register_page.click(register_page.locators.BUTTON_SUBMIT)
            assert "Invalid email address" in register_page.driver.page_source
            assert "Passwords must match" in register_page.driver.page_source
            assert "{'email': ['Invalid email address'], 'password': ['Passwords must match']}" not in register_page.driver.page_source
            assert self.builder.check_user_by_name(NAME) == False
        elif err == 3:
            NAME = register_page.generate_data()
            register_page.send(register_page.locators.FORM_USERNAME, "6")
            register_page.send(register_page.locators.FORM_PASSWORD, NAME)
            register_page.send(register_page.locators.FORM_CPASSWORD, NAME + "Q")
            register_page.send(register_page.locators.FORM_EMAIL, NAME + "@")
            register_page.click(register_page.locators.FORM_CONFIRM)
            register_page.click(register_page.locators.BUTTON_SUBMIT)
            assert "Incorrect username length" in register_page.driver.page_source
            assert "Passwords must match" in register_page.driver.page_source
            assert "Invalid email address" in register_page.driver.page_source
            assert "{'username': ['Incorrect username length'], 'email': ['Invalid email address'], 'password': ['Passwords must match']}" not in register_page.driver.page_source
            assert self.builder.check_user_by_name(NAME) == False

    @pytest.mark.UI   
    def test_register_positive(self, register_page):
        """
        CHECK REGISTERATION POSITIVE

        Step 1:
        Register user via registration page

        Step 2:
        Check that user is in the db

        EXPECT: 
        User exists in db
        """
        user = register_page.get_user()
        register_page.send(register_page.locators.FORM_USERNAME, user.username)
        register_page.send(register_page.locators.FORM_PASSWORD, user.password)
        register_page.send(register_page.locators.FORM_CPASSWORD, user.password)
        register_page.send(register_page.locators.FORM_EMAIL, user.email)
        register_page.click(register_page.locators.FORM_CONFIRM)
        register_page.click(register_page.locators.BUTTON_SUBMIT)
        time.sleep(2)
        assert self.builder.check_user(user) == True
        self.builder.delete_user(user)

    @pytest.mark.UI   
    def test_register_active_time(self, register_page):
        """
        CHECK 'ACTIVE TIME' FLAG AFTER REGISTRATION

        Step 1:
        Register user via registration page

        Step 2:
        Check that 'active time' field is not null in database

        EXPECT: 
        'active time' field is not null in database
        """
        user = register_page.get_user()
        register_page.send(register_page.locators.FORM_USERNAME, user.username)
        register_page.send(register_page.locators.FORM_PASSWORD, user.username)
        register_page.send(register_page.locators.FORM_CPASSWORD, user.username)
        register_page.send(register_page.locators.FORM_EMAIL, user.email)
        register_page.click(register_page.locators.FORM_CONFIRM)
        register_page.click(register_page.locators.BUTTON_SUBMIT)
        active_time = self.builder.get_datetime(user)
        self.builder.delete_user(user)
        assert active_time is not None

    @pytest.mark.UI   
    def test_register_active(self, register_page):
        """
        CHECK 'ACTIVE' FLAG AFTER REGISTRATION

        Step 1:
        Register user via registration page

        Step 2:
        Check that 'active' field is not null in database

        EXPECT: 
        'active' field == 1
        """
        user = register_page.get_user()
        register_page.send(register_page.locators.FORM_USERNAME, user.username)
        register_page.send(register_page.locators.FORM_PASSWORD, user.username)
        register_page.send(register_page.locators.FORM_CPASSWORD, user.username)
        register_page.send(register_page.locators.FORM_EMAIL, user.email)
        register_page.click(register_page.locators.FORM_CONFIRM)
        register_page.click(register_page.locators.BUTTON_SUBMIT)
        active = self.builder.get_active(user)
        self.builder.delete_user(user)
        assert active == 1
        
class TestMainPage(BaseCase):

    @pytest.mark.UI
    def test_logout(self, main_page):
        """
        CHECK LOGOUT BUTTON

        Step 1:
        Click logout button on the main page

        EXPECT: 
        login page is shown
        """
        main_page.click(main_page.locators.BUTTON_LOGOUT)
        assert 'Welcome to the TEST SERVER' in main_page.driver.page_source

    @pytest.mark.UI
    def test_what_is_api(self, main_page):
        """
        CHECK 'WHAT IS API' BUTTON

        Step 1:
        Click 'what is api' button on the main page

        EXPECT: 
        wikipedia page is shown
        """
        main_page.click(main_page.locators.BUTTON_API)
        main_page.driver.switch_to.window(main_page.driver.window_handles[-1])
        assert 'Application programming interface - Wikipedia' in main_page.driver.page_source

    @pytest.mark.UI
    def test_future_of_the_internet(self, main_page):
        """
        CHECK 'FUTURE OF THE INTERNET' BUTTON

        Step 1:
        Click 'future of the internet' button on the main page

        EXPECT: 
        'future of the internet' article is shown
        """
        main_page.click(main_page.locators.BUTTON_INTERNET)
        main_page.driver.switch_to.window(main_page.driver.window_handles[-1])
        assert 'What Will the Internet Be Like in the Next 50 Years?' in main_page.driver.page_source

    @pytest.mark.UI
    def test_smtp(self, main_page):
        """
        CHECK 'SMTP' BUTTON
        
        Step 1:
        Click 'SMTP' button on the main page

        EXPECT: 
        wikipedia page is shown
        """
        main_page.click(main_page.locators.BUTTON_SMTP)
        main_page.driver.switch_to.window(main_page.driver.window_handles[-1])
        assert 'SMTP — Википедия' in main_page.driver.page_source

    @pytest.mark.UI
    def test_home(self, main_page):
        """
        CHECK 'HOME' BUTTON

        Step 1:
        Click 'home' button on the main page

        EXPECT: 
        Main page is shown
        """
        main_page.click(main_page.locators.BUTTON_HOME)
        assert "TM version 0.1" in main_page.driver.page_source

    @pytest.mark.UI
    def test_python(self, main_page):
        """
        CHECK 'PYTHON' BUTTON

        Step 1:
        Click 'python' button on the main page

        EXPECT: 
        Python.org page is shown
        """
        main_page.click(main_page.locators.BUTTON_PYTHON)
        assert "python home" in main_page.driver.page_source

    @pytest.mark.UI
    def test_history_python(self, main_page):
        """
        CHECK 'PYTHON HISTORY' BUTTON

        Step 1:
        Click 'python history' button on the main page

        EXPECT: 
        "History of Python - Wikipedia" page is shown
        """
        element = main_page.find(main_page.locators.BUTTON_PYTHON_MENU)
        ActionChains(main_page.driver).move_to_element(element).perform()
        main_page.click(main_page.locators.BUTTON_HISTORY_PYTHON)
        assert "History of Python - Wikipedia" in main_page.driver.page_source

    @pytest.mark.UI
    def test_flask(self, main_page):
        """
        CHECK 'flask' BUTTON

        Step 1:
        Click 'flask' button on the main page

        EXPECT: 
        Flask documentation main page is shown
        """
        element = main_page.find(main_page.locators.BUTTON_PYTHON_MENU)
        ActionChains(main_page.driver).move_to_element(element).perform()
        main_page.click(main_page.locators.BUTTON_FLASK)
        main_page.driver.switch_to.window(main_page.driver.window_handles[-1])
        assert "Welcome to Flask — Flask Documentation" in main_page.driver.page_source
        
    @pytest.mark.UI
    def test_linux(self, main_page):
        """
        CHECK 'download centos 7' BUTTON

        Step 1:
        Click 'download centos 7' button on the main page

        EXPECT: 
        Centos 7 download page is shown
        """
        element = main_page.find(main_page.locators.BUTTON_LINUX)
        ActionChains(main_page.driver).move_to_element(element).perform()
        main_page.click(main_page.locators.BUTTON_CENTOS)
        main_page.driver.switch_to.window(main_page.driver.window_handles[-1])
        assert "centos" in main_page.driver.page_source

    @pytest.mark.UI
    def test_wireshark_news(self, main_page):
        """
        CHECK 'wireshark news' BUTTON

        Step 1:
        Click 'wireshark news' button on the main page

        EXPECT: 
        'wireshark news' page is shown
        """
        element = main_page.find(main_page.locators.BUTTON_NETWORK)
        ActionChains(main_page.driver).move_to_element(element).perform()
        main_page.click(main_page.locators.BUTTON_NEWS)
        main_page.driver.switch_to.window(main_page.driver.window_handles[-1])
        assert "Wireshark · News" in main_page.driver.page_source

    @pytest.mark.UI
    def test_wireshark_download(self, main_page):
        """
        CHECK 'wireshark download' BUTTON

        Step 1:
        Click 'wireshark download' button on the main page

        EXPECT: 
        'wireshark download' page is shown
        """
        element = main_page.find(main_page.locators.BUTTON_NETWORK)
        ActionChains(main_page.driver).move_to_element(element).perform()
        main_page.click(main_page.locators.BUTTON_DOWNLOAD)
        main_page.driver.switch_to.window(main_page.driver.window_handles[-1])
        assert "Wireshark · Go Deep." in main_page.driver.page_source

    @pytest.mark.UI
    def test_tcpdump(self, main_page):
        """
        CHECK 'tcpdump' BUTTON

        Step 1:
        Click 'tcpdump' button on the main page

        EXPECT: 
        TCPdump examples page is shown
        """
        element = main_page.find(main_page.locators.BUTTON_NETWORK)
        ActionChains(main_page.driver).move_to_element(element).perform()
        main_page.click(main_page.locators.BUTTON_EXAMPLES)
        main_page.driver.switch_to.window(main_page.driver.window_handles[-1])
        assert "Tcpdump Examples - 22 Tactical Commands | HackerTarget.com" in main_page.driver.page_source
