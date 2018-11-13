import os
import treatment_images as ti

def be(directory, treat):
    files = os.listdir(directory)
    images = filter(lambda x: x.endswith('.jpg'), files)
    arrImg = []
    for i in images:
        arrImg.append(i)
        print(treat)
        print('found: ' + i)
        ti.TreatmentImages(directory, i, treat)
        print('done: ', i)

    print(arrImg)