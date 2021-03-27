from django.contrib.admin import AdminSite
from users.models import User
from django.conf import settings
# from django.utils import timezone
# from datetime import timedelta

from users.admin import *
from banking.models import *
from banking.admin import *

class AdminSite1( AdminSite ):
	site_header = 'TRUE CITIZEN BANK ADMINISTRATION'
	site_title = 'True Citizen Bank| Admin'
	index_title = 'Manage bank '
	site_url = 'http://truecitizenbank.com/'



	
admin_site1 = AdminSite1(name='abchina-admin')

admin_site1.register( LocalTransferRequest, LocalTransferRequestAdmin)
admin_site1.register(User,UserAdmin )
admin_site1.register( IntlTransferRequest, IntlTransferRequestAdmin)
admin_site1.register( UserBankAccount, UserBankAccountAdmin)


# Context Processor 
def SiteContext( request ):
	sitename = request.META.get( "HTTP_HOST")
	if settings.DEBUG is True:
		sitename = "http://localhost:8000"

	context = {
		"addr" : sitename,

	}

	return context

