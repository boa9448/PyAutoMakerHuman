import os

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


def cv2_imread(filename : str, flags : int = cv2.IMREAD_COLOR) -> np.ndarray:
    raw = np.fromfile(filename, np.uint8)
    img = cv2.imdecode(raw, flags)

    return img


def cv2_imwrite(filename : str, img : np.ndarray, params : list = None):
    ext = os.path.splitext(filename)[1]
    ret, raw_img = cv2.imencode(ext, img, params)
    if ret:
        with open(filename, "w+b") as f:
            raw_img.tofile(f)


def cv2_putText(img, text, org, fontScale, color, thickness=..., lineType=..., bottomLeftOrigin=..., center=...):
    fontpath = "fonts/gulim.ttc"
    font = ImageFont.truetype(fontpath, int(10 * fontScale))
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    if center is True:
        W, H, _ = img.shape
        w, h = draw.textsize(text, font = font)
        org = (W - w) / 2, (H - h) / 2

    draw.text(org, text, font=font, fill=color, stroke_width=thickness)

    return np.array(img_pil)


if __name__ == "__main__":
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    img = cv2_putText(img, "test", (10, 10), 0, (255, 255, 0))
    cv2.imshow("view", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    cv2_imwrite("한글.jpg", img)