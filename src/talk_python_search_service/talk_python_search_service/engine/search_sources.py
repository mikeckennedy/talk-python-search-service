import json
import os

import datetime
from .search_record import SearchRecord
import talk_python_search_service


class SearchSources:
    search_records = []
    keyword_to_record_lookup = dict()
    trimmed_data = False
    record_factory = None

    @classmethod
    def global_init(cls, record_factory):
        """
        Setup the search engine
        :param record_factory: This is a method that access your data.
        :return: A list of SearchRecords
        """
        cls.record_factory = record_factory

    @staticmethod
    def build_records(force=False, save=False):

        if not SearchSources.record_factory:
            raise Exception("Record factory not set (call SearchSources.global_init()")

        if SearchSources.search_records and not force:
            # print("Search sources already built, not rebuilding.")
            return

        print("Building search records (force mode: {})...".format(force))
        records = SearchSources.record_factory()
        # counter = len(records)
        # for idx, record in enumerate(records):
        #     print("Processing record {} of {}".format(idx+1, counter))
        #     record.build_keywords()

        print("Building keywords for {} records...".format(len(records)))
        for record in records:
            record.build_keywords()

        SearchSources.keyword_to_record_lookup = SearchSources.get_lookup(records)
        SearchSources.search_records = records
        SearchSources.trimmed_data = False
        if save:
            SearchSources.save()

        print("Built search records successfully.")

    @classmethod
    def load(cls):
        index_filename = cls.search_file_path()

        if not os.path.exists(index_filename):
            print("No search index, cannot init")
            return False

        print("Loading {}".format(index_filename))
        with open(index_filename, 'r') as fin:
            data = json.load(fin)

        SearchSources.search_records = [
            SearchRecord.from_dict(d)
            for d in data['records']
            ]

        SearchSources.keyword_to_record_lookup = SearchSources.get_lookup(
            SearchSources.search_records)

        SearchSources.trim_data()
        return True

    @staticmethod
    def trim_data():
        print("Trimming data...")
        for sr in SearchSources.search_records:
            sr.keywords = None
        SearchSources.trimmed_data = True
        print("Done..")

    @classmethod
    def save(cls):
        if SearchSources.trimmed_data:
            raise Exception("Cannot save data that has been trimmed")

        full_file = cls.search_file_path()

        data = {
            'created': str(datetime.datetime.now()),
            'records': [
                r.to_dict()
                for r in SearchSources.search_records
                ]
        }
        with open(full_file, 'w') as fout:
            json.dump(data, fout, indent=True)

    @classmethod
    def search_file_path(cls):
        working_folder = os.path.dirname(talk_python_search_service.__file__)
        index_filename = 'search_index.json'
        full_file = os.path.abspath(os.path.join(working_folder, 'data', index_filename))
        return full_file

    @classmethod
    def get_lookup(cls, records):

        distinct_keywords = set()
        for r in records:
            distinct_keywords.update(r.keywords)

        lookup = dict()

        counter = len(distinct_keywords)
        for idx, word in enumerate(distinct_keywords):
            if idx % max(1, counter // 10) == 0:
                print("Merging keywords from records {}/{}".format(idx + 1, counter))
            lookup[word] = []
            for r in records:
                if word in r.keywords:
                    lookup[word].append(r)

        return lookup

    @classmethod
    def records_by_word(cls, word):
        return SearchSources.keyword_to_record_lookup.get(word, [])
