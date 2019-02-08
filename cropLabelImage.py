#
#  Crops images from .xml files created LabelImg
#
#  Replace {NameDir} with the name of the image folder
#

import os
import glob
from PIL import Image
import xml.etree.ElementTree as ET

def crop(path):
    i = 0
    directoryImages = '/' + {NameDir} + '/'
    for xml_file in glob.glob(path + directoryImages + '*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            i += 1
            value = [root.find('filename').text,
                member[0].text,
                int(member[4][0].text),
                int(member[4][1].text),
                int(member[4][2].text),
                int(member[4][3].text)
                ]

            if not os.path.exists(path + directoryImages + value[1]):
                os.makedirs(path + directoryImages + value[1])

            img = Image.open(path + directoryImages + value[0])
            img = img.crop((value[2], value[3], value[4], value[5]))
            img.save(path + directoryImages + value[1] + '/image_' + value[1] + '_' + str(i) + '.png')

    print('done ' + str(i) + ' labels')

def main():
    image_path = os.path.join(os.getcwd())
    crop(image_path)
    print('Successfully crop.')

main()
