from .keyword_builder import KeywordBuilder


class SearchRecord:
    def __init__(self, category: str, title: str, item, text_list: list = None):
        self.item = item
        self.title = title
        self.category = category
        self.text_list = text_list
        self.keywords = None

    def build_keywords(self):
        if self.keywords:
            return

        self.keywords = set()
        self.keywords = KeywordBuilder.build_keywords(self.text_list)
        self.text_list = None

    def to_dict(self, short=False):
        if not short and self.keywords is None:
            self.keywords = []

        if short:
            data = dict(category=self.category,
                        title=self.title)
        else:
            data = dict(category=self.category , keywords=list(self.keywords),
                        title=self.title)

        return data

    @classmethod
    def from_dict(cls, dict_data):
        category = dict_data.get('category')
        title = dict_data.get('title')
        keywords = set()
        if dict_data.get('keywords'):
            keywords = set(dict_data.get('keywords'))

        record = cls(category, title, dict_data)
        record.keywords = keywords

        return record
