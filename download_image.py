import requests
import os

HOME_DIR = r'C:\Users\wuxi2\Documents\GitSandbox.temp\python\image_tools'

FOLDER_LIST = [
    '1967794'
]


# ##############################
# functions

def makeRemoteUrl(item, sequence):
    return item.format(sequence)

def downloadImageFile(url, localPath):
    dir = os.path.dirname(os.path.normpath(localPath))
    if not os.path.exists(dir):
        os.mkdir(dir)

    response = requests.get(url)
    if response.status_code != 200:
        print(f'error:{response.status_code}, {url}')
        return False

    image = response.content
    with open(localPath, "wb") as f:
        f.write(image)

    return True

def main():
    for folder in FOLDER_LIST:
        errorCounter = 0
        for i in range(1, 200):
            sequence = str(i)
            print(f'{folder},{sequence}')
            url = 'https://i.nhentai.net/galleries/{}/{}.jpg'.format(folder, sequence)
            localPath = f'{HOME_DIR}/data/{folder}/{sequence}.jpg'
            sts = downloadImageFile(url, localPath)
            if not sts:
                errorCounter += 1
                if errorCounter > 3:
                    break

    return


# ##############################
# entrance
if __name__ == '__main__':
    main()
