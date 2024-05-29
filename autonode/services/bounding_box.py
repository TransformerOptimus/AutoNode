import jellyfish
from autonode.clients.ocr import OCRClient
from autonode.clients.yolo import YoloClient
from autonode.logger.logger import logger
from autonode.services.ocr import OCRService
from autonode.utils.helpers.bounding_box_helper import BoundingBoxHelper
from autonode.utils.helpers.cleanup_helper import CleanupHelper
from autonode.utils.helpers.image_helper import ImageHelper
from autonode.utils.helpers.string_helper import StringHelper


class BoundingBoxService:

    def __init__(self):
        self.yolo = YoloClient()
        self.ocr = OCRClient()

    def get_bounding_box(self, image_path: str, folder_path: str):
        CleanupHelper.clear_folders(folders=[folder_path])

        yolo_results = self.yolo.detect(image_path)
        cropped_images_data = ImageHelper().crop_images_parallel(image_path=image_path, results=yolo_results,
                                                                 folder_path=folder_path)
        ocr_results = OCRService().ocr_images_parallel(cropped_images_data)
        return ocr_results

    def get_location(self, node, clickable_objects, previous_node, screenshot_path,
                     threshold_for_element_search=0.7) -> list:
        """
        Function to get the location of the node
        Filtration is done on the basis of the distance and the similarity of the text
            score = 0.7*similarity + 0.3*(1 - distance)

        Args:
            :param screenshot_path:
            :param previous_node:
            :param threshold_for_element_search:
            :param node: Node of the tree
            :param clickable_objects: List of clickable_objects with bounding boxes

        Returns:
            location (list) : Location of the node [x,y]

        """
        filtered_bbox = BoundingBoxHelper().find_bboxs_in_an_area(clickable_objects, node.location, screenshot_path)
        filtered_bbox = self.filter_previous_node(filtered_bbox, previous_node, screenshot_path)

        highest_similarity_bbox = self.find_highest_similarity_bbox(filtered_bbox, node, screenshot_path)

        if highest_similarity_bbox[0] > threshold_for_element_search:
            return highest_similarity_bbox
        return [None, None]

    def filter_previous_node(self, filtered_bbox, previous_node, screenshot_path):
        if previous_node:
            obj_ids = BoundingBoxHelper().which_bounding_box(filtered_bbox, previous_node.location, screenshot_path)
            prev_element_name = previous_node.type_value if previous_node.type_value else previous_node.node_name
            if obj_ids:
                for obj_id in obj_ids:
                    if prev_element_name.strip() != "" and filtered_bbox[obj_id][0].get('ocr_result') and \
                            jellyfish.jaro_similarity(prev_element_name, filtered_bbox[obj_id][0]['ocr_result']) > 0.87:
                        logger.info(f"Deleting the previous clicked location: {filtered_bbox[obj_id]} ")
                        del filtered_bbox[obj_id]
        return filtered_bbox

    def find_highest_similarity_bbox(self, filtered_bbox, node, screenshot_path):
        highest_similarity_bbox = [-1, ""]
        curr_element_name = node.actionable_element_type if node.node_name.strip() == "" else node.node_name
        flag_element_type_match = node.node_name.strip() == ""

        for obj, distance in filtered_bbox:
            if flag_element_type_match:
                similarity = self.calculate_similarity(curr_element_name, obj['class'], distance)
            else:
                if obj['ocr_result'] in ["", None]:
                    annotation = StringHelper.remove_special_chars(obj['class'])
                else:
                    annotation = StringHelper.remove_special_chars(obj['ocr_result'])

                similarity = self.calculate_similarity(annotation, node.node_name, distance)

            if similarity > highest_similarity_bbox[0]:
                highest_similarity_bbox = [similarity,
                                           BoundingBoxHelper().get_middle_of_a_bbox(obj['bbox'], screenshot_path)]

        return highest_similarity_bbox

    def calculate_similarity(self, string1, string2, distance):
        print(f"Similarity {string1} {string2} {distance}")
        if string1 and string2:
            similarity = (0.7 * jellyfish.jaro_similarity(string1, string2)) + (0.3 * (1 - distance))
            print(similarity)
            return similarity
        return 0
