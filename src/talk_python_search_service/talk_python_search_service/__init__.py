from pyramid.config import Configurator
from talk_python_search_service.app_specific import data_driver
from talk_python_search_service.engine.site_search import SiteSearch
import talk_python_search_service.engine.search_task as search_task


def main(_, **settings):
    config = Configurator(settings=settings)

    init_includes(config)
    init_routes(config)
    init_search(config)

    return config.make_wsgi_app()


def init_search(config):

    SiteSearch.init(record_factory=data_driver.create_search_records)

    freq = 60 * int(config.get_settings().get('refresh_in_minutes'))
    search_task.set_frequency(freq_in_seconds=freq)
    search_task.start_search_task()


def init_includes(config):
    config.include('pyramid_chameleon')


def init_routes(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('search', '/api/search')
    config.scan()
