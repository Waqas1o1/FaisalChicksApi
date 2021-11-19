from rest_framework import serializers
from . import models as m
from django.db.models import F, Sum
from django.contrib.auth.models import User
# Table
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email', 'first_name', 'last_name','password','last_login')
    
class DiscountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.DiscountCategory
        fields = '__all__'


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Party
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        response['discount'] = DiscountCategorySerializer(instance.discount).data
        response['sale_officer'] = SalesOfficerSerializer(instance.sale_officer).data
        return response

class SalesOfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SalesOfficer
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UsersSerializer(instance.user).data
        return response

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Product
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        return response

class SalesOfficerLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SalesOfficerLedger
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sales_officer'] = SalesOfficerSerializer(instance.sales_officer).data
        return response


class SalesPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SalesPerson
        fields = '__all__'

class DiscountPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.DiscountPerson
        fields = '__all__'

class FreightPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.FreightPerson
        fields = '__all__'

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Bank
        fields = '__all__'

class ClearingPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ClearingPerson
        fields = '__all__'

class CashPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.CashPerson
        fields = '__all__'

class IncentivePersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.IncentivePerson
        fields = '__all__'


# Ledger
class PartyLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PartyLedger
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['party'] = PartySerializer(instance.party).data
        response['sales_officer'] = SalesOfficerSerializer(instance.sales_officer).data
        return response

class SalesLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SalesLedger
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sales_person'] = SalesPersonSerializer(instance.sales_person).data

        return response

class FreightLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.FreightLedger
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response

class DiscountLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.DiscountLedger
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)

        return response

class BankLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.BankLedger
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bank'] = BankSerializer(instance.bank).data
        return response

class ClearingLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ClearingLedger
        fields = '__all__'

class CashLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.CashLedger
        fields = '__all__'

class IncentiveLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.IncentiveLedger
        fields = '__all__'


# UI

class DispatchTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.DispatchTable
        fields = '__all__'


class POPSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PartyOrderProduct
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['product'] = ProductSerializer(instance.product).data
        return response

class PartyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PartyOrder
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['party'] = PartySerializer(instance.party).data
        response['sale_officer'] = SalesOfficerSerializer(instance.sale_officer).data
        pop = m.PartyOrderProduct.objects.filter(party_order=instance)
        response['products'] = POPSerializer(pop,many=True).data
        pd = m.PartyOrderProduct.objects.filter(party_order=instance)
        sum = 0
        for p in pd:
            sum += p.qty
        response['pdt_qty__sum'] = sum

        if response['status'] == 'Delivered':
            dt = m.DispatchTable.objects.get(party_order=instance)
            response['dispatch'] = DispatchTableSerializer(dt).data
        return response


class PartyOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PartyOrderProduct
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['party_order'] = PartyOrderSerializer(instance.party_order).data
        response['product'] = ProductSerializer(instance.product).data
        return response


class RecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Recovery
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['bank'] = BankSerializer(instance.bank).data
        response['party'] = PartySerializer(instance.party).data
        response['party_order'] = PartyOrderSerializer(instance.party_order).data
        response['sale_officer'] = SalesOfficerSerializer(instance.sale_officer).data
        return response


class SalesOfficerReceivingSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SalesOfficerReceiving
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sales_officer'] = SalesOfficerSerializer(instance.sales_officer).data
        return response
