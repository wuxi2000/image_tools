import requests
import threading
import os

BOOK_ID_LIST = [
    '2000581', '1985334', '1563958'
]

# ##############################
# functions

def makeRemoteUrl(bookId, seq):
    urlTemplate = 'https://i.nhentai.net/galleries/{bookId}/{seq}.jpg'
    urlTemplate.format(bookId=bookId, seq=seq)
    return urlTemplate

def downloadImage(url, localPath):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f'error:{response.status_code}, {url}')
            return False

        image = response.content
        with open(localPath, "wb") as f:
            f.write(image)

        return True

    except Exception as e:
        print(f'error in download {url}, {e}')
        return False

def downloadFolder(bookId, localDir):
    print(f'{bookId} download start {localDir}')

    dir = os.path.join(localDir, bookId)
    if not os.path.exists(dir):
        os.makedirs(dir)

    counter = 0
    errorCounter = 0
    for i in range(1, 200):
        localFilename = os.path.join(localDir, bookId, f'{str(i)}.jpg')
        url = makeRemoteUrl(bookId, str(i))
        sts = downloadImage(url, localFilename)
        if not sts:
            errorCounter += 1
            if errorCounter > 3:
                break

        counter += 1

    print(f'{bookId} download finish, pages={counter}')
    return

def main():
    print(f'>>> start bookIds={len(BOOK_ID_LIST)}')

    localDir = os.path.join(os.getcwd(), 'data')
    for bookId in BOOK_ID_LIST:
        thread = threading.Thread(target=downloadFolder, args=(bookId, localDir))
        thread.start()
        thread.join()

    print('<<< finished')
    return


# ##############################
# entrance
if __name__ == '__main__':
    main()
