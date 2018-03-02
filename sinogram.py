import cv2
import numpy as np

from filter import filter_projection


class Sinogram:

    def __init__(self, image_name, section=None, number_of_emitters=None, angle=1, experimental=False):
        self._image = cv2.imread(image_name, 0)
        self.width, self.height = np.shape(self._image)
        if self.width != self.height:
            raise NotSquare
        self._SECTION = section if section is not None else self._image.shape[0]
        self._NUMBER_OF_EMITTERS = number_of_emitters if number_of_emitters is not None else self._image.shape[0]
        self.ANGLES = np.arange(0, 180, angle)
        self._OFFSETS = np.linspace(-self._SECTION / 2, self._SECTION / 2, self._NUMBER_OF_EMITTERS)
        self._radius = self.width / 2
        self._experimental = experimental
        self.last_sinogram = None
        self.output_image = np.zeros((self.width, self.height))
        self._lines = []
        self.filtered_sinogram = None
        self.iteration = 0

    def _create_line(self, points):
        x1, y1, x2, y2 = int(points[0]), int(points[1]), int(points[2]), \
                         int(points[3])
        result = []

        kx = 1 if x1 < x2 else -1
        ky = 1 if y1 < y2 else -1

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        result.append((x1, y1))
        if dx > dy:
            e = dx / 2
            for i in range(int(dx)):
                x1 += kx
                e -= dy
                if e < 0:
                    y1 += ky
                    e += dx
                result.append((x1, y1))
        else:
            e = dy / 2
            for i in range(int(dy)):
                y1 += ky
                e -= dx
                if e < 0:
                    x1 += kx
                    e += dy
                result.append((x1, y1))

        radius_pow_2 = self._radius ** 2
        return [(x, y) for x, y in result if ((x - self._radius) ** 2 + (y - self._radius) ** 2) <= radius_pow_2]

    def _get_positions(self, angle, offset):
        x1, y1 = self._radius * np.cos(angle), self._radius * np.sin(angle)
        x2, y2 = -x1, -y1
        xv, yv = offset * np.cos(angle + np.pi / 2), offset * np.sin(angle + np.pi / 2)
        x1 += xv + self._radius
        y1 += yv + self._radius
        x2 += xv + self._radius
        y2 += yv + self._radius
        return [x1, y1, x2, y2]

    def _calculate_single_line(self, line):
        result = []
        for x, y in line:
            if 0 <= x < self.width and 0 <= y < self.height:
                result.append(self._image[x, y])

        if self._experimental:
            normalize_sum = sum(result) / (255 * len(line)) if len(line) > 0 else 0
            return np.exp(-normalize_sum)
        else:
            return np.array(result).mean() if len(result) > 0 else 0

    def generate(self):

        if self._image is None:
            raise NoImage

        sin = []

        self._lines = []
        for angle in self.ANGLES:
            angle = np.deg2rad(angle)
            sin_row = []
            lines_row = []
            for offset in self._OFFSETS:
                positions = self._get_positions(angle, offset)
                line = self._create_line(positions)
                color = self._calculate_single_line(line)
                sin_row.append(color)
                lines_row.append(line)
            sin.append(sin_row)
            self._lines.append(lines_row)

        if self._experimental:
            max_value = np.max(sin)
            min_value = np.min(sin)
            factor = 256 / (max_value - min_value)
            sin -= min_value
            sin *= factor
            sin = np.full(np.shape(sin), 255) - sin

        self.last_sinogram = np.array(sin)
        return np.array(sin)

    def save_as_image(self, name="output.png"):
        if self.last_sinogram is None:
            sin = self.generate()
        else:
            sin = self.last_sinogram.copy()
        cv2.imwrite(name, sin)

    def reverse(self, output_name="output_reverse.png"):
        if self.last_sinogram is None:
            self.generate()
        self.output_image = np.zeros((self.width, self.height))

        filtered_sinogram = filter_projection(self.last_sinogram)
        for i in range(filtered_sinogram.shape[0]):
            for j in range(filtered_sinogram.shape[1]):
                for x, y in self._lines[i][j]:
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.output_image[x, y] += filtered_sinogram[i][j]

        cv2.imwrite(output_name, self.output_image)

    def prepare_animation(self):
        if self.last_sinogram is None:
            self.generate()
        self.output_image = np.zeros((self.width, self.height))
        self.filtered_sinogram = filter_projection(self.last_sinogram)
        self.iteration = 0

    def animation_reverse(self):
        if self.iteration < len(self.ANGLES):
            for j in range(self.filtered_sinogram.shape[1]):
                for x, y in self._lines[self.iteration][j]:
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.output_image[x, y] += self.filtered_sinogram[self.iteration][j]
            self.iteration += 1
            return True
        else:
            return False

    def calculate_mse(self):
        return np.sqrt(((self._image - self.output_image) ** 2).mean(axis=None))


class NotSquare(Exception):
    pass


class NoImage(Exception):
    pass
