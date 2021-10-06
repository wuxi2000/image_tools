import os
import PyPDF2
from PIL import Image
import img2pdf
import math

PAGES_EACH_PDF = 20

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
    for i in range(1, math.ceil(len(pdfFileList) / PAGES_EACH_PDF) + 1):
        startIdx = (i - 1) * PAGES_EACH_PDF
        stopIdx = min(i * PAGES_EACH_PDF, len(pdfFileList))
        mergepdfs(pdfFileList[startIdx : stopIdx], os.path.join(folder, f'{folder}_{i}.pdf'))

def main():
    imgDir = os.path.join(os.getcwd(), 'data/')
    allDirs = sorted(os.listdir(imgDir))
    dirs = [f for f in allDirs if os.path.isdir(os.path.join(imgDir, f))]
    for dir in dirs:
        jpg2pdfByFolder(os.path.join(imgDir, dir))

    return


# entrance
if __name__ == "__main__":
    main()
