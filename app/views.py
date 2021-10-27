from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework  import viewsets,generics
from rest_framework.response import Response
from app import models as m
from app import serializers as s
from app import permisions as p
from django.db.models import Q, F
from django.views.decorators.csrf import csrf_exempt
from utils.utils import GetLegder
from utils.enums import Groups as g
from django.contrib.auth.models import Group



# Create your views here.
# Authentication
 
# CRUD oprations
class PartyViewSet(viewsets.ViewSet):
    def list(self, request):
        user = request.user.groups.all().first()
        if user:
            user = user.name
        if user == 'salesofficer':
            sales_officer = m.SalesOfficer.objects.get(user=request.user)
            data = m.Party.objects.filter(sale_officer=sales_officer)
        else:
            data = m.Party.objects.all()

        serializer = s.PartySerializer(
            data, many=True, context={"request": request})
        response_dict = {
            "error": False, "message": "All List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        # if request.user.is_superuser:
        try:
            serializer = s.PartySerializer(data=request.data)
            serializer.is_valid(raise_exception=False)
            print(serializer.errors)
            serializer.save()
            dict_response = {"error": False,
                            "message": "Data Save Successfully"}
        except ValueError as err:
            dict_response = {"error": True, "message": err}
        except:
            dict_response = {"error": True,
                            "message": "Error During Saving Data"}
        # else:
        #     dict_response = {
        #         "error": True, "message": 'UnAuthenticated Person'}
        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant :
            queryset = m.Party.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.PartySerializer(
                query, context={"request": request})
            serializer_data = serializer.data
        
            return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})
        else:
            response_dict = {
                "error": False, "message": 'UnAuthenticated Person'}
        return Response(response_dict)
    def update(self, request, pk=None):
        # if request.user.is_superuser:
        if request:
            try:
                queryset = m.Party.objects.all()
                query = get_object_or_404(queryset, pk=pk)
                serializer = s.PartySerializer(
                    query, data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Successfully Updated Data"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Updating Data"}

            return Response(dict_response)
        else:
            response_dict = {
                "error": True, "message": 'UnAuthenticated Person'}
        return Response(response_dict)

    def delete(self, request, pk=None):
        # if request.user.is_superuser :
        if request:
            try:
                m.Party.objects.get(id=pk).delete()
                response_dict = {"error": False,
                                "message": "Successfully Deleted"}
            except:
                response_dict = {"error": True,
                                "message": "Error During Deleted Data "}
        else:
            response_dict = {
                "error": True, "message": 'UnAuthenticated Person'}
        return Response(response_dict)

class SalesOfficerViewSet(viewsets.ViewSet):

    def list(self, request):
        # if request.user.is_superuser or p.Accountant(request)
        data = m.SalesOfficer.objects.all()
        serializer = s.SalesOfficerSerializer(
            data, many=True, context={"request": request})
        response_dict = {
            "error": False, "message": "All List Data", "data": serializer.data}
        return Response(response_dict)
    
    def create(self, request):
        try:
            # user
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            name = request.data['name']
            user = User.objects.create_user(username, email, password)
            user.first_name  = name
            user.last_name  = 'Sales Officer'
            grp = Group.objects.get(name=g.SalesOfficer.value)
            user.groups.add(grp)
            
            # SalesOfficer
            commission = request.data['commission']
            contact = request.data['contact']
            opening_Balance = request.data['opening_Balance']
            m.SalesOfficer(name=name,commission=commission,contact=contact,opening_Balance=opening_Balance,user=user).save()
            user.save()
            
            response_dict = {"error": False,
                            "message": "Data Save Successfully"}
        except ValueError as err:
            response_dict = {"error": True, "message": err}
        except:
            response_dict = {"error": True,
                                "message": "Error During Saving Data"}
        return JsonResponse(response_dict)

    def retrieve(self, request, pk=None):
        queryset = m.SalesOfficer.objects.all()
        query = get_object_or_404(queryset, pk=pk)
        serializer = s.SalesOfficerSerializer(
            query, context={"request": request})
        serializer_data = serializer.data
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})
       

    def update(self, request, pk=None):
        try:
            queryset = m.SalesOfficer.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            request.data['user'] = query.user.id
            query.user.username =  request.data['username'] 
            query.user.email =  request.data['email']
            if 'password' in request.data:
                query.user.set_password(request.data['password'])
                print('Here')
            query.user.save() 
            serializer = s.SalesOfficerSerializer(
                query, data=request.data, context={"request": request})
            serializer.is_valid()

            serializer.save()
            response_dict = {"error": False,
                            "message": "Successfully Updated Data"}
        except:
            response_dict = {"error": True,
                            "message": "Error During Updating Data"}
        
        return JsonResponse(response_dict)

    def delete(self, request, pk=None):
        if request.user.is_superuser:
            try:
                m.SalesOfficer.objects.get(id=pk).user.delete()
                response_dict = {"error": False,
                                "message": "Successfully Deleted"}
            except:
                response_dict = {"error": True,
                                "message": "Error During Deleted Data "}
        else:
            response_dict = {"error": True,
                                "message": "Error During Updating Data"}
        return Response(response_dict)

