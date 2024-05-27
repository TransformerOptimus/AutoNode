def get_point(bbox):
    """
        Function to get the point of the text from the bounding box of easyocr

        Args:
            bbox (List): bounding box of the text from easyocr
    """
    x1, x2, x3, x4 = bbox
    x = (x1[0] + x2[0]) / 2
    y = (x1[1] + x4[1]) / 2
    return [x, y]


def convert_units_of_bbox(bbox, img):
    """
       Convert the units of the bounding box from easyocr to percentages from left and right

       ------------------
       |         |      |
       |         v      |
       |------->x%y%    |
       |                |
       |                |
       |                |
       |                |
       ------------------
   """
    width, height = img.size
    x1, x2, x3, x4 = bbox

    x1 = [x1[0] / width, x1[1] / height]
    x2 = [x2[0] / width, x2[1] / height]
    x3 = [x3[0] / width, x3[1] / height]
    x4 = [x4[0] / width, x4[1] / height]

    new_bbox = [x1, x2, x3, x4]

    return new_bbox