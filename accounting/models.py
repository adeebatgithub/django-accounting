from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountModel(MPTTModel, TimeStampedModel):
    ASSET = 1
    LIABILITY = 2
    INCOME = 3
    EXPENSE = 5
    ACCOUNT_TYPE = (
        (ASSET, 'Asset'),
        (LIABILITY, 'Liability'),
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    )

    name = models.CharField(max_length=50)
    account_type = models.PositiveSmallIntegerField(choices=ACCOUNT_TYPE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_balance(self):
        return JournalEntryLineModel.objects.filter(account_id=self.id).aggregate(
            total=models.Sum(
                models.Case(
                    models.When(account__account_type__in=[self.ASSET, self.EXPENSE],
                         then=models.F('debit') - models.F('credit')),
                    models.When(account__account_type__in=[self.LIABILITY, self.INCOME],
                         then=models.F('credit') - models.F('debit')),
                    default=0,
                    output_field=models.DecimalField()
                )
            )
        )['total'] or 0

    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            self.slug = f"{slugify(self.name)}_{self.pk}"
            return super().save(update_fields=["slug"])
        return super().save(*args, **kwargs)


class JournalEntryModel(TimeStampedModel):
    date = models.DateField()
    reference_number = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    # created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.reference_number


class JournalEntryLineModel(TimeStampedModel):
    journal_entry = models.ForeignKey(JournalEntryModel, on_delete=models.CASCADE)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
