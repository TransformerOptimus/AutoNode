from PIL import Image
import math


class BoundingBoxHelper:

    def __init__(self):
        pass

    def find_bboxs_in_an_area(self, clickable_objects, click_location, screenshot_path, area=0.40):
        """
        Function to get all the bounding boxes in an area

        Args:
            :param clickable_objects: List of clickable_objects with bounding boxes
            :param click_location: = [x,y] (Default None)
            :param screenshot_path (str): Path to the screenshot

        Returns:
            bbox_clickable (list) : Clickable Bounding Box coordinates [x1,y1,x2,y2] in a specified area

        """
        filtered_bboxs = []
        for obj in clickable_objects:
            x1, y1 = self.get_middle_of_a_bbox(obj['bbox'], screenshot_path=screenshot_path)
            distance = self.euclidean_distance(click_location, [x1, y1])
            if distance <= area:
                filtered_bboxs.append([obj, distance])
        return filtered_bboxs

    def get_middle_of_a_bbox(self, bbox, screenshot_path, percentage_x=0.3, percentage_y=0.5):
        """Function to get the middle point of a bounding box

        Args:
            bbox (List): bounding box of the text from easyocr
            percentage_x (int): Percentage of point taken while taking the mid-point for x-axis
            percentage_y (int): Percentage of point taken while taking the mid-point for y-axis
            screenshot_path (str): Path to the screenshot

        Returns:
            List: middle point of the bounding box
        """
        img = Image.open(screenshot_path)
        width, height = img.size

        x1, y1, x2, y2 = bbox
        x = x1 + abs(x2 - x1) * percentage_x
        y = y1 + abs(y2 - y1) * percentage_y

        x = x / width
        y = y / height

        return [x, y]

    def euclidean_distance(self, point1, point2):
        """Calculate the Euclidean distance between two points in a 2D space.

        Parameters:
        - point1: Tuple representing the coordinates of the first point (x1, y1).
        - point2: Tuple representing the coordinates of the second point (x2, y2).

        Returns:
        - The Euclidean distance between the two points.
        """

        x1, y1 = point1
        x2, y2 = point2

        distance = float(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        return distance

    def which_bounding_box(self, clickable_objects_, click_location_, screenshot_path) -> [int]:
        """Returns the index of the bounding box in which the point (x,y) lies

        Args:
            clickable_objects_ (list): List of clickable_objects with bounding boxes
            click_location_ (List): [x,y] Click Location
            screenshot_path (str): Path to the screenshot
        Returns:
            int: index of the bounding box in which the point (x,y) lies
        """

        x, y = click_location_
        img = Image.open(screenshot_path)
        width, height = img.size
        bboxes = []
        for obj_id, obj in enumerate(clickable_objects_):
            x1, y1, x2, y2 = obj[0]['bbox']  # TODO: has to be changed
            x1_ = x1 / width
            x2_ = x2 / width
            y1_ = y1 / height
            y2_ = y2 / height

            if x1_ <= x <= x2_ and y1_ <= y <= y2_:
                bboxes.append(obj_id)
        if bboxes:
            bboxes.sort(reverse=True)
        return bboxes

