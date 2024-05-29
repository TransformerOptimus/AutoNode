from typing import List

import easyocr

from ocr.ocr.configs.settings import OcrConfig


class EasyOcr(object):
    def __init__(self, lang_list: List[str], gpu: bool):
        self.decoder = OcrConfig.easyocr_image_decoder
        self.text_threshold = OcrConfig.easyocr_text_threshold
        self.beam_width = OcrConfig.easyocr_image_decoder_beam_width
        self.batch_size = OcrConfig.easyocr_image_decoder_batch_size
        self.width_ths = OcrConfig.easyocr_image_decoder_width_ths
        self.mag_ratio = OcrConfig.easyocr_image_decoder_mag_ratio
        self.low_text = OcrConfig.easyocr_image_decoder_low_text
        self.reader = easyocr.Reader(lang_list, gpu=gpu)

    def predict_para_text(self, image: str):
        return self.reader.readtext(image, batch_size=self.batch_size, mag_ratio=self.mag_ratio,
                                    low_text=self.low_text, text_threshold=self.text_threshold, paragraph=True)

    def predict_text(self, image_contents: bytes):
        return self.reader.readtext(image_contents, batch_size=self.batch_size, decoder=self.decoder,
                                    beamWidth=self.beam_width, width_ths=self.width_ths)
