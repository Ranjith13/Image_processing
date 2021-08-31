import fitz # PyMuPDF
import io, os, glob, re
from PIL import Image

# file path you want to extract images from
out_path = "output/path"
os.chdir("files/from/dir")
for files in glob.glob('*.pdf'):
    # print(files)
    # open the file
    pdf_file = fitz.open(files)

    # iterate over PDF pages
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()
        # print(image_list)
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(image_list, start=1):
            # print(img)
            # get the XREF of the image
            xref = img[0]

            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            # print(image_bytes)

            # get the image extension
            image_ext = base_image["ext"]

            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # print(image)

            # save it to local disk
            outpath = out_path + "outputImg\\" + files[:-4]
            # print(count)
            image.save(open(outpath + f"_P{page_index:04}.{image_ext}", "wb"))
            # image.save(open(f"image.{image_ext}", "wb"))
