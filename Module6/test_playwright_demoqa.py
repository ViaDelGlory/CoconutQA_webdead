from playwright.sync_api import Page, expect
import time
from pathlib import Path
from datetime import datetime
from Module6.Tools import Tools

def test_text_box(page: Page):
    page.goto('https://demoqa.com/text-box')

    username_locator = '#userName'
    page.fill(username_locator, 'testQa')
    page.fill('#userEmail', 'test@qa.com')
    page.fill('#currentAddress', 'Phuket, Thalang 99')
    page.fill('#permanentAddress', 'Moscow, Mashkova 1')

    page.click('button#submit')

    expect(page.locator('#output #name')).to_have_text('Name:testQa')
    expect(page.locator('#output #email')).to_have_text('Email:test@qa.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :Phuket, Thalang 99')
    expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :Moscow, Mashkova 1')

    time.sleep(5)

def test_example(page: Page):

    page.goto('https://demoqa.com/text-box')

    page.get_by_role("textbox", name="Full Name").click()
    page.pause()
    page.get_by_role("textbox", name="Full Name").fill("Ебланчик")
    page.get_by_role("textbox", name="Full Name").press("Tab")
    page.get_by_role("textbox", name="name@example.com").fill("EbloYtinoe@mail.ru")
    page.get_by_role("textbox", name="name@example.com").press("Tab")
    page.get_by_role("textbox", name="Current Address").fill("S123S123")
    page.get_by_role("textbox", name="Current Address").press("Tab")
    page.locator("#permanentAddress-wrapper #permanentAddress").fill("St.Penis, h, 2")
    page.get_by_role("button", name="Submit").click()

def test_example_locator1(page: Page):
    """Работа по определению локаторов-CSS и интерактивность с элементами 'Web Tables'"""
    #Переходим на сайт с таблицей
    page.goto("https://demoqa.com/webtables")

    #Находим локатор и кликаем по нему
    page.locator('button:has-text("Add")').click()

    #Убеждаемся, что открылась форма
    locator_reg = page.get_by_text("Registration Form")
    expect(locator_reg).to_be_visible(timeout=5000)

    #Заполянем инпуты
    page.locator('input[placeholder="First Name"]').fill("Xyu")
    page.locator('input[placeholder="Last Name"]').fill("Вонючий")
    page.locator('input[placeholder="name@example.com"]').fill("SobakaPomet@gmail.com")
    page.locator('input[placeholder="Age"]').fill("12")
    page.locator('input[placeholder="Salary"]').fill("1337")
    page.locator('input[placeholder="Department"]').fill("SQL")

    #Нажимаем кнопку Submit
    page.locator('button:has-text("Submit")').click()

    time.sleep(5)

def test_example_practice_form(page: Page):
    """Тестирование заполнение формы"""
    today = datetime.now().strftime("%d %b %Y")
    page.goto("https://demoqa.com/automation-practice-form")

    #Заполняем форму
    page.fill('#firstName', "Вячеслав")
    page.type('input[placeholder="Last Name"]', "Молочков")
    page.fill('#userEmail', "Sobaka@mail.ru")
    page.check('#gender-radio-3')
    page.type('input[placeholder="Mobile Number"]', "88005553535")

    #Забираем value из времени и проверяем с системной
    assert page.get_attribute('#dateOfBirthInput', 'value') == today, \
    f"Ожидали, что время будет равно {today}"

    #Продолжаем заполнять форму
    subjects = page.locator("#subjectsInput")
    subjects.fill("Maths")
    subjects.press("Enter")

    page.check('#hobbies-checkbox-1')
    page.get_by_placeholder("Current Address").fill("St.Pisunov")

    #Локаторы выпадающего списка
    page.locator("#state").click()
    page.get_by_text("NCR", exact=True).click()
    page.locator("#city").click()
    page.get_by_text("Delhi", exact=True).click()

    #Находим футер
    footer = page.text_content('footer span')
    assert footer == "© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED."

def test_is_enabled(page: Page):
    """Проверка активности 2 радиобаттонов и неактивности 3-го"""

    page.goto("https://demoqa.com/radio-button")

    #Проверка активности радио-батонов
    assert page.is_enabled('#yesRadio')
    assert page.is_enabled('#impressiveRadio')
    assert not page.is_enabled('input#noRadio') # Или через is_disabled()

def test_is_visible(page: Page):
    """Проверка видимости Home и Desktop"""

    page.goto("https://demoqa.com/checkbox")

    home_locator = page.get_by_role("checkbox", name="Select Home")
    desktop_locator = page.get_by_role("checkbox", name="Select Desktop")

    # Home виден, Desktop не виден
    assert home_locator.is_visible()
    assert not desktop_locator.is_visible()

    # Раскрываем дерево
    page.click("span.rc-tree-switcher")

    # Desktop стал виден
    assert desktop_locator.is_visible()

def test_wait(page:Page):
    """Через 5 секунд после загрузки страницы появится элемент"""

    # Элемента нет на странице
    page.goto('https://demoqa.com/dynamic-properties')
    assert not page.is_visible('button#visibleAfter')

    # Проверяем что он появится через 5 секунд

    assert page.wait_for_selector('button#visibleAfter', timeout=6000)
    assert page.is_visible('button#visibleAfter')


def test_expect(page: Page):
    page.goto("https://demoqa.com/radio-button")
    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")
    expect(no_radio).to_be_disabled()  # проверяем, что не доступен
    expect(yes_radio).to_be_enabled()  # проверяем, что доступен
    expect(impressive_radio).to_be_enabled()  # проверяем, что доступен
    page.locator('[for="yesRadio"]').click()  # тут хитрый лейбл не позволяет кликнуть прямо на инпут, обращаемся по лейблу
    expect(yes_radio).to_be_checked()  # проверяем, что отмечен
    expect(impressive_radio).not_to_be_checked()  # проверяем, что не отмечен
