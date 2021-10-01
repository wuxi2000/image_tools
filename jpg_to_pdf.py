import os
import PyPDF2
from PIL import Image
import img2pdf

HOME_DIR = r'C:\Users\wuxi2\Documents\GitSandbox.temp\python\image_tools'

def jpg2pdf(jpgFilename, pdfFilename):
    img = Image.open(jpgFilename)
    pdf = img2pdf.convert(jpgFilename)
    pdfFile = open(pdfFilename, 'wb')
    pdfFile.write(pdf)
    img.close()
    pdfFile.close()

def mergepdfs(inputFilenameList, outputFilename):
    merger = PyPDF2.PdfFileMerger()
    for inputPdfFile in inputFilenameList:
        merger.append(inputPdfFile)
    merger.write(outputFilename)
    merger.close()

def jpg2pdfByFolder(folder):
    files = os.listdir(folder)
    pdfFileList = []
    for filename in files:
        if not filename.endswith('.jpg'):
            continue

        pdfFilename = filename.replace('.jpg', '.pdf')
        print(f'{filename} -> {pdfFilename}')
        jpg2pdf(os.path.join(folder, filename), os.path.join(folder, pdfFilename))
        pdfFileList.append(os.path.join(folder, pdfFilename))

    pdfFileList = sorted(pdfFileList, key=lambda x: int(os.path.basename(x).split('.')[0]))
    mergepdfs(pdfFileList, os.path.join(folder, f'{folder}.pdf'))

def main():
    imgDir = os.path.join(HOME_DIR, 'data/')
    allDirs = sorted(os.listdir(imgDir))
    dirs = [f for f in allDirs if os.path.isdir(os.path.join(imgDir, f))]
    for dir in dirs:
        jpg2pdfByFolder(os.path.join(imgDir, dir))

    return


# entrance
if __name__ == "__main__":
    main()