class BankViewSet(viewsets.ViewSet):
    def list(self, request):
        # if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant :
        if request:
            data = m.Bank.objects.all()
            serializer = s.BankSerializer(
                data, many=True, context={"request": request})
            response_dict = {
                "error": False, "message": "All List Data", "data": serializer.data}
        else:
            response_dict = {
                "error": False, "message": 'UnAuthenticated Person'}
        return Response(response_dict)

    def create(self, request):
        # if request.user.is_superuser :
        if request:
            try:
                serializer = s.BankSerializer(
                    data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Data Save Successfully"}
            except ValueError as err:
                dict_response = {"error": True, "message": err}
            except:
                dict_response = {"error": True,
                                "message": "Error During Saving Data"}
        else:
            response_dict = {
                "error": False, "message": 'UnAuthenticated Person'}
        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        # if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant :
        if request:
            queryset = m.Bank.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.BankSerializer(
                query, context={"request": request})
            serializer_data = serializer.data
        
            return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})
        else:
            response_dict = {
                "error": False, "message": 'UnAuthenticated Person'}
        return Response(response_dict)
    
    def update(self, request, pk=None):
        # if request.user.is_superuser:
        if request:
            try:
                queryset = m.Bank.objects.all()
                query = get_object_or_404(queryset, pk=pk)
                serializer = s.BankSerializer(
                    query, data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Successfully Updated Data"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Updating Data"}

            return Response(dict_response)
        else:
            response_dict = {
                "error": False, "message": 'UnAuthenticated Person'}
        return Response(response_dict)

    def delete(self, request, pk=None):
        # if request.user.is_superuser :
        if request:
            try:
                m.Bank.objects.get(id=pk).delete()
                response_dict = {"error": False,
                                "message": "Successfully Deleted"}
            except:
                response_dict = {"error": True,
                                "message": "Error During Deleted Data "}
        else:
            response_dict = {
                "error": False, "message": 'UnAuthenticated Person'}
        return Response(response_dict)


