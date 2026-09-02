from playwright.sync_api import Page, expect


from pages.base_page import BasePage


class CinescopeMoviePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.more_button = '[data-qa-id="more_button"]'
        self.review_input = '[data-qa-id="movie_review_input"]'
        self.review_submit_button = '[data-qa-id="movie_review_submit_button"]'

    def open_first_movie(self):
        self.click_first(self.more_button)

    def add_review(self, review_text: str):
        self.enter_text(self.review_input, review_text)
        self.click(self.review_submit_button)