from django.db import models
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Account(models.Model):
    SAVINGS = 'SAVINGS'
    CHECKING = 'CHECKING'

    ACCOUNT_TYPES = [
        (SAVINGS, 'Savings Account'),
        (CHECKING, 'Checking Account'),
    ]

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('NGN', 'Nigerian Naira'),
    ]


    ACCOUNT_STATUSES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True, editable=False)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default=SAVINGS)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    status = models.CharField(max_length=10, choices=ACCOUNT_STATUSES, default='ACTIVE')


    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        while True:
            account_number = str(random.randint(1000000000, 9999999999))  # Generate 10-digit number
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    # def update_account_status(self):
    #     now = timezone.now()

    #     if self.last_transaction_date and now - self.last_transaction_date >= timedelta(days=30):
    #         self.status = self.INACTIVE

    #     if self.last_transaction_date and now - self.last_transaction_date >= timedelta(days=90):
    #         self.status = self.CLOSED

    #     self.save()

    def __str__(self):
        return f'{self.account_number} - {self.user.email}'


class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_transaction_type_display()} - {self.amount}'
