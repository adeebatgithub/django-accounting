from accounting.models import AccountModel

LIST_OF_ACCOUNTS = [
    {
        "id": 1,
        "name": "Capital Account",
        "account_type": AccountModel.LIABILITY,
    },
    {
        "id": 2,
        "name": "Current Assets",
        "account_type": AccountModel.ASSET,
    },
    {
        "id": 3,
        "name": "Bank Accounts",
        "account_type": AccountModel.ASSET,
        "parent_id": 2
    },
    {
        "id": 4,
        "name": "Cash In Hand",
        "account_type": AccountModel.ASSET,
        "parent_id": 2
    },
    {
        "id": 5,
        "name": "Current Liabilities",
        "account_type": AccountModel.LIABILITY,
    },
    {
        "id": 6,
        "name": "Direct Expense",
        "account_type": AccountModel.EXPENSE,
    },
    {
        "id": 7,
        "name": "Indirect Expense",
        "account_type": AccountModel.EXPENSE,
    },
    {
        "id": 8,
        "name": "Direct Income",
        "account_type": AccountModel.INCOME,
    },
    {
        "id": 9,
        "name": "Indirect Income",
        "account_type": AccountModel.INCOME,
    },
    {
        "id": 10,
        "name": "Fixed Assets",
        "account_type": AccountModel.ASSET,
    },
    {
        "id": 11,
        "name": "Investments",
        "account_type": AccountModel.ASSET,
    },
    {
        "id": 12,
        "name": "Loans",
        "account_type": AccountModel.LIABILITY,
    },
    {
        "id": 13,
        "name": "Purchase Account",
        "account_type": AccountModel.EXPENSE,
    },
    {
        "id": 14,
        "name": "Sales Account",
        "account_type": AccountModel.INCOME,
    },
    {
        "id": 15,
        "name": "Cash",
        "account_type": AccountModel.ASSET,
        "parent_id": 4
    },
    {
        "id": 15,
        "name": "Accounts Receivable",
        "account_type": AccountModel.ASSET,
        "parent_id": 2
    },
]
