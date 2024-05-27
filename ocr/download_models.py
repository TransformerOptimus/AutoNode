from easyocr import easyocr

import ocr.configs.settings

easyocr.Reader(ocr.configs.settings.OcrConfig.languages)
