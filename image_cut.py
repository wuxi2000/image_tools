import os
import img2pdf
from PIL import Image
from PIL import ImageFilter
import PyPDF2

FOLDER_BASE = 'xxxxxxxxxxxxxxxxxxxxxx' # TODO
FOLDER_ORIGINAL_PNG = os.path.join(FOLDER_BASE, '1.original_png')
FOLDER_RENAMED_PNG = os.path.join(FOLDER_BASE, '2.renamed_png')
FOLDER_CUTTED_PNG = os.path.join(FOLDER_BASE, '3.cutted_png')
FOLDER_GRAYED_PNG = os.path.join(FOLDER_BASE, '4.grayed_png')
FOLDER_SINGLE_PDF = os.path.join(FOLDER_BASE, '5.single_pdf')
FOLDER_MERGED_PDF = os.path.join(FOLDER_BASE, '6.merged_pdf')

################ ################ ################ 
# step 1 : file name format
# {FOLDER_ORIGINAL_PNG}/スクリーンショット (3).png -> {FOLDER_RENAMED_PNG}/img_1.png
################ ################ ################ 
def changeImageNames():
    files = os.listdir(FOLDER_ORIGINAL_PNG)
    for filename in files:
        if not filename.endswith('.png'):
            continue

        renamedFilename = filename.replace('(', '').replace(')', '').replace(' ', '').replace('www.examtopics.com_exams_microsoft_az-104_view_', 'img_')

        oldFullpath = os.path.join(FOLDER_ORIGINAL_PNG, filename)
        renamedFullPath = os.path.join(FOLDER_RENAMED_PNG, renamedFilename)
        os.rename(oldFullpath, renamedFullPath)

        print(f'{filename} -> {renamedFullPath}')

################ ################ ################ 
# step 1.5 : file name format again
# {FOLDER_RENAMED_PNG}/img_1.png -> {FOLDER_RENAMED_PNG}/img_001.png
################ ################ ################ 
def changeImageNamesAgain():
    files = os.listdir(FOLDER_RENAMED_PNG)
    for filename in files:
        if not filename.endswith('.png'):
            continue
        if not filename.startswith('img_'):
            continue

        fileno = filename.split('.')[0].split('_')[1]
        if len(fileno) == 1:
            fileno = '00' + fileno
        elif len(fileno) == 2:
            fileno = '0' + fileno
        else:
            pass

        renamedFilename = 'renamed_' + fileno + '.png'

        oldFullpath = os.path.join(FOLDER_RENAMED_PNG, filename)
        renamedFullPath = os.path.join(FOLDER_RENAMED_PNG, renamedFilename)
        os.rename(oldFullpath, renamedFullPath)

        print(f'{filename} -> {renamedFullPath}')

################ ################ ################ 
# step 2 : trim 
# {FOLDER_RENAMED_PNG}/img_001.png -> {FOLDER_CUTTED_PNG}/new_001.png
################ ################ ################ 
def trim():
    files = os.listdir(FOLDER_RENAMED_PNG)
    for filename in files:
        if not filename.endswith('.png'):
            continue
        if not filename.startswith('renamed_'):
            continue

        img = Image.open(os.path.join(FOLDER_RENAMED_PNG, filename))
        
        # (left, upper, right, lower)
        # cuttedImg = img[42 : 1077, 529: 1365] <- for cv2
        cuttedImg = img.crop((529, 42, 1365, 1077))

        cuttedFilename = filename.replace('renamed_', 'cutted_')
        cuttedImg.save(os.path.join(FOLDER_CUTTED_PNG, cuttedFilename), quality=100)

        print(f'{filename} -> {cuttedFilename}')

