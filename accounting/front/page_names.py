from accounting.front.accounts.page_names import page_names as accounts_page_names
from accounting.front.vouchers.page_names import page_names as vouchers_page_names
from accounting.front.dashboard.page_names import page_names as dashboard_page_names
from accounting.front.reports.page_names import page_names as reports_page_names

def page_name_processor(request):
    url_name = request.resolver_match.url_name if request.resolver_match else ''
    titles = {
        'daybook': 'Day Book',

        **dashboard_page_names,
        **accounts_page_names,
        **vouchers_page_names,
        **reports_page_names,
    }
    return {'page_name': titles.get(url_name, 'My Site')}
