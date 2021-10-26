from django.urls import path, include
from rest_framework import routers
from app import views
router = routers.DefaultRouter()
router.register("Party", views.PartyViewSet, basename="Party")
router.register("SalesOfficer", views.SalesOfficerViewSet, basename="SalesOfficer")
router.register("Dispatcher", views.DispatchViewSet, basename="Dispatcher")
router.register("Bank", views.BankViewSet, basename="Bank")
router.register("Category", views.CategoryViewSet, basename="Category")
router.register("Product", views.ProductViewSet, basename="Product")
router.register("DiscountCategory", views.DiscountCategoryViewSet, basename="DiscountCategory")
router.register("PartyOrder", views.PartyOrderViewSet, basename="PartyOrder")
router.register("DispatchTable", views.DispatchTableViewSet, basename="DispatchTable")
router.register("PartyOrderProduct", views.PartyOrderProductViewSet, basename="PartyOrderProduct")
router.register("Recovery", views.RecoveryViewSet, basename="Recovery")
router.register("GenratePartyOrder", views.GenratePartOrder, basename="GenratePartyOrder")
router.register("LedgerAdjustments", views.LedgerAdjustments, basename="LedgerAdjustments")
# Authentication


urlpatterns = [
    path('', include(router.urls)),
    # Genraet Party Order
    # Ledgers
    path('PartyLedger/<int:party>/<str:FromDate>/<str:ToDate>',views.PartyLedgerFilter.as_view()),
    path('SalesOfficerLedger/<int:sales_officer>/<str:FromDate>/<str:ToDate>',views.SalesOfficerLedgerFilter.as_view()),
    path('ClearingLedger/<str:FromDate>/<str:ToDate>',views.ClearingLedgerFilter.as_view()),
    path('CashLedger/<str:FromDate>/<str:ToDate>',views.CashLedgerFilter.as_view()),
    path('SalesLedger/<str:FromDate>/<str:ToDate>',views.SalesLedgerFilter.as_view()),
    path('FreightLedger/<str:FromDate>/<str:ToDate>',views.FreightLedgerFilter.as_view()),
    path('DiscountLedger/<str:FromDate>/<str:ToDate>',views.DiscountLedgerFilter.as_view()),
    path('BankLedger/<int:bank>/<str:FromDate>/<str:ToDate>',views.BankLedgerFilter.as_view()),
    path('IncentiveLedger/<str:FromDate>/<str:ToDate>',views.IncentiveLedgerFilter.as_view()),
    path('GetPartyOrderByAmount/<int:party>/<int:amount>/',views.GetPartyOrderByAmount),
    # Status Change
    path('ChangePartyOrderStatus/<int:id>/',views.ChangePartyOrderStatus),
    path('ResetPartyOrderStatus/<int:id>/',views.ResetPartyOrderStatus),
    path('AproveRecovery/<int:id>/',views.RecoveryStatusChange),
    # Test
    path('test',views.Test),
    # Import
    path('ImportCSV/',views.Import),


]
