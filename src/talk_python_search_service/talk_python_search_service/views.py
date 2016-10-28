import datetime
from pyramid.view import view_config
from talk_python_search_service.engine.site_search import SiteSearch
import talk_python_search_service.engine.webutils as webutils


@view_config(route_name='home', renderer='templates/index.pt')
def index(_):
    return {}


@view_config(route_name='search', renderer='json')
def search(request):
    search_text = request.GET.get('q')
    words = webutils.from_url_style(search_text)

    t0 = datetime.datetime.now()

    raw_results = list(SiteSearch.perform_search(words))

    result_dicts = [
        r.to_dict(short=True)
        for r in raw_results]

    dt = datetime.datetime.now() - t0

    return {
        'results': result_dicts,
        'elapsed_ms': dt.total_seconds() * 1000
            }
