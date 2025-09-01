from django.contrib import admin

from accounting.models import *

@admin.register(AccountModel)
class AccountModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'parent')


@admin.register(JournalEntryModel)
class JournalEntryModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'reference_number', 'description')


@admin.register(JournalEntryLineModel)
class JournalEntryLineModelAdmin(admin.ModelAdmin):
    list_display = ('journal_entry', 'account', 'debit', 'credit')
