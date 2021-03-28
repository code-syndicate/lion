from django.urls import path
from .import views


app_name = "banking"

urlpatterns = [

    
    path( 'logout/', views.LogoutView, name = "logout"),
    
    path( 'confirm-transfer/<type>/<id>/', views.ConfirmTransferView.as_view(), name = "confirmtransfer" ),

    path( 'login/', views.LoginView, name = "Loginview "),

    path('create-account/', views.CreateView.as_view(), name = "createview"),
    path( '', views.IndexView, name = "indexview "),

    path( 'our-services/', views.ServiceView, name  = "serviceview"),

    path( 'contact-us/', views.ContactView, name = "contactview"),

    path( 'about-us/', views.AboutView, name = "aboutview"),
    
    path('user/dashboard/', views.DashBoardView, name = "dashboardview"),
    
    path('user/transfer-history/', views.WithdrawalHistoryView, name = "historyview"),
    
    path('user/transfer/', views.TransferView, name = "transferview"),
]