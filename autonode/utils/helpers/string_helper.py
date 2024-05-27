import re


class StringHelper:

    def __init__(self):
        pass

    @classmethod
    def remove_special_chars(cls, sentence):
        """
        Extract alphabets and numerics, keeping spaces and removing other special characters from a sentence.

        Parameters:
        - sentence: Input sentence from which special characters need to be removed.

        Returns:
        - A string containing only alphabets, numerics, and spaces.
        """
        # Use regular expression to keep only alphabets, numerics, and spaces
        alphanumeric_string = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
        return alphanumeric_string

    @classmethod
    def type_response_cleaner(cls, string):
        string = cls._remove_quotes(string)
        return string

    @classmethod
    def _remove_quotes(cls, string):
        return re.sub(r'["\']', '', string)
