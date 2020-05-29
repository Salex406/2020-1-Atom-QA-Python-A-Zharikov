from selenium.webdriver.common.by import By


class LoginPageLocators:
    BUTTON_LOGIN = (By.ID, 'submit')
    BUTTON_REGISTER = (By.XPATH, '//a[@href="/reg"]')
    FORM_LOGIN = (By.ID, 'username')
    FORM_PASSWORD = (By.ID, 'password')
    
class MainPageLocators:
    BUTTON_LOGIN = (By.ID, 'submit')
    FORM_LOGIN = (By.ID, 'username')
    FORM_PASSWORD = (By.ID, 'password')
    BUTTON_HOME = (By.XPATH, '//a[@href="/"]')
    
    BUTTON_PYTHON = (By.XPATH, '//a[@href="https://www.python.org/"]')
    BUTTON_HISTORY_PYTHON = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/History_of_Python"]')
    BUTTON_FLASK = (By.XPATH, '//a[@href="https://flask.palletsprojects.com/en/1.1.x/#"]')
    BUTTON_PYTHON_MENU = (By.XPATH, '//*[@id="wrap"]/header[1]/nav[1]/ul[1]/li[2]')
    
    BUTTON_LINUX = (By.XPATH, '//a[contains(text(),"Linux")]')
    BUTTON_CENTOS = (By.XPATH, '//a[@href="https://getfedora.org/ru/workstation/download/"]')
    
    BUTTON_NETWORK = (By.XPATH, '//a[contains(text(),"Network")]')
    BUTTON_NEWS = (By.XPATH, '//a[@href="https://www.wireshark.org/news/"]')
    BUTTON_DOWNLOAD = (By.XPATH, '//a[@href="https://www.wireshark.org/#download"]')
    BUTTON_EXAMPLES = (By.XPATH, '//a[@href="https://hackertarget.com/tcpdump-examples/"]')
    
    BUTTON_API = (By.XPATH, '//a[@href="https://en.wikipedia.org/wiki/Application_programming_interface"]')
    BUTTON_INTERNET = (By.XPATH, '//a[@href="https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"]')
    BUTTON_SMTP = (By.XPATH, '//a[@href="https://ru.wikipedia.org/wiki/SMTP"]')
    BUTTON_LOGOUT = (By.XPATH, '//a[@href="/logout"]')

class RegisterPageLocators:
    FORM_USERNAME = (By.ID, 'username')
    FORM_PASSWORD = (By.ID, 'password')
    FORM_EMAIL = (By.ID, 'email')
    FORM_CPASSWORD = (By.ID, 'confirm')
    FORM_CONFIRM = (By.ID, 'term')
    BUTTON_SUBMIT = (By.ID, 'submit')
