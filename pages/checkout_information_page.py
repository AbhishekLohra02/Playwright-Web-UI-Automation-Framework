from playwright.sync_api import Page

class CheckoutInformationPage:

    def __init__(self,page: Page):
        self.page = page
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.postal_code_input = page.get_by_placeholder("Zip/Postal Code")
        self.click_continue_button = page.get_by_role("button", name="Continue")
        self.error_message = page.get_by_test_id("error")


    def enter_details(self, first_name:str, last_name:str, postal_code:str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def click_continue(self) -> None:
        self.click_continue_button.click()

                                   

        
