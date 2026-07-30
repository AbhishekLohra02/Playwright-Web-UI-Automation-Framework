from playwright.sync_api import Page


class InventoryPage: 
    def __init__(self, page: Page):
        self.page = page
        self.page_title = page.get_by_test_id("title")
        
        