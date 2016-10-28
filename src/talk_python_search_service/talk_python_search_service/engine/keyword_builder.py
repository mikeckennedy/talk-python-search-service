class KeywordBuilder:
    @staticmethod
    def build_keywords(text_list: list):
        words = set()
        if not text_list:
            return words

        for text in text_list:
            words.update(KeywordBuilder.tokenize(text))

        return words

    @classmethod
    def tokenize(cls, text: str):
        letters = [
            ch if ch.isalnum() else ' '
            for ch in text
            ]

        clean_text = ''.join(letters).lower()
        chars = -1
        while chars != len(clean_text):
            chars = len(clean_text)
            clean_text.replace('  ', ' ')

        words = {
            ch.strip()
            for ch in clean_text.split(' ')
            if ch.strip()
            }

        return words
