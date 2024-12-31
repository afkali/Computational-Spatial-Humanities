import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import unquote
import re
import os
import time


def sanitize_filename(filename):
    base_name = os.path.basename(filename)
    name, extension = os.path.splitext(base_name)
    truncated_name = name[:100 - len(extension)]
    sanitized_name = re.sub(r'[^\w\s-]', '_', truncated_name)

    # decode URL-encoded characters
    sanitized_name = unquote(sanitized_name)
    sanitized_name = sanitized_name.replace('.', '')
    sanitized_name = sanitized_name.replace('__', '_')
    sanitized_name = sanitized_name.replace('\n', '')
    sanitized_name = sanitized_name.replace(' ', '_')
    sanitized_name = sanitized_name.replace('?', '_')

    # replace invalid characters with underscores
    invalid_chars = r'[<>|":/?\\]'
    sanitized_name = re.sub(invalid_chars, '_', sanitized_name)
    sanitized_name = sanitized_name.rstrip('._')
    sanitized_filename = sanitized_name.strip('_') + extension
    return sanitized_filename

    
def scrape_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        return None

def download_image(image_url, link_text, folder_name):
    image_name = os.path.basename(image_url)
    sanitized_link_text = sanitize_filename(link_text)
    sanitized_image_name = sanitize_filename(image_name)
    filename = f"{sanitized_link_text}_{sanitized_image_name}"
    file_path = os.path.join(folder_name, filename)
    print("file path:", file_path)
    
    response = requests.get(image_url)
    
    if response.status_code == 200:
        try:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"saved image: {filename}")
        except OSError as e:
            print(f"failed to download image: {filename}")
            print(f"error: {e}")
    else:
        print(f"failed to download image: {filename}")



main_url = "https://www.joyceproject.com/index.php?chapter=telem&notes=1"
response = requests.get(main_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find(id='frame')

    if body:
        links = body.find_all('a')
        links_content = []

        folder_name = "text_files_2_2"
        os.makedirs(folder_name, exist_ok=True)

        for link in links:
            link_text = link.get_text()
            # PRINT
            print("Linktext1:"+ link_text)

            link_url = link.get('href')
            absolute_url = urljoin(main_url, link_url)
            links_content.append((link_text, absolute_url))
            linked_page = scrape_page(absolute_url)
            if linked_page:
                linked_page_content = linked_page.get_text().strip()
                linked_images = linked_page.find_all('img')
                if linked_images:
                    for image in linked_images:
                        image_src = image.get('src')
                        absolute_image_url = urljoin(absolute_url, image_src)
                        download_image(absolute_image_url, link_text, folder_name)
                        time.sleep(1)

                if linked_page_content:
                    print(f"content of {link_text}: ")
                    print(linked_page_content)
                    print()

                    # remove multiple whitespace characters
                    cleaned_content = re.sub(r'\s+', ' ', linked_page_content)

                    # sanitize link text for filename
                    sanitized_link_text = sanitize_filename(link_text)
                    print("Link_San:"+sanitized_link_text)

                    # adjust filename
                    filename = sanitized_link_text + ".txt"
                    filename = filename.replace('?', '')
                    filename = filename.replace(' ', '')
                    filename = filename.replace('_', ' ')
                    filename = filename.replace('\n', ' ')
                    

                    file_path = os.path.join(folder_name, filename)

                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(cleaned_content)

                    # pause between requests
                    time.sleep(1)


        scraped_content = body.get_text().strip()
        print("Main Page Content: ")
        print(scraped_content)
        print()

        # remove multiple whitespace characters
        cleaned_content = re.sub(r'\s+', ' ', scraped_content)

        # save main content to a text file
        main_content_file = os.path.join(folder_name, "main_page.txt")
        with open(main_content_file, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

    else:
        print("No body tag found")
else:
    print("failed to retrieve the web page")