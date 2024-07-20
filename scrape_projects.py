from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def setup_driver():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def get_project_links(driver):
    base_url = 'https://hprera.nic.in/PublicDashboard'
    driver.get(base_url)
    time.sleep(10)  # Wait for the page to load fully

    # Print page source for debugging
    page_source = driver.page_source
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(page_source)

    project_links = []
    try:
        # Update the selector based on actual HTML
        project_section = driver.find_element(By.ID, 'content-tab_project_main')  # Adjust if necessary
        links = project_section.find_elements(By.TAG_NAME, 'a')

        for link in links:
            href = link.get_attribute('href')
            if href and 'rera-number' in href:
                project_links.append(href)
                if len(project_links) == 6:
                    break
    except Exception as e:
        print(f"Error extracting project links: {e}")

    print("Extracted project links:", project_links)
    return project_links

def get_project_details(driver, link):
    driver.get(link)
    time.sleep(10)  # Wait for the page to load

    details = {
        'GSTIN No': '',
        'PAN No': '',
        'Name': '',
        'Permanent Address': ''
    }

    try:
        # Update the selectors based on actual HTML
        gstin_tag = driver.find_element(By.XPATH, "//div[contains(text(), 'GSTIN No')]/following-sibling::div")
        details['GSTIN No'] = gstin_tag.text.strip()

        pan_tag = driver.find_element(By.XPATH, "//div[contains(text(), 'PAN No')]/following-sibling::div")
        details['PAN No'] = pan_tag.text.strip()

        name_tag = driver.find_element(By.XPATH, "//div[contains(text(), 'Name')]/following-sibling::div")
        details['Name'] = name_tag.text.strip()

        address_tag = driver.find_element(By.XPATH, "//div[contains(text(), 'Permanent Address')]/following-sibling::div")
        details['Permanent Address'] = address_tag.text.strip()

    except Exception as e:
        print(f"Error extracting details: {e}")

    return details

def main():
    driver = setup_driver()
    try:
        project_links = get_project_links(driver)
        if not project_links:
            print("No project links found.")
            return

        all_project_details = []

        for link in project_links:
            details = get_project_details(driver, link)
            all_project_details.append(details)

        df = pd.DataFrame(all_project_details)
        df.to_csv('project_details.csv', index=False)
        print("Data has been saved to project_details.csv")

    finally:
        driver.quit()

if __name__ == '__main__':
    main()
