from PIL import Image, ExifTags
#from exif import Image
import piexif
import os
import time
import sys
import cv2
import shutil


def write_index_file(main_filename, preview_name, path_name, current_path, alt_text):
    text = f'''<div class="media {path_name}">
<a href="images/fulls/{main_filename}"><img src="images/thumbs/{preview_name}" alt="{alt_text}" title="{path_name}" /></a>
</div>
\n'''
    with open(os.path.join(current_path, 'output')  + "_main.txt", 'a') as f:
        f.write(text)



def write_galery_file(main_filename, preview_name, path_name, current_path,alt_text):
    text = f'''<div class="media all {path_name}">
<a href="images/fulls/{main_filename}"><img src="images/thumbs/{preview_name}" alt="{alt_text}" title="{path_name}" /></a>
</div>
\n'''
    with open(os.path.join(current_path, 'output') + "_gallery.txt", 'a') as f:
        f.write(text)


def change_size(filename):
   
    image = cv2.imread(filename)
    height , width , layers =  image.shape
    multiplicator = 1/6
    new_height = 200 # int(height * multiplicator)
    new_width = 300 # int(width * multiplicator)
    resized_image = cv2.resize(image, (new_width,new_height))
    return resized_image


def extract_alt_text (filename):
    image = Image.open(filename)
    exif_data = image._getexif()
    exif = {
    ExifTags.TAGS[k]: v
    for k, v in image._getexif().items()
    if k in ExifTags.TAGS
    }

    alt_text = exif['XPKeywords'].decode('utf-16')
    return alt_text

def main():
    webste_subdir = "site-files"
    website_image_dir = "images"
    website_path =  os.path.join(os.path.abspath(os.path.join(__file__ ,"..")),webste_subdir, website_image_dir)
    print(website_path)
    file_counter = 0
    current_path = os.getcwd()
    site = "site"
    new_path = os.path.join(current_path, "site")
    os.chdir(new_path)
    all_dirs = os.listdir()
    print(all_dirs)
    for path in all_dirs:

            os.chdir(os.path.join(new_path, path))
            new_path1 = os.chdir(os.path.join(new_path, path))
            files = [f for f in os.listdir(new_path1) if os.path.isfile(f) and f.endswith('.jpg')]
            print(files)
            for filename in files:
                print('filename:', filename)
                file_counter += 1
                
                main_file_name = str(file_counter) + ".jpg"
                os.rename(filename, main_file_name)
                try:
                    alt_text = extract_alt_text(main_file_name)
                except Exception as err:
                    alt_text = ""
                    print(err.args)
                alt_text = " ".join(path.split(" ")[1:]) + ";" + alt_text
                caption =  " ".join(path.split(" ")[1:])
                alt_text = " ".join(alt_text.split(";"))
                print(alt_text)
                time.sleep(29)
                try:
 
                    preview_image = change_size(main_file_name)
                except Exception as err:
                    preview_image = ""
                    print(err.args)
                preview_file_name = "preview_"+ str(file_counter) + "_.jpg"
                cv2.imwrite(preview_file_name, preview_image)
                
                
                print(1)
                write_index_file(main_file_name,preview_file_name, caption, current_path,alt_text)
                write_galery_file(main_file_name,preview_file_name, caption, current_path,alt_text)
                shutil.move(main_file_name, os.path.join(website_path,"fulls") )
                shutil.move(preview_file_name, os.path.join(website_path,"thumbs") )
            
                
                
'''   
get list folders
get list files jpg

change file size 300-200

rename files
move files
create text files
'''

if __name__ == "__main__":
    main()


print(os.getcwd())
print(os.listdir())
