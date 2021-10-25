from django.db import models
from django.utils import timezone
from utils.utils import UpdateLeadgers,DeleteLeadgers
from django.contrib.auth.models import User
# Users

# ~~~~~~~~~~~
class SalesOfficer(models.Model):
    name = models.CharField(max_length=200,unique=True)
    commission = models.FloatField(default=0.0)
    contact = models.CharField(max_length=13)
    
    
    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance
        super(SalesOfficer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class DiscountCategory(models.Model):
    name = models.CharField(max_length=50)
    discount = models.FloatField()

    def __str__(self):
        return self.name + ' : ' + str(self.discount)

class Category(models.Model):
    name = models.CharField(max_length=300,unique=True)
    date = models.DateField(default=timezone.now, blank=True)
    def __str__(self):
        return self.name 
 
class Party(models.Model):
    ref_id = models.IntegerField(blank=True,null=True)  
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    area = models.CharField(max_length=300)
    zone = models.CharField(max_length=300)
    region = models.CharField(max_length=300)
    contact = models.CharField(max_length=13)
    # Relation
    discount = models.ForeignKey(DiscountCategory,on_delete=models.CASCADE)
    sale_officer = models.ForeignKey(SalesOfficer,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    # Accounts
    creditLimit = models.FloatField()
    salesTarget = models.FloatField()
    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)
    # Images 
    SCI = models.FileField(null=True,blank=True,upload_to='Security Check Images')
    TOR = models.FileField(null=True,blank=True,upload_to='Terms of Recoreds')
    # Date
    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance

        super(Party, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
   
class Product(models.Model):
    name = models.CharField(max_length=200,unique=True)
    type = models.CharField(max_length=300,choices=(('Pellet','Pellet'),('CRUMSS','CRUMSS')))
    unit = models.CharField(max_length=30,default='Kg')
    pakage_weight = models.IntegerField(default=0)
    sales_price = models.FloatField(default=0)
    cost_price = models.FloatField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE) 
    date = models.DateField(default=timezone.now, blank=True)
    
    def __str__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length=30, unique=True)
    account_no = models.CharField(max_length=400)
    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)

    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance

        super(Bank, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# ~~~~~~~~  
class SalesPerson(models.Model):
    name = models.CharField(max_length=30, unique=True)

    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)

    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance
        super(SalesPerson, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
 
class DiscountPerson(models.Model):
    name = models.CharField(max_length=30, unique=True)

    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)

    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance

        super(DiscountPerson, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
 
class FreightPerson(models.Model):
    name = models.CharField(max_length=30, unique=True)
    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)

    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance

        super(FreightPerson, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class CashPerson(models.Model):
    name = models.CharField(max_length=30, unique=True)
    # Opening
    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)

    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance

        super(CashPerson, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class OnlinePerson(models.Model):
    name = models.CharField(max_length=30, unique=True)
    # Opening
    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)

    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance

        super(OnlinePerson, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ClearingPerson(models.Model):
    name = models.CharField(max_length=30, unique=True)
    # Opening
    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)

    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance

        super(ClearingPerson, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class IncentivePerson(models.Model):
    name = models.CharField(max_length=30, unique=True)
    # Opening
    opening_Balance = models.FloatField()
    current_Balance = models.FloatField(blank=True, null=True)

    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if self.id == None:
            self.current_Balance = self.opening_Balance

        super(IncentivePerson, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Ledgers
class Ledger(models.Model):
    date = models.DateField(default=timezone.now, blank=True)
    description = models.CharField(max_length=50, null=True)
    transaction_type = models.CharField(max_length=50, choices=(
        ('Debit', 'Debit'), ('Credit', 'Credit')))
    total_amount = models.FloatField(null=True)
    net_balance = models.FloatField(blank=True, default=0.0)

    def __str__(self):
        return str(self.id)
    
class PartyLedger(Ledger):
    party = models.ForeignKey(Party,on_delete=models.CASCADE)
    sales_officer = models.ForeignKey(SalesOfficer, on_delete=models.CASCADE)
    freight = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.party.name + str(self.id)

    def save(self, *args, **kwargs):        
        if self.id == None:
            if self.transaction_type == 'Credit':
                self.party.current_Balance -= self.total_amount
                self.net_balance = self.party.current_Balance
            else:
                self.party.current_Balance += self.total_amount
                self.net_balance = self.party.current_Balance
            self.party.save()
            super(PartyLedger, self).save(*args, **kwargs)
        else:
            up = kwargs.pop('updating', {})
            obj = self
            if up == {}:
                obj = UpdateLeadgers(self, PartyLedger, 'Party', True)
                obj.total_amount = self.total_amount

            super(PartyLedger, obj).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        up = kwargs.pop('updating', {})
        if up == {}:
            DeleteLeadgers(self, PartyLedger, 'Party', True)
        else:
            super(PartyLedger, self).delete()

class SalesOfficerLedger(Ledger):
    sales_officer = models.ForeignKey(SalesOfficer, on_delete=models.CASCADE)
    party_order = models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return self.sales_officer.name + str(self.id)

    def save(self, *args, **kwargs):        
        if self.id == None:
            if self.transaction_type == 'Credit':
                self.sales_officer.current_Balance -= self.total_amount
                self.net_balance = self.sales_officer.current_Balance
            else:
                self.sales_officer.current_Balance += self.total_amount
                self.net_balance = self.sales_officer.current_Balance
            self.sales_officer.save()

            super(SalesOfficerLedger, self).save(*args, **kwargs)
        else:
            up = kwargs.pop('updating', {})
            obj = self
            if up == {}:
                obj = UpdateLeadgers(self, SalesOfficerLedger, 'SalesOfficer', True)
                obj.description = self.description
                obj.total_amount = self.total_amount

            super(SalesOfficerLedger, obj).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        up = kwargs.pop('updating', {})
        if up == {}:
            DeleteLeadgers(self, SalesOfficerLedger, 'SalesOfficer', True)
        else:
            super(SalesOfficerLedger, self).delete()

class BankLedger(Ledger):
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.bank.name

    def save(self, *args, **kwargs):        
        if self.id == None:
            if self.transaction_type == 'Credit':
                self.bank.current_Balance -= self.total_amount
                self.net_balance = self.bank.current_Balance
            else:
                self.bank.current_Balance += self.total_amount
                self.net_balance = self.bank.current_Balance
            self.bank.save()
            super(BankLedger, self).save(*args, **kwargs)
        else:
            up = kwargs.pop('updating', {})
            obj = self
            if up == {}:
                obj = UpdateLeadgers(self, BankLedger, 'Bank', True)
                obj.total_amount = self.total_amount

            super(BankLedger, obj).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        up = kwargs.pop('updating', {})
        if up == {}:
            DeleteLeadgers(self, DiscountLedger, 'Bank', True)
        else:
            super(DiscountLedger, self).delete()   

class SalesLedger(Ledger):
    sales_person = models.ForeignKey(SalesPerson,on_delete=models.CASCADE)
   
    def __str__(self):
        return self.sales_person.name 
    
    def save(self, *args, **kwargs):        
        if self.id == None:
            self.sales_person = SalesPerson.objects.first()
            if self.transaction_type == 'Credit':
                self.sales_person.current_Balance -= self.total_amount
                self.net_balance = self.sales_person.current_Balance
            else:
                self.sales_person.current_Balance += self.total_amount
                self.net_balance = self.sales_person.current_Balance
            self.sales_person.save()
            super(SalesLedger, self).save(*args, **kwargs)
        else:
            up = kwargs.pop('updating', {})
            obj = self
            if up == {}:
                obj = UpdateLeadgers(self, SalesLedger, 'Sales', True)
                obj.total_amount = self.total_amount

            super(SalesLedger, obj).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        up = kwargs.pop('updating', {})
        if up == {}:
            DeleteLeadgers(self, SalesLedger, 'Sales', True)
        else:
            super(SalesLedger, self).delete()

class FreightLedger(Ledger):
    freight_person = models.ForeignKey(FreightPerson,on_delete=models.CASCADE)
    freight = models.FloatField()
    def __str__(self):
        return self.freight_person.name   
    
    def save(self, *args, **kwargs):        
        if self.id == None:
            self.freight_person = FreightPerson.objects.first()
            if self.transaction_type == 'Credit':
                self.freight_person.current_Balance -= self.total_amount
                self.net_balance = self.freight_person.current_Balance
            else:
                self.freight_person.current_Balance += self.total_amount
                self.net_balance = self.freight_person.current_Balance
            self.freight_person.save()
            super(FreightLedger, self).save(*args, **kwargs)
        else:
            up = kwargs.pop('updating', {})
            obj = self
            if up == {}:
                obj = UpdateLeadgers(self, FreightLedger, 'Freight', True)
                obj.total_amount = self.total_amount

            super(FreightLedger, obj).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        up = kwargs.pop('updating', {})
        if up == {}:
            DeleteLeadgers(self, FreightLedger, 'Freight', True)
        else:
            super(FreightLedger, self).delete()

class DiscountLedger(Ledger):
    discount_person = models.ForeignKey(DiscountPerson,on_delete=models.CASCADE)
    discounted_amount = models.FloatField()
    
    def __str__(self):
        return self.discount_person.name 

    def save(self, *args, **kwargs):        
        if self.id == None:
            self.discount_person = DiscountPerson.objects.first()
            if self.transaction_type == 'Credit':
                self.discount_person.current_Balance -= self.total_amount
                self.net_balance = self.discount_person.current_Balance
            else:
                self.discount_person.current_Balance += self.total_amount
                self.net_balance = self.discount_person.current_Balance
            self.discount_person.save()
            super(DiscountLedger, self).save(*args, **kwargs)
        else:
            up = kwargs.pop('updating', {})
            obj = self
            if up == {}:
                obj = UpdateLeadgers(self, DiscountLedger, 'Discount', True)
                obj.total_amount = self.total_amount

            super(DiscountLedger, obj).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        up = kwargs.pop('updating', {})
        if up == {}:
            DeleteLeadgers(self, DiscountLedger, 'Discount', True)
        else:
            super(DiscountLedger, self).delete()   

class CashLedger(Ledger):
    cash_person = models.ForeignKey(CashPerson,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.cash_person.name 

    def save(self, *args, **kwargs):        
        if self.id == None:
            self.cash_person = CashPerson.objects.first()
            if self.transaction_type == 'Credit':
                self.Cash_person.current_Balance -= self.total_amount
                self.net_balance = self.cash_person.current_Balance
            else:
                self.cash_person.current_Balance += self.total_amount
                self.net_balance = self.cash_person.current_Balance
            self.cash_person.save()
            super(CashLedger, self).save(*args, **kwargs)
        else:
            up = kwargs.pop('updating', {})
            obj = self
            if up == {}:
                obj = UpdateLeadgers(self, CashLedger, 'Cash', True)
                obj.total_amount = self.total_amount

            super(CashLedger, obj).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        up = kwargs.pop('updating', {})
        if up == {}:
            DeleteLeadgers(self, CashLedger, 'Cash', True)
        else:
            super(CashLedger, self).delete()   

class ClearingLedger(Ledger):
    clearing_person = models.ForeignKey(ClearingPerson,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.clearing_person.name 

    def save(self, *args, **kwargs):        
        if self.id == None:
            self.clearing_person = ClearingPerson.objects.first()
            if self.transaction_type == 'Credit':
                self.clearing_person.current_Balance -= self.total_amount
                self.net_balance = self.clearing_person.current_Balance
            else:
                self.clearing_person.current_Balance += self.total_amount
                self.net_balance = self.clearing_person.current_Balance
            self.clearing_person.save()
            super(ClearingLedger, self).save(*args, **kwargs)
        else:
            up = kwargs.pop('updating', {})
            obj = self
            if up == {}:
                obj = UpdateLeadgers(self, ClearingLedger, 'Clearing', True)
                obj.total_amount = self.total_amount

            super(ClearingLedger, obj).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        up = kwargs.pop('updating', {})
        if up == {}:
            DeleteLeadgers(self, ClearingLedger, 'Clearing', True)
        else:
            super(ClearingLedger, self).delete()   

class IncentiveLedger(Ledger):
    incentive_person = models.ForeignKey(IncentivePerson,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.incentive_person.name 

    def save(self, *args, **kwargs):        
        if self.id == None:
            self.incentive_person = IncentivePerson.objects.first()
            if self.transaction_type == 'Credit':
                self.incentive_person.current_Balance -= self.total_amount
                self.net_balance = self.incentive_person.current_Balance
            else:
                self.incentive_person.current_Balance += self.total_amount
                self.net_balance = self.incentive_person.current_Balance
            self.incentive_person.save()
            super(IncentiveLedger, self).save(*args, **kwargs)
        else:
            up = kwargs.pop('updating', {})
            obj = self
            if up == {}:
                obj = UpdateLeadgers(self, IncentiveLedger, 'Incentive', True)
                obj.total_amount = self.total_amount

            super(IncentiveLedger, obj).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        up = kwargs.pop('updating', {})
        if up == {}:
            DeleteLeadgers(self, IncentiveLedger, 'Incentive', True)
        else:
            super(IncentiveLedger, self).delete()   

# UI
class PartyOrder(models.Model):
    date = models.DateField(default=timezone.now, blank=True)
    party = models.ForeignKey(Party,on_delete=models.CASCADE)
    sale_officer = models.ForeignKey(SalesOfficer,on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Confirmed','Confirmed'),('Delivered','Delivered')], default='Pending')
    description = models.CharField(max_length=50,blank=True,null=True)
    freight = models.FloatField(default=0)
   
    
    total_amount = models.FloatField()
    pandding_amount = models.IntegerField(blank=True,default=0)
    discounted_amount = models.FloatField(null=True, blank=True)


    pl = models.ForeignKey(PartyLedger,on_delete=models.SET_NULL,null=True,blank=True, related_name='+')
    plc1 = models.ForeignKey(PartyLedger,on_delete=models.SET_NULL,null=True,blank=True, related_name='+')
    plc2 = models.ForeignKey(PartyLedger,on_delete=models.SET_NULL,null=True,blank=True, related_name='+')
    sl = models.ForeignKey(SalesLedger,on_delete=models.SET_NULL,null=True,blank=True)
    sol = models.ForeignKey(SalesOfficerLedger,on_delete=models.SET_NULL,null=True,blank=True)
    il = models.ForeignKey(IncentiveLedger,on_delete=models.SET_NULL,null=True,blank=True)
    fl = models.ForeignKey(FreightLedger,on_delete=models.SET_NULL,null=True,blank=True)
    dl = models.ForeignKey(DiscountLedger,on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return self.party.name + ' : ' + str(self.id)
    

    def save(self, *args, **kwargs):
        if self.id == None:
            self.pandding_amount = self.total_amount
            self.discounted_amount = self.total_amount * (self.party.discount.discount/100) 
            super(PartyOrder, self).save(*args, **kwargs)
        else:
            # If Approved
            if self.status == 'Delivered':
                if not self.pl:
                    pl = PartyLedger(party=self.party,sales_officer=self.sale_officer, 
                                    freight = self.freight,transaction_type='Debit',
                                    description=self.description,
                                    total_amount=self.total_amount)
                    pl.save()
                    self.pl = pl
                    pl = PartyLedger(party=self.party,sales_officer=self.sale_officer, 
                                    freight = self.freight,transaction_type='Credit',
                                    description=self.description,
                                    total_amount=self.freight)
                    pl.save()
                    self.plc1 = pl
                    pl = PartyLedger(party=self.party,sales_officer=self.sale_officer,
                                    transaction_type='Credit',
                                    description=self.description,
                                    total_amount=self.discounted_amount)
                    pl.save()
                    self.plc2 = pl
                    # -------------------
                    dl = DiscountLedger(total_amount=self.discounted_amount,transaction_type='Debit'
                                        ,discounted_amount=self.discounted_amount)
                    dl.save()
                    self.dl = dl

            if self.status == 'Confirmed':
                if not self.sl:
                    # --------------------
                    sl = SalesLedger(total_amount=self.total_amount,transaction_type='Credit')

                    sl.save()
                    self.sl = sl
                    # -------------------
                    sl = SalesOfficerLedger(sales_officer=self.sale_officer,transaction_type='Credit',
                                            description = self.description,
                                            party_order = self.id,
                                            total_amount =self.total_amount - self.total_amount *(self.sale_officer.commission/100))
                    sl.save()
                    self.sol = sl
                    # --------------------
                    il = IncentiveLedger(total_amount=self.total_amount *(self.sale_officer.commission/100),transaction_type='Debit',description=self.description)
                    il.save()
                    self.il = il
                    # --------------------
                    fl = FreightLedger(total_amount=self.freight,freight=self.freight,transaction_type='Debit')
                    fl.save()
                    self.fl = fl
               
                # ##################
            super(PartyOrder, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.status == 'Delivered':
            self.pl.delete();
            self.plc1.delete();
            self.plc2.delete();
            self.dl.delete()
        elif self.status == 'Confirmed':
            self.sol.delete()
            self.sl.delete()
            self.il.delete()
            self.fl.delete()

        super(PartyOrder, self).delete()

class PartyOrderProduct(models.Model):
    party_order = models.ForeignKey(PartyOrder,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField()
    rate = models.IntegerField()
    
    def __str__(self):
        return str(self.party_order.id)
      
class Recovery(models.Model):
    date = models.DateField(default=timezone.now, blank=True)
    party = models.ForeignKey(Party,on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved','Approved')], default='Pending')
    party_order = models.ForeignKey(PartyOrder,on_delete=models.CASCADE,null=True,blank=True)
    sale_officer = models.ForeignKey(SalesOfficer,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20,choices=(('Cash','Cash'),('Bank','Bank'),('Clearing','Clearing'))) 
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE,null=True,blank=True)
    amount = models.FloatField()
    description = models.CharField(blank=True,null=True,max_length=50)

    pl = models.ForeignKey(PartyLedger,on_delete=models.CASCADE,null=True,blank=True)
    bl = models.ForeignKey(BankLedger,on_delete=models.CASCADE,null=True,blank=True)
    cl = models.ForeignKey(CashLedger,on_delete=models.CASCADE,null=True,blank=True)
    cll = models.ForeignKey(ClearingLedger,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.id) + ':' + self.sale_officer.name

    def delete(self, *args, **kwargs):
        if self.status == 'Approved':
            self.pl.delete();
            if self.payment_method == 'Bank':
                self.bl.delete();
            if self.payment_method == 'Clearing':
                self.cll.delete();
            if self.payment_method == 'Cash':
                self.cl.delete();
            

        super(Recovery, self).delete()
    
    def save(self, *args, **kwargs):
        if self.id == None:
            super(Recovery, self).save(*args, **kwargs)
        else:
            if self.party_order:
                order = PartyOrder.objects.get(id=self.party_order.id)
                order.pandding_amount -= self.amount
                order.save()
            if self.status == 'Approved':
                if self.party_order:
                    pl = PartyLedger(party=self.party,sales_officer=self.sale_officer, 
                                freight = self.party_order.freight,transaction_type='Credit',
                                description=self.description,
                                total_amount=self.amount)
                    pl.save()                 
                else:
                    pl = PartyLedger(party=self.party,sales_officer=self.sale_officer, 
                                    transaction_type='Credit',
                                    description=self.description,
                                    total_amount=self.amount)
                    pl.save()
                self.pl = pl
                
                if self.payment_method == 'Bank':
                    bl = BankLedger(bank=self.bank,transaction_type='Debit',
                                    description=self.description,
                                    total_amount=(self.amount))
                    bl.save()
                    self.bl = bl
                elif self.payment_method == 'Cash':
                    cl = CashLedger(transaction_type='Debit',
                                    description=self.description,
                                    total_amount=(self.amount))
                    cl.save()
                    self.cl = cl
                elif self.payment_method == 'Clearing':
                    ccl = ClearingLedger(transaction_type='Debit',
                                description=self.description,
                                total_amount=(self.amount))
                    ccl.save()
                    self.cll = ccl
            super(Recovery, self).save(*args, **kwargs)  

class DispatchTable(models.Model):
    driver = models.CharField(max_length=300)
    freight = models.IntegerField(default=0)
    vehical_no = models.CharField(max_length=10)
    cell_no = models.CharField(max_length=12,blank=True,null=True)
    bulty_no = models.CharField(max_length=30)
    gate_pass = models.CharField(max_length=300)
    party_order = models.ForeignKey(PartyOrder,on_delete=models.CASCADE)
    locations = models.TextField(null=True)
    def __str__(self) -> str:
        return self.driver + '->' +  self.bulty_no
        
class SalesOfficerReceiving(models.Model):
    date = models.DateField(default=timezone.now, blank=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved','Approved')], default='Pending')
    sale_officer = models.ForeignKey(SalesOfficer,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20,choices=(('Cash','Cash'),('Bank','Bank'),('Clearing','Clearing'))) 
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE,null=True,blank=True)
    recieved_amount = models.FloatField()
    description = models.CharField(max_length=50)

    sol = models.ForeignKey(SalesOfficerLedger,on_delete=models.CASCADE,null=True,blank=True)
    bl = models.ForeignKey(BankLedger,on_delete=models.CASCADE,null=True,blank=True)
    cl = models.ForeignKey(CashLedger,on_delete=models.CASCADE,null=True,blank=True)
    cll = models.ForeignKey(ClearingLedger,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.date) + ':' + self.sale_officer.name

    
    def save(self, *args, **kwargs):
        if self.id == None:
            super(SalesOfficerReceiving, self).save(*args, **kwargs)
        else:
            if self.status == 'Approved':
                sl = SalesOfficerLedger(sales_officer=self.sale_officer,transaction_type='Credit',
                                description = self.description,
                                total_amount = self.recieved_amount)
                sl.save()
                self.sol = sl
                
                if self.payment_method == 'Bank':
                    bl = BankLedger(bank=self.bank,transaction_type='Debit',
                                description=self.description,
                                total_amount=self.recieved_amount)
                    bl.save()
                    self.bl = bl
                elif self.payment_method == 'Cash':
                    cl = CashLedger(transaction_type='Debit',
                                description=self.description,
                                total_amount=self.recieved_amount)
                    cl.save()
                    self.cl = cl
                elif self.payment_method == 'Clearing':
                    ccl = ClearingLedger(transaction_type='Debit',
                                description=self.description,
                                total_amount=self.recieved_amount)
                    ccl.save()
                    self.cll = ccl
            super(SalesOfficerReceiving, self).save(*args, **kwargs)  

class ExpectedCustomers(models.Model):
    customer = models.CharField(max_length=300)
    location = models.CharField(max_length=1000)
    category = models.CharField(choices=(('Farmer','Farmer'),('Dealer','Dealer'),('Distributer','Distributer')),max_length=15)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved','Approved')], default='Pending')
    monthly_rage = models.IntegerField()
    attached_company = models.CharField(max_length=300)
    response = models.CharField(max_length=1000)

    discount = models.ForeignKey(DiscountCategory,on_delete=models.SET_NULL,null=True,blank=True)
    contact = models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return self.customer
    
    def save(self,*args,**kwargs):
        if self.status == 'Approved':
            p = Party(name=self.customer,opening_Balance=0,discount=self.discount,contact=self.contact)
            p.save()
            print(p)
        super(ExpectedCustomers,self).save(*args,**kwargs)