################ ################ ################ 
# step 3 : color to gray & sharpen
# {FOLDER_CUTTED_PNG}/new_001.png -> {FOLDER_GRAYED_PNG}/gray_001.png
################ ################ ################ 
def grayAndSharpen():
    files = os.listdir(FOLDER_CUTTED_PNG)
    for filename in files:
        if not filename.endswith('.png'):
            continue

        # TODO
        # if not filename.startswith('cutted_'):
        if not filename.startswith('new_'):
            continue

        # TODO
        # grayedFilename = filename.replace('cutted_', 'gray_')
        grayedFilename = filename.replace('new_', 'gray_')

        img = Image.open(os.path.join(FOLDER_CUTTED_PNG, filename))
        sharpenImg = img.filter(ImageFilter.SHARPEN)
        # sharpenImg = sharpenImg.filter(ImageFilter.EDGE_ENHANCE)
        grayedImg = sharpenImg.convert("L")
        grayedImg.save(os.path.join(FOLDER_GRAYED_PNG, grayedFilename))

        print(f'{filename} -> {grayedFilename}')

################ ################ ################ 
# step 4 : convert to pdf
# {FOLDER_GRAYED_PNG}/gray_001.png -> {FOLDER_SINGLE_PDF}/gray_001.png
################ ################ ################ 
def coverntToPdf():
    files = os.listdir(FOLDER_GRAYED_PNG)
    for filename in files:
        if not filename.endswith('.png'):
            continue
        if not filename.startswith('gray_'):
            continue

        img = Image.open(os.path.join(FOLDER_GRAYED_PNG, filename))
        pdf = img2pdf.convert(os.path.join(FOLDER_GRAYED_PNG, filename))
        pdfFilename = filename.replace('.png', '.pdf')
        pdfFile = open(os.path.join(FOLDER_SINGLE_PDF, pdfFilename), 'wb')
        pdfFile.write(pdf)
        img.close()
        pdfFile.close()

        print(f'{filename} -> {pdfFilename}')

################ ################ ################ 
# step 5 : merge pdf
# {FOLDER_SINGLE_PDF}/gray_001.png -> {OUTPUT_DIR}/mockx.pdf
################ ################ ################ 
def mergePdf():

    maxPageOfBook = 60

    pdfFiles = []
    files = os.listdir(FOLDER_SINGLE_PDF)
    for line in files:
        if line.endswith('.pdf'):
            pdfFiles.append(line)

    pageIndex = 0
    bookIndex = 0

    for inputPdfFile in pdfFiles:
        inputPdfReader = PyPDF2.PdfFileReader(os.path.join(FOLDER_SINGLE_PDF, inputPdfFile))
        for i in range(inputPdfReader.getNumPages()):

            if pageIndex % maxPageOfBook == 0:
                bookIndex += 1
                print(f'start new book {bookIndex}')
                mergedPdfFilename = os.path.join(FOLDER_MERGED_PDF, f'mock{bookIndex}.pdf')
                mergedPdfFile = open(mergedPdfFilename, "wb")
                pdfWriter = PyPDF2.PdfFileWriter()

            pageIndex += 1
            print(f'    add page to book {bookIndex} / {pageIndex}')
            assert pdfWriter is not None
            pdfWriter.addPage(inputPdfReader.getPage(i))

            if pageIndex % maxPageOfBook == 0:
                assert pdfWriter is not None
                print(f'end book {bookIndex}')
                mergedPdfFile = open(mergedPdfFilename, "wb")
                pdfWriter.write(mergedPdfFile)
                mergedPdfFile.close()
            else:
                pass

    print(f'end book {bookIndex}')
    mergedPdfFile = open(mergedPdfFilename, "wb")
    assert pdfWriter is not None
    pdfWriter.write(mergedPdfFile)
    mergedPdfFile.close()

################ ################ ################ 
# main
################ ################ ################ 

def main():
    # changeImageNames()
    # changeImageNamesAgain()
    trim()
    # grayAndSharpen()
    # coverntToPdf()
    # mergePdf()

################ ################ ################ 
# entrance
################ ################ ################ 
if __name__ == "__main__":
    main()

