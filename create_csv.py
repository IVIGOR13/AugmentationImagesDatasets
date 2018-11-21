#
#   Images are read from all directories in the folder in which the script resides.
#   The directory name is an image label.
#
import os
import glob
import pandas as pd
from PIL import Image

def img_to_csv(dirs_in):
    xml_list = []
    for dir_in in dirs_in:
        for image_file in glob.glob(dir_in + '/*.png'):
            image = Image.open(image_file)
            width = image.size[0]
            height = image.size[1]

            a = dir_in.split('\\')
            label = a[len(a)-1]

            b = image_file.split('\\')
            filename = b[len(b)-1]

            value = (filename,
                     width,
                     height,
                     label,
                     0,
                     0,
                     width,
                     height
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    dirs = [x[0] for x in os.walk(os.path.join(os.getcwd()))]
    dirs_in = dirs[1:]
    xml_df = img_to_csv(dirs_in)
    xml_df.to_csv('data_labels.csv', index=None)
    print('Successfully create csv file.')

main()
