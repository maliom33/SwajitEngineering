from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CreateInvoiceView, ExpenseCategoryViewSet, ExpenseViewSet, FinanceDashboardViewSet, FinancialTransactionViewSet, InvoiceItemViewSet, InvoiceViewSet, PaymentViewSet

router = DefaultRouter()
router.register('invoices', InvoiceViewSet, basename='finance-invoice')
router.register('invoice-items', InvoiceItemViewSet, basename='finance-invoice-item')
router.register('payments', PaymentViewSet, basename='finance-payment')
router.register('expenses', ExpenseViewSet, basename='finance-expense')
router.register('expense-categories', ExpenseCategoryViewSet, basename='finance-expense-category')
router.register('transactions', FinancialTransactionViewSet, basename='finance-transaction')

urlpatterns = router.urls + [
    path('orders/<int:pk>/create-invoice/', CreateInvoiceView.as_view({'post': 'create_invoice'}), name='finance-create-invoice'),
    path('dashboard/', FinanceDashboardViewSet.as_view({'get': 'dashboard'}), name='finance-dashboard'),
]