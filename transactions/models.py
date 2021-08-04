import uuid
from django.db import models


class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    price = models.IntegerField()
    date = models.DateTimeField()
    CLOSED = 'closed'
    FUNDING = 'funding'
    FUNDING_USER = 'funding-user'
    PENDING = 'pending'
    REVERSED = 'reversed'
    TRANSACTION_STATUS_CHOICES = [
        (CLOSED, 'Closed'),
        (FUNDING, 'Funding'),
        (FUNDING_USER, 'User funding'),
        (PENDING, 'Pending'),
        (REVERSED, 'Reversed'),
    ]
    transaction_status = models.CharField(
        max_length=12,
        choices=TRANSACTION_STATUS_CHOICES,
        default=PENDING
    )
    approval_status = models.BooleanField(default=False)
    charge_status = models.BooleanField()
    company = models.ForeignKey(
        'Companies',
        on_delete=models.CASCADE,
        default=uuid.uuid4()
    )

    def save(self, *args, **kwargs):
        if self.approval_status is True and self.transaction_status == 'closed':
            self.charge_status = True
            super().save(*args, **kwargs)


class Companies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=32)
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    COMPANIES_STATUS_CHOICES =[
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    company_status = models.CharField(
        max_length=8,
        choices=COMPANIES_STATUS_CHOICES,
        default=ACTIVE
    )