from .search_sources import SearchSources
from .keyword_builder import KeywordBuilder


class SiteSearch:
    has_initialized = False

    @classmethod
    def init(cls, record_factory, use_files_across_instances=False):
        if cls.has_initialized:
            return

        cls.has_initialized = True
        SearchSources.global_init(record_factory)
        if use_files_across_instances:
            if not SearchSources.load():
                SearchSources.build_records()
        else:
            SearchSources.build_records(save=use_files_across_instances)

    @classmethod
    def perform_search(cls, text):
        if not cls.has_initialized:
            raise Exception("You must call SiteSearch.init() before you perform searches.")

        if not text:
            return set()

        words = KeywordBuilder.build_keywords([text])
        if not words:
            return set()

        sets = []
        for word in words:
            matches = set(SearchSources.records_by_word(word))
            sets.append(matches)

        final_match = sets[0]
        for s in sets[1:]:
            final_match = final_match.intersection(s)

        return final_match

    @classmethod
    def get_url(cls, search_text):
        if not search_text:
            return None
        words = KeywordBuilder.build_keywords([search_text])
        return '-'.join(words)

    @classmethod
    def from_url(cls, search_query_string):
        if not search_query_string:
            return ''

        return search_query_string.replace('-', ' ').strip()
