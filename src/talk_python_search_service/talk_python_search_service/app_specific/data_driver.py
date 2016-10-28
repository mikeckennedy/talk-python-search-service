from talk_python_search_service.engine.search_record import SearchRecord
from talk_python_search_service.app_data.fake_db import Database


def create_search_records():
    books = Database.all_books()

    print("Building search records...")
    print("Books contents...")
    books_records = []
    for book in books:
        text_list = [book.title] + [para.text for para in book.paragraphs]
        record = SearchRecord('Book', book.title, book, text_list)
        books_records.append(record)

    print("Paragraph contents...")
    for b in books:
        for idx, para in enumerate(b.paragraphs):
            record = SearchRecord('Paragraph', '{}_paragraph_{}'.format(para.text, idx),
                                  para, [para.text])
            books_records.append(record)
    print("Loaded, building keywords...")
    return books_records

