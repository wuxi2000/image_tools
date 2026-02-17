from loguru import logger
import requests
import threading
import os

# ##############################
# consts
# ##############################

LOG_FILE = 'logs/download_image.log'
INPUT_BOOK_URL_LIST_FILE = 'data/list.txt'
OUTPUT_IMAGE_FOLDER = 'data/images/'
MAX_PAGE_NO = 200
EXT_NAME_LIST = ['jpg','webp', 'png']
MULTI_THREAD_MODE = True

# ##############################
# functions
# ##############################

def init_logger():
    logger.add(
        LOG_FILE, 
        level="DEBUG",
        format='{time:HH:mm:ss.SSS}|{level: <8}|{function}:{line} - {message}'
    )


def read_book_url_list():
    list_file_path = INPUT_BOOK_URL_LIST_FILE
    book_urls = []
    with open(list_file_path, 'r') as f:
        for line in f:
            book_urls.append(line.strip())

    return book_urls

def analyze_book_url(book_url):
    folder_name = '' 
    page_url_template = ''
    filename_template = ''

    last_slash_index = book_url.rfind('/')
    second_last_slash_index = book_url.rfind('/', 0, last_slash_index)

    folder_name = book_url[second_last_slash_index+1 : last_slash_index]
    page_url_template = book_url[0: last_slash_index+1] + '{page_no}' + '.' + '{ext_name}'
    filename_template = '{page_no}' + '.' + '{ext_name}'

    return folder_name, page_url_template, filename_template

def download_single_file(remote_url, local_file_path):

    try:
        response = requests.get(remote_url)
        if response.status_code != 200:
            logger.trace(f'{remote_url}->False')
            return False

        with open(local_file_path, 'wb') as f:
            f.write(response.content)

        logger.trace(f'{remote_url}->True')
        return True

    except Exception as e:
        logger.trace(f'{remote_url}->True')
        logger.exception(e)
        return False

def download_book(book_url):
    logger.info(f'{book_url} : START')
    folder_name, page_url_template, filename_template = analyze_book_url(book_url)

    local_folder = os.path.join(OUTPUT_IMAGE_FOLDER, folder_name)
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    successed_page_counter = 0
    failed_page_counter = 0
    for i in range(1, MAX_PAGE_NO):

        successed = False
        for ext_name in EXT_NAME_LIST:
            page_url = page_url_template.replace('{page_no}', str(i)).replace('{ext_name}', ext_name)
            local_file_name = filename_template.replace('{page_no}', str(i)).replace('{ext_name}', ext_name)
            local_file_path = os.path.join(local_folder, local_file_name)

            sts = download_single_file(page_url, local_file_path)
            if sts:
                successed = True
                break
            else:
                continue

        if successed:
            successed_page_counter = successed_page_counter + 1
        else:
            failed_page_counter = failed_page_counter + 1

        is_end_of_book = failed_page_counter > 3
        if is_end_of_book:
            break

    logger.info(f'{book_url} : {successed_page_counter}/{failed_page_counter}')
    return

def main():
    book_url_list = read_book_url_list()
    logger.info(f'{len(book_url_list)} : START')

    if MULTI_THREAD_MODE:
        thread_list = []
        for book_url in book_url_list:
            thread = threading.Thread(target=download_book, args=([book_url]))
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()
    else:
        for book_url in book_url_list:
            download_book(book_url)


    logger.info(f'{len(book_url_list)} : END')
    return

# ##############################
# entrance
# ##############################

if __name__ == '__main__':
    init_logger()
    main()
