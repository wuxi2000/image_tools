import requests
import threading
import os

BOOK_ID_LIST = [
    '1091289', '1339591',
]


# ##############################
# functions

def makeRemoteUrl(bookId, seq):
    urlTemplate = 'https://i.nhentai.net/galleries/{bookId}/{seq}.jpg'
    return urlTemplate.format(bookId=bookId, seq=seq)

def downloadImage(url, localPath):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return False

        image = response.content
        with open(localPath, "wb") as f:
            f.write(image)

        return True

    except Exception as e:
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
        if sts:
            counter += 1
        else:
            errorCounter += 1
            if errorCounter > 3:
                break

    print(f'{bookId} download finish, pages={counter}')
    return

def main():
    print(f'>>> start bookIds={len(BOOK_ID_LIST)}')

    threadList = []
    localDir = os.path.join(os.getcwd(), 'data')
    for bookId in BOOK_ID_LIST:
        thread = threading.Thread(target=downloadFolder, args=(bookId, localDir))
        thread.start()
        threadList.append(thread)

    for thread in threadList:
        thread.join()

    print('<<< finished')
    return


# ##############################
# entrance
if __name__ == '__main__':
    main()
