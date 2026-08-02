from playwright.sync_api import Page

class CheckoutCompletePage:

    def __init__(self,page: Page):
        self.page = page
        self.complete_header = page.get_by_role("heading", name="Thank you for your order!")

    
