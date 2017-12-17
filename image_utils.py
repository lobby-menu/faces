import cv2

def readRGBImage(imgPath):
    """
    Reads RGB image from the given part.
    :param imgPath:
    :return:
    """
    bgrImg = cv2.imread(imgPath)
    return None if bgrImg is None else cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

def snapRectangle(img, rect):
    """
    Given a image and a rectangle, returns only the rectangle part of that image.

    :param img: the image to snap the rectangle from.
    :param rect: the rectangle in the ((left, top), (width, height)) format.
    :return: the snapped and copied rectangle from the image.
    """
    imgHeight, imgWidth, _ = img.shape
    left, top = rect[0]
    width, height = rect[1]
    # TODO: Copy maybe unnecessary?
    return img[max(0, top):min(imgHeight, top+height), max(0, left):min(imgWidth, left+width)].copy()