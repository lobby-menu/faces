import cv2


def read_rgb_image(img_path):
    """
    Reads RGB image from the given part.
    :param img_path:
    :return:
    """
    bgr_img = cv2.imread(img_path)
    return None if bgr_img is None else cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)


def rgb_to_png_bytes(rgb_image):
    image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    result, buf = cv2.imencode(".png", image)
    return bytearray(buf)


def snap_rectangle(img, rect):
    """
    Given a image and a rectangle, returns only the rectangle part of that image.

    :param img: the image to snap the rectangle from.
    :param rect: the rectangle in the ((left, top), (width, height)) format.
    :return: the snapped and copied rectangle from the image.
    """
    img_height, img_width, _ = img.shape
    left, top = rect[0]
    width, height = rect[1]
    # TODO: Copy maybe unnecessary?
    return img[max(0, top):min(img_height, top+height), max(0, left):min(img_width, left+width)].copy()
