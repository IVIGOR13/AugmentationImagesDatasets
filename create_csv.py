import os
import glob
import pandas as pd
from PIL import Image 

def xml_to_csv(directorys):
    dir_in = directorys[1]
    for directory in dir_in:
        xml_list = []
        for image_file in glob.glob(directory + '/*.png'):
            image = Image.open(image_file)
            width = image.size[0]
            height = image.size[1]

            a = directory.split('/')
            label = a[len(a)-1]

            b = image_file.split('/')
            filename = b[len(b)-1]

            value = (filename[:len(filename)-4],
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
    directorys = [x[0] for x in os.walk(os.path.join(os.getcwd()))]
    xml_df = xml_to_csv(directorys)
    xml_df.to_csv('data_labels.csv', index=None)
    print('Successfully create csv file.')

main()