class CategoryViewSet(viewsets.ViewSet):

    def list(self, request):
        # if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant(request):
        if request:
            data = m.Category.objects.all()
            serializer = s.CategorySerializer(
                data, many=True, context={"request": request})
            response_dict = {
                "error": False, "message": "All List Data", "data": serializer.data}
            return Response(response_dict)
        
    def create(self, request):
        # if request.user.is_superuser :
        if request:
            try:
                serializer = s.CategorySerializer(
                    data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Data Save Successfully"}
            except ValueError as err:
                dict_response = {"error": True, "message": err}
            except:
                dict_response = {"error": True,
                                "message": "Error During Saving Data"}

        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        # if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant(request):
        if request:
            queryset = m.Category.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.CategorySerializer(
                query, context={"request": request})
            serializer_data = serializer.data
            return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
        # if request.user.is_superuser :
        if request:
            try:
                queryset = m.Category.objects.all()
                query = get_object_or_404(queryset, pk=pk)
                serializer = s.CategorySerializer(
                    query, data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Successfully Updated Data"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Updating Data"}

        return Response(dict_response)

    def delete(self, request, pk=None):
        # if request.user.is_superuser:
        if request:
            try:
                m.Category.objects.get(id=pk).delete()
                dict_response = {"error": False,
                                "message": "Successfully Deleted"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Deleted Data "}

        return Response(dict_response)

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        # if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant(request):
        data = m.Product.objects.all()
        serializer = s.ProductSerializer(
            data, many=True, context={"request": request})
        response_dict = {
            "error": False, "message": "All List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        if request:
            try:
                serializer = s.ProductSerializer(
                    data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Data Save Successfully"}
            except ValueError as err:
                dict_response = {"error": True, "message": err}
            except:
                dict_response = {"error": True,
                                "message": "Error During Saving Data"}

        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        if request:  
            queryset = m.Product.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.ProductSerializer(
                query, context={"request": request})
            serializer_data = serializer.data
            return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
        try:
            queryset = m.Product.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.ProductSerializer(
                query, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False,
                            "message": "Successfully Updated Data"}
        except:
            dict_response = {"error": True,
                            "message": "Error During Updating Data"}

        return Response(dict_response)

    def delete(self, request, pk=None):
        try:
            m.Product.objects.get(id=pk).delete()
            dict_response = {"error": False,
                            "message": "Successfully Deleted"}
        except:
            dict_response = {"error": True,
                            "message": "Error During Deleted Data "}
        return Response(dict_response)

class DiscountCategoryViewSet(viewsets.ViewSet):

    def list(self, request):
        data = m.DiscountCategory.objects.all()
        serializer = s.DiscountCategorySerializer(
            data, many=True, context={"request": request})
        response_dict = {"error": False, "message": "All List Data", "data": serializer.data}
        return Response(response_dict)
    
    def create(self, request):
        # if request.user.is_superuser:
        if request:
            try:
                serializer = s.DiscountCategorySerializer(
                    data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Data Save Successfully"}
            except ValueError as err:
                dict_response = {"error": True, "message": err}
            except:
                dict_response = {"error": True,
                                "message": "Error During Saving Data"}

            return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        # if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant(request):
        if request:
            queryset = m.DiscountCategory.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.DiscountCategorySerializer(
                query, context={"request": request})
            serializer_data = serializer.data
            return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
        # if request.user.is_superuser:
        if request:
            try:
                queryset = m.DiscountCategory.objects.all()
                query = get_object_or_404(queryset, pk=pk)
                serializer = s.DiscountCategorySerializer(
                    query, data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Successfully Updated Data"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Updating Data"}

            return Response(dict_response)

    def delete(self, request, pk=None):
        # if request.user.is_superuser:
        if request:
            try:
                m.DiscountCategory.objects.get(id=pk).delete()
                dict_response = {"error": False,
                                "message": "Successfully Deleted"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Deleted Data "}

            return Response(dict_response)

class PartyOrderViewSet(viewsets.ViewSet):

    def list(self, request):
        if (request.user.groups.first().name == g.Dispatcher.value):
            data = m.PartyOrder.objects.filter(Q(status='Confirmed')| Q(status='Delivered') )
        elif (request.user.groups.first().name == g.SalesOfficer.value):
            data = m.PartyOrder.objects.filter(sale_officer__user=request.user)
        else:    
            data = m.PartyOrder.objects.all()
        serializer = s.PartyOrderSerializer(
            data.order_by('-id'), many=True, context={"request": request})
        response_dict = {
            "error": False, "message": "All List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = s.PartyOrderSerializer(
                data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False,
                            "message": "Data Save Successfully","data":serializer.data}
        except ValueError as err:
            dict_response = {"error": True, "message": err}
        except:
            dict_response = {"error": True,
                            "message": "Error During Saving Data"}

        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        # if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant(request):
        queryset = m.PartyOrder.objects.all()
        query = get_object_or_404(queryset, pk=pk)
        serializer = s.PartyOrderSerializer(
            query, context={"request": request})
        serializer_data = serializer.data
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
        try:
            if (request.user.groups.first().name == g.Dispatcher.value):
                return Response({"error": True,
                                "message": "Un Athneticated"})
            queryset = m.PartyOrder.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.PartyOrderSerializer(
                query, data=request.data, context={"request": request})
            serializer.is_valid()
            m.PartyOrderProduct.objects.filter(party_order__id=pk).delete()

            for p in request.data['products']:
                m.PartyOrderProduct(party_order=query,
                                    product=m.Product.objects.get(name=p['product']['name']),
                                    qty=p['qty'],
                                    rate=p['rate']).save()
            
                
            serializer.save()
            dict_response = {"error": False,
                            "message": "Successfully Updated Data"}
        except:
            dict_response = {"error": True,
                            "message": "Error During Updating Data"}

        return Response(dict_response)

    def delete(self, request, pk=None):
        if (request.user.groups.first().name == g.Dispatcher.value):
            return Response({"error": True,"message": "Un Athneticated"})
        po = m.PartyOrder.objects.get(id=pk)
        if po.status == 'Delivered':
            m.DispatchTable.objects.get(party_order=po).delete()
        po.delete()
        pop = m.PartyOrderProduct.objects.filter(party_order=po)
        for i in pop:
            i.delete()
        dict_response = {"error": False,
                        "message": "Successfully Deleted"}
        return Response(dict_response)

class DispatchTableViewSet(viewsets.ViewSet):

    def list(self, request):
        data = m.DispatchTable.objects.all()
        serializer = s.DispatchTableSerializer(
            data, many=True, context={"request": request})

        response_dict = {
            "error": False, "message": "All List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        # if request.user.is_superuser or p.SalesOfficer(request):
        try:
            bulty_no = request.data['bulty_no']
            cell_no = request.data['cell_no']
            driver = request.data['driver']
            vehical_no = request.data['vehical_no']
            freight = request.data['freight']
            gate_pass = request.data['gate_pass']
            locations = request.data['locations']
            party_order = request.data['party_order']
            pt = m.PartyOrder.objects.get(id=int(party_order))
            dt = m.DispatchTable(cell_no=cell_no,bulty_no=bulty_no,driver=driver,
            vehical_no=vehical_no,freight=freight,gate_pass=gate_pass,
            locations=locations,party_order=pt)
            pt.freight = int(freight)
            pt.status = 'Delivered'
            pt.save()
            dt.save()
            dict_response = {"error": False,
                            "message": "Data Save Successfully","data":request.data}
        except ValueError as err:
            dict_response = {"error": True, "message": err}
        except:
            dict_response = {"error": True,
                            "message": "Error During Saving Data"}

        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        query = m.DispatchTable.objects.get(party_order__id=pk)
        serializer = s.DispatchTableSerializer(
            query, context={"request": request})
        serializer_data = serializer.data
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
        if request.user.is_superuser or p.SalesOfficer(request):
            try:
                query = m.DispatchTable.objects.get(party_order__id=pk)
                serializer = s.DispatchTableSerializer(
                    query, data=request.data, context={"request": request})
                serializer.is_valid()
                serializer.save()
                dict_response = {"error": False,
                                "message": "Successfully Updated Data"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Updating Data"}

            return Response(dict_response)

    def delete(self, request, pk=None):
        # if request.user.is_superuser or p.SalesOfficer(request):
        # try:
        m.DispatchTable.objects.get(id=pk).delete()
        dict_response = {"error": False,
                        "message": "Successfully Deleted"}
        # except:
        #     dict_response = {"error": True,
        #                     "message": "Error During Deleted Data "}

        return Response(dict_response)

class PartyOrderProductViewSet(viewsets.ViewSet):

    def list(self, request):
        data = m.PartyOrderProduct.objects.all()
        serializer = s.PartyOrderProductSerializer(
            data, many=True, context={"request": request})
        print(pd)
        response_dict = {
            "error": False, "message": "All List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        try:
            serializer = s.PartyOrderProductSerializer(
                data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            print(serializer.errors)
            serializer.save()
            dict_response = {"error": False,
                            "message": "Data Save Successfully"}
        except ValueError as err:
            dict_response = {"error": True, "message": err}
        except:
            dict_response = {"error": True,
                            "message": "Error During Saving Data"}

        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant(request):
            queryset = m.PartyOrderProduct.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.PartyOrderProductSerializer(
                query, context={"request": request})
            serializer_data = serializer.data
            return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
            try:
                queryset = m.PartyOrderProduct.objects.all()
                query = get_object_or_404(queryset, pk=pk)
                serializer = s.PartyOrderProductSerializer(
                    query, data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Successfully Updated Data"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Updating Data"}

            return Response(dict_response)

    def delete(self, request, pk=None):
        if request.user.is_superuser or p.SalesOfficer(request):
            try:
                m.PartyOrderProduct.objects.get(id=pk).delete()
                dict_response = {"error": False,
                                "message": "Successfully Deleted"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Deleted Data "}

            return Response(dict_response)

class RecoveryViewSet(viewsets.ViewSet):

    def list(self, request):
        if (request.user.groups.first().name == g.SalesOfficer.value):
            data = m.Recovery.objects.filter(sale_officer__user=request.user).order_by('-id')
        else:
            data = m.Recovery.objects.all()
        serializer = s.RecoverySerializer(
            data, many=True, context={"request": request})
        response_dict = {
            "error": False, "message": "All List Data", "data": serializer.data}
        return Response(response_dict)

    def create(self, request):
        # if request.user.is_superuser or p.SalesOfficer(request):
        if request:
            # try:
            serializer = s.RecoverySerializer(
                data=request.data, context={"request": request})
            print(request.data)
            serializer.is_valid(raise_exception=True)
            # print(serializer.errors)
            serializer.save()
            print(serializer.errors)
            dict_response = {"error": False,
                            "message": "Data Save Successfully"}
            # except ValueError as err:
            #     dict_response = {"error": True, "message": err}
            # except:
            #     dict_response = {"error": True,
            #                     "message": "Error During Saving Data"}

        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        # if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant(request):
        if request:
            queryset = m.Recovery.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.RecoverySerializer(
                query, context={"request": request})
            serializer_data = serializer.data
            return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
        # if request.user.is_superuser or p.SalesOfficer(request) or p.Accountant(request):
        # try:
        queryset = m.Recovery.objects.all()
        query = get_object_or_404(queryset, pk=pk)
        serializer = s.RecoverySerializer(
            query, data=request.data, context={"request": request})
        serializer.is_valid()
        print(serializer.errors)
        serializer.save()
        dict_response = {"error": False,
                        "message": "Successfully Updated Data"}
        # except:
        #     dict_response = {"error": True,
        #                     "message": "Error During Updating Data"}

        return Response(dict_response)

    def delete(self, request, pk=None):
        try:
            m.Recovery.objects.get(id=pk).delete()
            dict_response = {"error": False,
                            "message": "Successfully Deleted"}
        except:
            dict_response = {"error": True,
                            "message": "Error During Deleted Data "}

            return Response(dict_response)

class SalesOfficerReceivingViewSet(viewsets.ViewSet):

    def list(self, request):
        if request.user.is_superuser:
            data = m.SalesOfficerReceiving.objects.all()
            serializer = s.SalesOfficerReceivingSerializer(
                data, many=True, context={"request": request})
            response_dict = {
                "error": False, "message": "All List Data", "data": serializer.data}
            return Response(response_dict)

    def create(self, request):
        if request.user.is_superuser :
            try:
                serializer = s.SalesOfficerReceivingSerializer(
                    data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Data Save Successfully"}
            except ValueError as err:
                dict_response = {"error": True, "message": err}
            except:
                dict_response = {"error": True,
                                "message": "Error During Saving Data"}

        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        if request.user.is_superuser:
            queryset = m.SalesOfficerReceiving.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.SalesOfficerReceivingSerializer(
                query, context={"request": request})
            serializer_data = serializer.data
            return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self, request, pk=None):
        if request.user.is_superuser :
            try:
                queryset = m.SalesOfficerReceiving.objects.all()
                query = get_object_or_404(queryset, pk=pk)
                serializer = s.SalesOfficerReceivingSerializer(
                    query, data=request.data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                dict_response = {"error": False,
                                "message": "Successfully Updated Data"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Updating Data"}

            return Response(dict_response)

    def delete(self, request, pk=None):
        if request.user.is_superuser:
            try:
                m.SalesOfficerReceiving.objects.get(id=pk).delete()
                dict_response = {"error": False,
                                "message": "Successfully Deleted"}
            except:
                dict_response = {"error": True,
                                "message": "Error During Deleted Data "}

            return Response(dict_response)

class DispatchViewSet(viewsets.ViewSet):
    def list(self, request):
        try:

            data = User.objects.filter(groups__name=g.Dispatcher.value)
            serializer = s.UsersSerializer(data, many=True, context={"request": request})
            response_dict = {"error": False, "message": "All List Data", "data": serializer.data}
        except:
            response_dict = {"error": False, "message": 'UnAuthenticated Person'}
        return Response(response_dict)

    def create(self, request):
        try:
            name = request.data['name']
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            user = User.objects.create_user(username, email, password)
            user.first_name = name
            user.last_name = 'Dispacther'
            grp = Group.objects.get(name=g.Dispatcher.value)
            user.groups.add(grp)
            user.save()
            dict_response = {"error": False,"message": "Data Save Successfully"}
        except ValueError as err:
            dict_response = {"error": True, "message": err}
        except:
            dict_response = {"error": True,"message": "Error During Saving Data"}
        
        return JsonResponse(dict_response)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        query = get_object_or_404(queryset, pk=pk)
        serializer = s.UsersSerializer(
            query, context={"request": request})
        serializer_data = serializer.data
        
        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})
        
    
    def update(self, request, pk=None):
        try:
            queryset = User.objects.all()
            query = get_object_or_404(queryset, pk=pk)
            serializer = s.UsersSerializer(
                query, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response = {"error": False,
                            "message": "Successfully Updated Data"}
        except:
            dict_response = {"error": True,
                            "message": "Error During Updating Data"}

        return Response(dict_response)

    def delete(self, request, pk=None):
        try:
            m.User.objects.get(id=pk).delete()
            response_dict = {"error": False,
                            "message": "Successfully Deleted"}
        except:
            response_dict = {"error": True,
                            "message": "Error During Deleted Data "}
       
        return Response(response_dict)

# Post 
class GenratePartOrder(viewsets.ViewSet):
    def create(self, request):
        try:
            party_order = request.data['party_order']
            serializer = s.PartyOrderSerializer(
                    data=party_order, context={"request": request})
            serializer.is_valid()
            pt = serializer.save()
            products = request.data['products']
            for product in products:
                save_dict = {
                    'party_order': pt.id,
                    'product': product['product_id'],
                    'qty':  product['qty'],
                    'rate': product['rate']
                }
                try:
                    serializer = s.PartyOrderProductSerializer(
                            data=save_dict, context={"request": request})
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except:
                    m.PartyOrderProduct.objects.get(party_order__id=save_dict['party_order']).delete()
                    dict_response = {"error": True,
                            "message": "Error in Saving Product"}
    
            recovery = request.data['recovery']
            if recovery['amount']:
                if (int(recovery['amount']) > 0 or recovery['amount'] != None):
                    recovery['party_order'] = pt.id
                    print(recovery)
                    try:
                        serializer = s.RecoverySerializer(
                            data=recovery, context={"request": request})
                        serializer.is_valid()
                        serializer.save()
                    except:
                        pt.delete()
                   
            dict_response = {"error": False,
                                "message": "Data Save Successfully"}
        except ValueError as err:
            dict_response = {"error": True, "message": err}
        except:
            dict_response = {"error": True,
                            "message": "Error During Saving Data"}

        return Response(dict_response)

class LedgerAdjustments(viewsets.ViewSet):
    def create(self, request):
        try:
            reciverLgType = request.data['reciverLgType']
            reciverheader = request.data['reciverheader']
            reciverPaymentType = request.data['reciverPaymentType']
            reciverDescription = request.data['reciverDescription']
            # To
            senderLgType = request.data['senderLgType']
            senderheader = request.data['senderheader']
            senderPaymentType = request.data['senderPaymentType']
            senderDescription = request.data['senderDescription']
            amount = request.data['senderAmount']
            reciver_lg = GetLegder(reciverLgType,reciverheader,reciverDescription,float(amount),reciverPaymentType);
            sender_lg = GetLegder(senderLgType,senderheader,senderDescription,float(amount),senderPaymentType);
            
            reciver_lg.save()
            sender_lg.save()
            dict_response = {"error": False,
                            "message": "Successfuly saved"}
        except:
            dict_response = {"error": True,
                            "message": "Error During Saving Data"}
        return Response(dict_response)
    
# Change Status

def ChangePartyOrderStatus(request,id):
    # if request.user.is_superuser or p.Accountant(request):
    try:
        pt = m.PartyOrder.objects.get(id=id)
        if pt.status == 'Pending':
            pt.status = 'Confirmed'
            pt.save()
        elif pt.status == 'Confirmed':
            pt.status = 'Delivered'
            pt.save()
        return JsonResponse({'error':False,'data':'Successfuly Updated'})
    except:
        return JsonResponse({'error':True,'data':'Something went"s wrong'})
    
def ResetPartyOrderStatus(request,id):
    # if request.user.is_superuser or p.Accountant(request):
    # try:
    pt = m.PartyOrder.objects.get(id=id)
    if pt.status == 'Delivered':
        pl = m.PartyLedger.objects.get(id=pt.pl.id)
        pl2 = m.PartyLedger.objects.get(id=pt.plc1.id)
        pl3 = m.PartyLedger.objects.get(id=pt.plc2.id)
        dl = m.DiscountLedger.objects.get(id=pt.dl.id)
        pt.status = 'Pending'
        pt.save()
        pl.delete()
        pl2.delete()
        pl3.delete()
        dl.delete()
    elif pt.status == 'Confirmed':
        pl1= pt.pl
        pl2  = pt.plc1
        pl3 = pt.plc2
        sol = pt.sol
        sl = pt.sl
        il = pt.il
        fl = pt.fl
        pt.status = 'Pending'
        pt.save()
        pl1.delete()
        pl2.delete()
        pl3.delete()
        sol.delete()
        sl.delete()
        il.delete()
        fl.delete()

    return JsonResponse({'error':False,'data':'Successfuly Reset'})
    # except:
    #     return JsonResponse({'error':True,'data':'Something went"s wrong'})
 

def RecoveryStatusChange(request,id):
    try:
        r = m.Recovery.objects.get(id=id)
        r.status = 'Approved'
        r.save()
        return JsonResponse({'error':False,'data':'Successfuly Updated'})
    except:
        return JsonResponse({'error':True,'data':'Something went"s wrong'})

# Ledger View
class PartyLedgerFilter(generics.ListAPIView):
    
    serializer_class = s.PartyLedgerSerializer

    def get_queryset(self):
        f_date = self.kwargs['FromDate']
        t_date = self.kwargs['ToDate']
        party = self.kwargs['party']
        return m.PartyLedger.objects.filter(party=party, date__lte=t_date, date__gte=f_date)

class SalesOfficerLedgerFilter(generics.ListAPIView):
    serializer_class = s.SalesOfficerLedgerSerializer

    def get_queryset(self):
        f_date = self.kwargs['FromDate']
        t_date = self.kwargs['ToDate']
        sales_officer = self.kwargs['sales_officer']
        return m.SalesOfficerLedger.objects.filter(sales_officer=sales_officer, date__lte=t_date, date__gte=f_date)

class ClearingLedgerFilter(generics.ListAPIView):
    serializer_class = s.ClearingLedgerSerializer

    def get_queryset(self):
        f_date = self.kwargs['FromDate']
        t_date = self.kwargs['ToDate']
        return m.ClearingLedger.objects.filter(date__lte=t_date, date__gte=f_date)

class CashLedgerFilter(generics.ListAPIView):
    serializer_class = s.CashLedgerSerializer

    def get_queryset(self):
        f_date = self.kwargs['FromDate']
        t_date = self.kwargs['ToDate']
        return m.CashLedger.objects.filter(date__lte=t_date, date__gte=f_date)

class SalesLedgerFilter(generics.ListAPIView):
    serializer_class = s.SalesLedgerSerializer

    def get_queryset(self):
        f_date = self.kwargs['FromDate']
        t_date = self.kwargs['ToDate']
        return m.SalesLedger.objects.filter(date__lte=t_date, date__gte=f_date)

class FreightLedgerFilter(generics.ListAPIView):
    serializer_class = s.FreightLedgerSerializer

    def get_queryset(self):
        f_date = self.kwargs['FromDate']
        t_date = self.kwargs['ToDate']
        return m.FreightLedger.objects.filter(date__lte=t_date, date__gte=f_date)

class DiscountLedgerFilter(generics.ListAPIView):
    serializer_class = s.DiscountLedgerSerializer

    def get_queryset(self):
        f_date = self.kwargs['FromDate']
        t_date = self.kwargs['ToDate']
        return m.DiscountLedger.objects.filter(date__lte=t_date, date__gte=f_date)

class BankLedgerFilter(generics.ListAPIView):
    serializer_class = s.BankLedgerSerializer

    def get_queryset(self):
        f_date = self.kwargs['FromDate']
        t_date = self.kwargs['ToDate']
        bank = self.kwargs['bank']
        return m.BankLedger.objects.filter(bank=bank, date__lte=t_date, date__gte=f_date)

class IncentiveLedgerFilter(generics.ListAPIView):
    serializer_class = s.IncentiveLedgerSerializer

    def get_queryset(self):
        f_date = self.kwargs['FromDate']
        t_date = self.kwargs['ToDate']
        return m.IncentiveLedger.objects.filter(date__lte=t_date, date__gte=f_date)


# Test

def Test(request):
    party = m.PartyLedger.objects.all()
    salesofficer = m.SalesOfficerLedger.objects.all()
    sales = m.SalesLedger.objects.all()
    bank = m.BankLedger.objects.all()
    freight = m.FreightLedger.objects.all()
    discount = m.DiscountLedger.objects.all()
    cleariing = m.ClearingLedger.objects.all()
    cash = m.CashLedger.objects.all()
    incentive = m.IncentiveLedger.objects.all()
    response_dict = {'Party':party,'SalesOfficer':salesofficer,'Sales':sales,'Bank':bank,'Freight':freight
                    ,'Discount':discount,'Cash':cash,'Clearing':cleariing,'Incentive':incentive }
    return render(request,'test.html',response_dict)

def GetPartyOrderByAmount(request,party,amount):
    party_orders = m.PartyOrder.objects.filter(Q(party__id=party) & Q(pandding_amount__gte=0))
    count = 0
    send = []
    if amount == 0:
        save  = m.PartyOrder.objects.filter(Q(party__id=party) & ~Q(pandding_amount__gte=0)).first()
        if save:
            send.append(save)
    else:
        for i in party_orders:
            count += i.pandding_amount
            send.append(i)
            if count > amount:
                break
    serializer = s.PartyOrderSerializer(
                send, many=True, context={"request": request})
    response_dict = {
                "error": False, "message": "All List Data", "data": serializer.data}
    return JsonResponse(response_dict)
import pandas as pd
@csrf_exempt
def Import(request):
    if request.method == 'POST':
        type = request.POST['type']
        df = pd.read_csv(request.FILES['file'])
        for index, row in df.iterrows():
            if type == 'Discount':
                m.DiscountCategory(name=row['name'],discount=row['discount']).save()
            if type == 'Party':
                so = m.SalesOfficer.objects.get(id=row['SalesOfficer id'])
                dt = m.DiscountCategory.objects.get(id=row['discount id'])
                ct = m.Category.objects.get(id=row['category id'])
                m.Party(name=row['name'],email=row['email'],contact=row['contact'],creditLimit=row['creditLimit'],salesTarget=row['salesTarget'],area=row['area'],sale_officer=so,discount=dt,category=ct,opening_Balance=row['opening_Balance'],ref_id=row['ref_id']).save()
            if type == 'Category':
                m.Category(name=row['name']).save()
            if type == 'Bank':
                m.Bank(name=row['name'],account_no=row['account_no'],opening_Balance=row['opening_Balance']).save()
            if type == 'Product':
                ct = m.Category.objects.get(id=row['category id'])
                m.Product(name=row['name'],type=row['type'],unit=row['unit'],pakage_weight=row['pakage_weight'],sales_price=row['sales_price'],cost_price=row['cost_price'],category=ct).save()
    
    return JsonResponse('Ok',safe=False)

