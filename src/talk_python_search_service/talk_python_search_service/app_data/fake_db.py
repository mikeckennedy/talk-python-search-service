# noinspection PyMethodMayBeStatic
import os


class Database:
    __books = []

    @classmethod
    def all_books(cls):
        if Database.__books:
            return Database.__books

        dir_name = os.path.join(
            os.path.dirname(__file__),
            'files'
        )

        Database.__books = [
            Book.create_from_file(os.path.join(dir_name, file))
            for file in os.listdir(dir_name)
            if file.endswith('.txt')
            ]

        return Database.__books


class Book:
    def __init__(self, title, text):
        self.paragraphs = self.build_paragraphs(text)
        self.title = title
        self.url = title.replace(" ", "-")

    def build_paragraphs(self, text):
        if not text:
            return []

        parts = text.split('\n\n')

        return [
            Paragraph(self, para_text
                      .strip()
                      .replace('\n', ' ')
                      .replace('\r', ' ')
                      .replace('  ', ' '))
            for para_text in parts
            if para_text.strip()
            ]

    @classmethod
    def create_from_file(cls, filename):
        full_path = os.path.abspath(filename)
        name = os.path.basename(full_path)
        with open(full_path, 'r', encoding='utf-8') as fin:
            text = fin.read()

        return Book(name, text)


class Paragraph:
    def __init__(self, book, text):
        self.text = text
        self.book = book
