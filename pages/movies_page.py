from playwright.sync_api import Page
from pages.base_page import BasePage

class CinescopeMoviesPage(BasePage):
    def __init__(self, page: Page):
        self.page = page

        self.all_movies_link = page.get_by_role("link", name="Все фильмы")

        self.city_filter = page.get_by_role("combobox").nth(0)
        self.genre_filter = page.get_by_role("combobox").nth(1)
        self.sort_filter = page.get_by_role("combobox").nth(2)

        self.details_buttons = page.get_by_role("button", name="Подробнее")

    def open(self):
        self.all_movies_link.click()

    def select_city(self, city: str):
        self.city_filter.click()
        self.page.get_by_role("option", name=city).click()

    def select_genre(self, genre: str):
        self.genre_filter.click()
        self.page.get_by_role("option", name=genre).click()

    def select_sort(self, sort_value: str):
        self.sort_filter.click()
        self.page.get_by_role("option", name=sort_value).click()

    def open_first_movie(self):
        self.details_buttons.first.click()