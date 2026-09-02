from playwright.sync_api import Page, expect
from random import randint
import time


def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    # вариант №1
    username_locator = '[data-qa-id="register_full_name_input"]'
    email_loacor = '[data-qa-id="register_email_input"]'
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

    user_email = f'test{randint(1, 9999)}-admin@email.qa'

    page.fill(username_locator, 'Жмышенко Валерий Альбертович')
    page.fill(email_loacor, user_email)
    page.fill(password_locator, 'qwerty123Q')
    page.fill(repeat_password_locator, 'qwerty123Q')

    page.click('[data-qa-id="register_submit_button"]')

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)

    time.sleep(5)

def test_run(playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demoqa.com/")
    page.get_by_role("link", name="Forms").click()
    page.get_by_role("link", name="Practice Form").click()
    page.get_by_role("textbox", name="name@example.com").click()
    page.get_by_role("textbox", name="name@example.com").fill("фывыфвы")
    page.get_by_role("textbox", name="name@example.com").press("ControlOrMeta+a")
    page.get_by_role("textbox", name="name@example.com").fill("SssodsssS@mail.ru")
    page.get_by_role("radio", name="Male", exact=True).check()
    page.locator("#dateOfBirthInput").click()
    page.get_by_role("gridcell", name="Choose Tuesday, September 22nd,").click()

    # ---------------------
    context.close()
    browser.close()