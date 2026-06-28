from browser import Browser


with Browser() as browser:

    page = browser.new_page()

    page.goto("https://www.google.com")

    print(page.title())