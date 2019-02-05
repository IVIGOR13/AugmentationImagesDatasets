import random
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw


class TreatmentImages:
    def __init__(self, dir, name, treat, index_transform):
        self.directory_in = dir
        self.name_in = name[:len(name)-4]
        self.image = Image.open(self.directory_in + '/' + name)
        self.width = self.image.size[0]
        self.height = self.image.size[1]

        self.directory_out = dir + '/out/'

        if not os.path.exists(self.directory_out):
            os.makedirs(self.directory_out)

        if index_transform == 0:
            for i in range(len(treat)):
                if treat[i][0] == 1:
                    img = self.transform_black_white(int(treat[i][1]), self.image.copy())
                    path = self.directory_out + self.name_in + '_black-white'
                    img.save((path + '.png'), "PNG")

                if treat[i][0] == 2:
                    img = self.transform_noises(int(treat[i][1]), self.image.copy())
                    path = self.directory_out + self.name_in + '_noises'
                    img.save((path + '.png'), "PNG")

                if treat[i][0] == 3:
                    img = self.transform_turn(int(treat[i][1]), self.directory_in + '/' + name)
                    cv2.imwrite(self.directory_out + self.name_in + '_turn_plus' + ".png", img[0])
                    cv2.imwrite(self.directory_out + self.name_in + '_turn_minus' + ".png", img[1])

                if treat[i][0] == 4:
                    img = self.transform_gray_shades(self.image.copy())
                    path = self.directory_out + self.name_in + '_gray_shades'
                    img.save((path + '.png'), "PNG")

                if treat[i][0] == 5:
                    img = self.transform_strip(int(treat[i][1]), self.image.copy())
                    path = self.directory_out + self.name_in + '_strip'
                    img.save((path + '.png'), "PNG")

                if treat[i][0] == 6:
                    img = self.transform_glare(int(treat[i][1]), self.image.copy())
                    path = self.directory_out + self.name_in + '_glare'
                    img.save((path + '.png'), "PNG")

                if treat[i][0] == 7:
                    img = self.transform_blur(self.directory_in + '/' + name)
                    cv2.imwrite(self.directory_out + self.name_in + '_blur' + ".png", img)

                if treat[i][0] == 8:
                    img = self.transform_compress(float(treat[i][1]), self.image.copy())
                    path = self.directory_out + self.name_in + '_compress'
                    img.save((path + '.png'), "PNG")

                if treat[i][0] == 9:
                    img = self.transform_stretch(float(treat[i][1]), self.image.copy())
                    path = self.directory_out + self.name_in + '_stretch'
                    img.save((path + '.png'), "PNG")


        if index_transform == 1:
            path_combo = self.name_combo(self.directory_out + self.name_in + '_combo.png')
            image_combo = self.image.copy()
            image_combo.save(path_combo, "PNG")

            for i in range(len(treat)):

                if treat[i][0] == 1:
                    img = self.transform_black_white(treat[i][1], image_combo)
                    img.save(path_combo, "PNG")

                if treat[i][0] == 2:
                    img = self.transform_noises(treat[i][1], image_combo)
                    img.save(path_combo, "PNG")

                if treat[i][0] == 3:
                    img = self.transform_turn(treat[i][1], path_combo)
                    cv2.imwrite(path_combo, img[0])

                if treat[i][0] == 4:
                    img = self.transform_gray_shades(image_combo)
                    img.save(path_combo, "PNG")

                if treat[i][0] == 5:
                    img = self.transform_strip(treat[i][1], image_combo)
                    img.save(path_combo, "PNG")

                if treat[i][0] == 6:
                    img = self.transform_glare(treat[i][1], image_combo)
                    img.save(path_combo, "PNG")

                if treat[i][0] == 7:
                    img = self.transform_blur(path_combo)
                    cv2.imwrite(path_combo, img)

                if treat[i][0] == 8:
                    img = self.transform_compress(treat[i][1], image_combo)
                    img.save(path_combo, "PNG")

                if treat[i][0] == 9:
                    img = self.transform_stretch(treat[i][1], image_combo)
                    img.save(path_combo, "PNG")

                image_combo = Image.open(path_combo)
            image_combo.save(path_combo, "PNG")

    def name_combo(self, path):
        expansion = path[len(path)-4:]
        path = path[:len(path)-4]
        p = path.split('/')
        path = p[:len(p)-1]
        path = '/'.join(path) + "/"
        name = p[len(p)-1]

        files = os.listdir(path)
        images = [x for x in files if x.endswith(expansion)]
        x = 0
        for i in images:
            if i.startswith(name):
                x += 1
        if not x == 0:
            return path + name + '_' + str(x) + expansion
        else:
            return path + name + expansion

    def transform_black_white(self, factor, img):
        pix = img.load()
        draw = ImageDraw.Draw(img)

        for i in range(self.width):
            for j in range(self.height):
                p = pix[i, j]
                if type(p) != int:
                    S = p[0] + p[1] + p[2]
                    if (S >= (((255 + factor) // 2) * 3)):
                        draw.point((i, j), (255, 255, 255))
                    else:
                        draw.point((i, j), (0, 0, 0))
                else:
                    if (p >= (255 + factor) // 2):
                        draw.point((i, j), 255)
                    else:
                        draw.point((i, j), 0)
        return img

    def transform_noises(self, factor, img):
        pix = img.load()
        draw = ImageDraw.Draw(img)
        for i in range(self.width):
            for j in range(self.height):
                rand = random.randint(-factor, factor)
                p = pix[i, j]
                if type(p) != int:
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
                else:
                    if (p < 0): draw.point((i, j), 0)
                    if (p > 255): draw.point((i, j), 255)

        return img

    def transform_turn(self, factor, path):
        def turn_image(image, angle):
            image_size = (self.width, self.height)
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

        image = cv2.imread(path)

        image_turned1 = turn_image(image, factor)
        image = cv2.imread(self.directory_in + '/' + self.name_in + '.png')
        image_turned2 = turn_image(image, -factor)
        return [image_turned1, image_turned2]

    def transform_gray_shades(self, img):
        pix = img.load()
        draw = ImageDraw.Draw(img)

        if type(pix[0, 0]) != int:
            for i in range(self.width):
                for j in range(self.height):
                    S = (pix[i, j][0] + pix[i, j][1] + pix[i, j][2]) // 3
                    draw.point((i, j), (S, S, S))
        return img

    def transform_strip(self, factor, img):
        pix = img.load()
        draw = ImageDraw.Draw(img)

        rand = random.randint(0, 100)
        tin = round(self.height * rand / 100)
        tout = round(self.height * random.randint(0, 100) / 100)

        if factor > 0:
            if type(pix[0, 0]) != int:
                for i in range(self.width):
                    for j in range(self.height):
                        ti = round(tin)
                        if j > ti and j < ti+self.height // 8:
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
            else:
                for i in range(self.width):
                    for j in range(self.height):
                        ti = round(tin)
                        if j > ti and j < ti+self.height // 8:
                            if (pix[i, j] > 215):
                                a = 255
                            else:
                                a = pix[i, j] + 40
                            draw.point((i, j), a)

                    if tin>tout:
                        tin = tin + (abs(self.height*rand / 100 - tout) / self.width)
                    else:
                        tin = tin - (abs(self.height * rand / 100 - tout) / self.width)

        else:
            if type(pix[0, 0]) != int:
                for i in range(self.width):
                    for j in range(self.height):
                        ti = round(tin)
                        if j > ti and j < ti + self.height // 8:
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
            else:
                for i in range(self.width):
                    for j in range(self.height):
                        ti = round(tin)
                        if j > ti and j < ti + self.height // 8:
                            if (pix[i, j] < -factor):
                                a = 0
                            else:
                                a = pix[i, j] + factor

                            draw.point((i, j), a)
                    if tin > tout:
                        tin = tin + (abs(self.height * rand / 100 - tout) / self.width)
                    else:
                        tin = tin - (abs(self.height * rand / 100 - tout) / self.width)

        return img

    def transform_glare(self, factor, img):
        pix = img.load()
        draw = ImageDraw.Draw(img)

        radius = self.height // 6
        Ox = random.randint(0, 100) / 100 * self.width
        Oy = random.randint(0, 100) / 100 * self.height

        if factor > 0:
            if type(pix[0, 0]) != int:
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
                            if (pix[i, j] > (255 - factor)):
                                a = 255
                            else:
                                a = pix[i, j] + factor

                            draw.point((i, j), a)

        else:
            if type(pix[0, 0]) != int:
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
            else:
                for i in range(self.width):
                    for j in range(self.height):
                        if (i - Ox) ** 2 + (j - Oy) ** 2 <= radius ** 2:
                            if (pix[i, j] > (0 - factor)):
                                a = 0
                            else:
                                a = pix[i, j] + factor

                            draw.point((i, j), a)

        return img

    def transform_blur(self, path):
        return  cv2.GaussianBlur(cv2.imread(path), (5,5), 0)

    def transform_compress(self, factor, img):
        img = img.resize((round(factor*self.width), self.height))
        return img

    def transform_stretch(self, factor, img):
        img = img.resize((self.width, round(factor*self.height)))
        return img
