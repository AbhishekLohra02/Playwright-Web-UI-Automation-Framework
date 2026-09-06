from playwright.sync_api import Page, expect

from pages.components.header import HeaderComponent


class BasePage:
    """Common behavior shared by every SauceDemo page object.

    Subclasses declare the path they own as `url_path`, so navigation and
    page-state checks are expressed once instead of being rebuilt in each test.

    Navigation methods return the page object for the screen they land on. That
    is what makes a test read as a journey rather than as a series of
    constructor calls, and it means the page objects - not the tests - own the
    knowledge of what follows what. Because those return types point at sibling
    modules, the imports are made inside the methods to avoid an import cycle.
    """

    url_path = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self) -> None:
        self.page.goto(self.url_path)

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url(self.url_path)


class AuthenticatedPage(BasePage):
    """A page that is only reachable once a user has signed in.

    Everything shared between such pages is the header, which is composed in
    rather than inherited.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
