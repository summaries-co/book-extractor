import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException


def setup_driver():
    # Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Comment this if you don't want to run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    return driver


def click_in_empty_space(driver):
    """
    Try to click in an empty space on the page to dismiss any unexpected overlays or popups.
    """
    try:
        # Clicking at a position that's generally empty to avoid popups
        ActionChains(driver).move_by_offset(10, 10).click().perform()
        print("Clicked in empty space to avoid popups.")
    except Exception as e:
        print(f"Failed to click in empty space: {e}")


def load_full_page(driver, url):
    driver.get(url)
    time.sleep(2)  # Wait for the initial page elements to load
    try:
        while True:
            show_more = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button--small')]"
                                                      "//span[contains(text(), 'Show more books')]/.."))
            )
            ActionChains(driver).move_to_element(show_more).click().perform()
            time.sleep(1)
    except TimeoutException as e:
        # Handle the case where the 'Show more books' button is no longer present or another timeout scenario
        if e.args:
            print(f"Finished loading all books or cannot click 'Show more': {e.args[0].splitlines()[0]}")
        else:
            print("Finished loading all books or cannot click 'Show more': No additional information available.")
    except ElementClickInterceptedException:
        # If clicking fails due to an intercepted click, click in an empty space and retry
        click_in_empty_space(driver)
        try:
            show_more = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Button--small')]"
                                                      "//span[contains(text(), 'Show more books')]/.."))
            )
            ActionChains(driver).move_to_element(show_more).click().perform()
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Could not find or click on 'Show more books' button after attempting to clear popups: {str(e)}")


def extract_books_data(driver):
    books = []
    elements = driver.find_elements(By.CSS_SELECTOR, "article.BookListItem")
    for element in elements:
        try:
            rank = element.find_element(By.CSS_SELECTOR, ".BookListItemRank h2").text.strip('#')
            title = element.find_element(By.CSS_SELECTOR, ".BookListItem__title h3 a").text
            author = element.find_element(By.CSS_SELECTOR, ".ContributorLink__name").text
            rating = element.find_element(By.CSS_SELECTOR, ".AverageRating__ratingValue").text
            books.append([rank, title, author, rating])
        except Exception as e:
            print(f"Failed to extract data for one book: {e}")
    return books


def save_to_csv(books, filename):
    """
    Save the extracted books data to a CSV file.
    """
    df = pd.DataFrame(books, columns=['Ranking', 'Title', 'Author', 'Average Rating'])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def get_goodreads_books_by(year, months):
    """
    Main function to extract books data for a given year and months.
    """
    driver = setup_driver()
    for month in months:
        url = f"https://www.goodreads.com/book/popular_by_date/{year}/{month}"
        print(f"Processing {url}")
        load_full_page(driver, url)
        books = extract_books_data(driver)
        data_path = 'data'
        save_to_csv(books, f"{data_path}/goodreads_books_{year}_{month}.csv")
    driver.quit()


if __name__ == "__main__":

    year = 2023
    # Set 'months' to a specific list of months, example:
    # months = [2, 3, 4] to process February, March, and April or
    # months = list(range(1, 13)) to process the Full Year.
    months = list(range(1, 13))
    get_goodreads_books_by(year, months)

