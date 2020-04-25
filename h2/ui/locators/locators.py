from selenium.webdriver.common.by import By


class CabinetPageLocators:
    BUTTON_SALEPOINTS = (By.XPATH, '// div[contains(@class, "column-list-item__title js-title")]')
    SELECTOR_MULTIFORMAT = (By.ID, '187')
    SELECTOR_BANNER = (By.ID, '192')
    BUTTON_UPLOAD_PIC = (By.XPATH, '//input[@type="file" and @data-gtm-id="load_image_btn_240_400"]')
    FORM_HEADER = (By.XPATH, '//input[@type="text" and @data-gtm-id="banner_form_title"]')
    FORM_DESCRIPTION = (By.XPATH, '//textarea[@data-gtm-id="banner_form_text"]')
    BUTTON_SUBMIT = (By.XPATH, '//div[@class="button__text" and contains(text(), "Добавить объявление")]')
    BUTTON_CREATE_C = (By.XPATH, '//div[@class="button__text" and contains(text(), "Создать кампанию")]')
    BUTTON_ACTIONS = (By.XPATH, '//button[@class="button button_general button_campaigns-tbl-actions"]')
    BUTTON_CREATE_CAMPAIGN = (By.XPATH, '//a[@href="/campaign/new"]')
    FORM_SITE_NAME = (By.CSS_SELECTOR, '.input_create-main-url input')
    FORM_CAMPAIGN_NAME = (By.CSS_SELECTOR, '.campaign-name input')
    BUTTON_DELETE = (By.XPATH, '//span[contains(text(),"Удалить")]')
    CAMPAIGN = '//a[contains(text(),"{}")]'
    CHKBX_CREATED_CAMPAIGN = '//a[contains(text(),"{}")]/../../../input'
    BUTTON_TO_SEGMENTS = (By.XPATH, '//a[contains(text(),"Аудитории")]')


class SegmentPageLocators:
    BUTTON_CREATE_SEGMENT_2 = (By.XPATH, '//a[@href="/segments/segments_list/new"]')
    BUTTON_CREATE_SEGMENT_1 = (By.XPATH, '//div[@class="button__text" and contains(text(),"сегмент")]')
    ADD_SEGMENT = (By.CLASS_NAME, 'create-segment-form__block')
    SEGMENT_NAME = (By.CSS_SELECTOR, '.js-segment-name input')
    BUTTON_APPS = (By.XPATH, '//div[contains(text(),"Приложения (ОК и МойМир)")]')
    CHECKBOX_SEGM = (By.XPATH, '//input[@type="checkbox"]')
    BUTTON_ADD_SEGMENT_1 = (By.XPATH, '//div[@class="button__text" and contains(text(),"Добавить сегмент")]')
    CREATED_SEGMENT = '//a[contains(text(),"{}")]'
    BUTTON_DELETE_CONFIRM = (By.XPATH, '//div[contains(text(),"Удалить")]')
    BUTTON_DELETE_SEGMENT = '//tr[@class="flexi-table__row" and .//a[@title="{}"]]//span[@class="icon-cross"]'
    BUTTON_TO_SEGMENTS = (By.XPATH, '//a[contains(text(),"Аудитории")]')


class MainPageLocators:
    BUTTON_LOGIN = (By.XPATH, '//div[contains(text(), "Войти")]')
    FORM_EMAIL = (By.NAME, "email")
    FORM_PASSWORD = (By.NAME, "password")
