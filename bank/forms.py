from django import forms
from .models import *

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'currency']  # Only allow the user to select account type, as account_number and balance are system generated

    # Optionally, you can set up some custom behavior or validations if needed.
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['account_type'].widget = forms.RadioSelect(choices=Account.ACCOUNT_TYPES)  # Use radio buttons for account type


class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

    def save(self, account):
        amount = self.cleaned_data['amount']
        if account.deposit(amount):
            Transaction.objects.create(
                account=account,
                transaction_type=Transaction.DEPOSIT,
                amount=amount
            )
            return True
        return False

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

    def save(self, account):
        amount = self.cleaned_data['amount']
        if account.withdraw(amount):
            Transaction.objects.create(
                account=account,
                transaction_type=Transaction.WITHDRAWAL,
                amount=amount
            )
            return True
        return False