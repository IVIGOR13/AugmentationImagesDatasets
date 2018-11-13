import random
import os
import cv2
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

class TreatmentImages:
    def __init__(self, dir, name, treat):
        self.directory_in = dir
        self.name_in = name[:len(name)-4]

        self.image = Image.open(self.directory_in + '/' + name)
        self.width = self.image.size[0]
        self.height = self.image.size[1]

        self.directory_out = dir + '/out/'

        if not os.path.exists(self.directory_out):
            os.makedirs(self.directory_out)

        for i in range(len(treat)):
            print('0')
            if treat[i][0] == 1:
                self.transform_black_white(treat[i][1])
            if treat[i][0] == 2:
                self.transform_noises(treat[i][1])
            if treat[i][0] == 3:
                self.transform_turn(treat[i][1])
            if treat[i][0] == 4:
                self.transform_gray_shades()
            if treat[i][0] == 5:
                self.transform_strip(treat[i][1])
            if treat[i][0] == 6:
                self.transform_glare(treat[i][1])
            if treat[i][0] == 7:
                self.transform_blur()
            if treat[i][0] == 8:
                self.transform_compress_vertical(treat[i][1])
            if treat[i][0] == 9:
                self.transform_stretch_vertical(treat[i][1])

    def transform_black_white(self, factor):
        newIm = self.image.copy()
        pix = newIm.load()
        draw = ImageDraw.Draw(newIm)

        for i in range(self.width):
            for j in range(self.height):
                S = pix[i, j][0] + pix[i, j][1] + pix[i, j][2]
                if (S > (((255+factor) // 2) * 3)):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                draw.point((i, j), (a, b, c))

        newIm.save((self.directory_out + self.name_in + '_black-white' + '.jpg'), "JPEG")

    def transform_noises(self, factor):
        newIm = self.image.copy()
        pix = newIm.load()
        draw = ImageDraw.Draw(newIm)

        for i in range(self.width):
            for j in range(self.height):
                rand = random.randint(-factor, factor)
                a = pix[i, j][0] + rand
                b = pix[i, j][1] + rand
                c = pix[i, j][2] + rand
                if (a < 0): a = 0
                if (b < 0): b = 0
                if (c < 0): c = 0
                if (a > 255): a = 255
                if (b > 255): b = 255
                if (c > 255): c = 255
                draw.point((i, j), (a, b, c))

        newIm.save((self.directory_out + self.name_in + '_noises' + '.jpg'), "JPEG")

    def transform_turn(self, factor):
        def turn_image(image, angle):
            image_size = (image.shape[1], image.shape[0])
            image_center = tuple(np.array(image_size) / 2)

            rot_mat = np.vstack(
                [cv2.getRotationMatrix2D(image_center, angle, 1.0), [0, 0, 1]]
            )

            rot_mat_notranslate = np.matrix(rot_mat[0:2, 0:2])

            image_w2 = image_size[0] * 0.5
            image_h2 = image_size[1] * 0.5

            rotated_coords = [
                (np.array([-image_w2, image_h2]) * rot_mat_notranslate).A[0],
                (np.array([image_w2, image_h2]) * rot_mat_notranslate).A[0],
                (np.array([-image_w2, -image_h2]) * rot_mat_notranslate).A[0],
                (np.array([image_w2, -image_h2]) * rot_mat_notranslate).A[0]
            ]

            x_coords = [pt[0] for pt in rotated_coords]
            x_pos = [x for x in x_coords if x > 0]
            x_neg = [x for x in x_coords if x < 0]

            y_coords = [pt[1] for pt in rotated_coords]
            y_pos = [y for y in y_coords if y > 0]
            y_neg = [y for y in y_coords if y < 0]

            right_bound = max(x_pos)
            left_bound = min(x_neg)
            top_bound = max(y_pos)
            bot_bound = min(y_neg)

            new_w = int(abs(right_bound - left_bound))
            new_h = int(abs(top_bound - bot_bound))

            trans_mat = np.matrix([
                [1, 0, int(new_w * 0.5 - image_w2)],
                [0, 1, int(new_h * 0.5 - image_h2)],
                [0, 0, 1]
            ])

            affine_mat = (np.matrix(trans_mat) * np.matrix(rot_mat))[0:2, :]

            result = cv2.warpAffine(
                image,
                affine_mat,
                (new_w, new_h),
                flags=cv2.INTER_LINEAR
            )

            return result

        image = cv2.imread(self.directory_in + '/' + self.name_in + '.jpg')
        image_turned = turn_image(image, factor)
        cv2.imwrite(self.directory_out + self.name_in + '_turn10' + ".jpg", image_turned)

        image = cv2.imread(self.directory_in + '/' + self.name_in + '.jpg')
        image_turned = turn_image(image, -factor)
        cv2.imwrite(self.directory_out + self.name_in + '_turn-10' + ".jpg", image_turned)

    def transform_gray_shades(self):
        newIm = self.image.copy()
        pix = newIm.load()
        draw = ImageDraw.Draw(newIm)

        for i in range(self.width):
            for j in range(self.height):
                S = (pix[i, j][0] + pix[i, j][1] + pix[i, j][2]) // 3
                draw.point((i, j), (S, S, S))

        newIm.save((self.directory_out + self.name_in + '_gray-shades' + '.jpg'), "JPEG")

    def transform_strip(self, factor):
        for iter in range(5):
            newIm = self.image.copy()
            pix = newIm.load()
            draw = ImageDraw.Draw(newIm)

            rand = random.randint(0, 100)
            tin = round(self.height * rand / 100)
            tout = round(self.height * random.randint(0, 100) / 100)

            if factor > 0:
                for i in range(self.width):
                    for j in range(self.height):
                        ti = round(tin)
                        if j>ti and j<ti+self.height/8:
                            if (pix[i, j][0] > 215):
                                a = 255
                            else:
                                a = pix[i, j][0] + 40
                            if (pix[i, j][1] > 215):
                                b = 255
                            else:
                                b = pix[i, j][1] + 40
                            if (pix[i, j][2] > 215):
                                c = 255
                            else:
                                c = pix[i, j][2] + 40

                            draw.point((i, j), (a, b ,c))

                    if tin>tout:
                        tin = tin + (abs(self.height*rand / 100 - tout) / self.width)
                    else:
                        tin = tin - (abs(self.height * rand / 100 - tout) / self.width)

                newIm.save((self.directory_out + self.name_in + '_light_strip_' + str(iter) + '.jpg'), "JPEG")

            else:
                for i in range(self.width):
                    for j in range(self.height):
                        ti = round(tin)
                        if j > ti and j < ti + self.height / 8:
                            if (pix[i, j][0] < -factor):
                                a = 0
                            else:
                                a = pix[i, j][0] + factor
                            if (pix[i, j][1] < -factor):
                                b = 0
                            else:
                                b = pix[i, j][1] + factor
                            if (pix[i, j][2] < -factor):
                                c = 0
                            else:
                                c = pix[i, j][2] + factor
                            draw.point((i, j), (a, b, c))
                    if tin > tout:
                        tin = tin + (abs(self.height * rand / 100 - tout) / self.width)
                    else:
                        tin = tin - (abs(self.height * rand / 100 - tout) / self.width)

                newIm.save((self.directory_out + self.name_in + '_dark_strip_' + str(iter) + '.jpg'), "JPEG")

    def transform_glare(self, factor):
        for iter in range(5):
            newIm = self.image.copy()
            pix = newIm.load()
            draw = ImageDraw.Draw(newIm)

            radius = self.height // 6
            Ox = random.randint(0, 100) / 100 * self.width
            Oy = random.randint(0, 100) / 100 * self.height

            if factor > 0:
                for i in range(self.width):
                    for j in range(self.height):
                        if (i - Ox) ** 2 + (j - Oy) ** 2 <= radius ** 2:
                            if (pix[i, j][0] > (255 - factor)):
                                a = 255
                            else:
                                a = pix[i, j][0] + factor
                            if (pix[i, j][1] > (255 - factor)):
                                b = 255
                            else:
                                b = pix[i, j][1] + factor
                            if (pix[i, j][2] > (255 - factor)):
                                c = 255
                            else:
                                c = pix[i, j][2] + factor

                            draw.point((i, j), (a, b, c))
            else:
                for i in range(self.width):
                    for j in range(self.height):
                        if (i - Ox) ** 2 + (j - Oy) ** 2 <= radius ** 2:
                            if (pix[i, j][0] > (0 - factor)):
                                a = 0
                            else:
                                a = pix[i, j][0] + factor
                            if (pix[i, j][1] > (0 - factor)):
                                b = 0
                            else:
                                b = pix[i, j][1] + factor
                            if (pix[i, j][2] > (0 - factor)):
                                c = 0
                            else:
                                c = pix[i, j][2] + factor

                            draw.point((i, j), (a, b, c))

            newIm.save((self.directory_out + self.name_in + '_glare_' + str(iter) + '.jpg'), "JPEG")

    def transform_blur(self):
        newIm = self.image.copy().filter(ImageFilter.BLUR)
        newIm.save((self.directory_out + self.name_in + '_blur' + '.jpg'), "JPEG")

    def transform_compress_vertical(self, factor):
        newIm = self.image.copy()
        stretch_image = newIm.resize((round(factor*self.width), self.height))
        stretch_image.save((self.directory_out + self.name_in + '_compress' + '.jpg'), "JPEG")

    def transform_stretch_vertical(self, factor):
        newIm = self.image.copy()
        stretch_image = newIm.resize((self.width, round(factor*self.height)))
        stretch_image.save((self.directory_out + self.name_in + '_stretch' + '.jpg'), "JPEG")



