from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register((Party,SalesOfficer,Category,Product,DiscountCategory,Bank))
admin.site.register((SalesPerson,DiscountPerson,FreightPerson,CashPerson,IncentivePerson,ClearingPerson))
admin.site.register((SalesOfficerLedger,PartyLedger,BankLedger,DiscountLedger,FreightLedger,CashLedger,ClearingLedger,SalesLedger,IncentiveLedger))
admin.site.register((PartyOrder,Recovery,SalesOfficerReceiving,ExpectedCustomers,PartyOrderProduct))