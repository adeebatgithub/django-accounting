from rest_framework.reverse import reverse_lazy

page_names = {
    'account-chart': 'Chart Of Accounts',
    'account-details': f'<a href="{reverse_lazy("accounting:account-chart")}">Chart Of Accounts</a> | Account Details',
    'account-create': f'<a href="{reverse_lazy("accounting:account-chart")}">Chart Of Accounts</a> | Create Account',
    'account-update': f'<a href="{reverse_lazy("accounting:account-chart")}">Chart Of Accounts</a> | Edit Account',
}