import hashlib
import datetime
import pytz
from django.db import models
from offers.utils import sendTransaction


# Create your models here.
class AuctionProduct(models.Model):

    description = models.CharField(max_length=30)
    seller = models.CharField(max_length=30, default='Unknown')
    location = models.CharField(max_length=30, default='')
    basePrice = models.FloatField(default=1.0)
    bestPrice = models.FloatField(default=0.0, blank=True)
    date = models.DateTimeField(blank=False)
    whoWon = models.CharField(max_length=30, default='', blank=True)
    jsonResult = models.CharField(max_length=500, default='', blank=True)
    hash = models.CharField(max_length=32, default=None, null=True, blank=True)
    txId = models.CharField(max_length=66, default=None, null=True, blank=True)

    # function to validate bookings on blockchain
    def writeOnChain(self):
        self.hash = hashlib.sha256(self.jsonResult.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()

    # function that checks if the auctions expiration date has been reached
    def isExpired(self):
        now = datetime.datetime.now()
        now = pytz.utc.localize(now)
        if self.date < now:
            return True
        return False
