from django import forms

from accounting.models import AccountModel


class AccountUpsertForm(forms.ModelForm):
    opening_balance = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = AccountModel
        exclude = ('is_active', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_type'].required = False
        self.fields['parent'].empty_label = "primary"
        print(self.fields['parent'].required)
        print(self.fields['parent'].empty_label)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        account_type = self.cleaned_data.get('account_type')
        if AccountModel.objects.filter(name__iexact=name, account_type=account_type).exists():
            raise forms.ValidationError("An account with this name already exists.")
        return name

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        if parent:
            self.cleaned_data['account_type'] = parent.account_type
        return parent

    def clean_account_type(self):
        account_type = self.cleaned_data.get('account_type')
        parent = self.cleaned_data.get('parent')
        if account_type and parent:
            raise forms.ValidationError("Account with parent is allowed to change the account type.")
        return account_type
