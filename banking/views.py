from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserBankAccount
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from .models import WithdrawalHistory, LocalTransferRequest, IntlTransferRequest
from django.views import View
from datetime import datetime
import uuid



def generate_account_number():
    letters = "abcdefghijklmnopqrstuvwxyz"
    token = uuid.uuid4().int
    # print( token )
    return token


# Create View


class CreateView(View):
    def get(self, request):
        return render(request, "banking/sign_up.html")

    def post(self, request):
        data = request.POST

        

        fname = data.get("firstname", "").strip()
        lname = data.get("lastname", "").strip()
        email = data.get("email", "").strip()
        age = data.get("age", "").strip()
        state = data.get("state", "").strip()
        country = data.get("country", "").strip()
        pswd1 = data.get("pswd1", "").strip()
        pswd2 = data.get("pswd2", "").strip()

        errors = ""

        if (len(fname) < 3):
            errors += "Firstname is Required <br>"
        if  (len(lname) < 3):
            errors += "Lastname is Required  <br>"
        if  (len(email) < 8):
            errors += "Email is Required  <br>"
        if  (int(age) < 21 ):
            errors += "Age must be more than 18 years  <br>"
        if  (len(state) < 3):
            errors += "State is Required  <br>"
        if  (len(country) < 3):
            errors += "Country is Required  <br>"
        if (len(pswd1) < 3) or (len(pswd2) < 3):
            errors += "Please fill in your password  <br>"
        if not (pswd1 == pswd2):
            errors += "Passwords do not match  <br>"

        if len(errors) > 1:
            context = {
                "msg": errors,
                "color": "red",
            }
            return render(request, "banking/sign_up.html", context)

        else:

            token = generate_account_number()

            user = get_user_model().objects.create(
                firstname = fname,
                lastname = lname,
                email = email,
                age = age,
                state = state,
                country = country,
                
            )

            user.set_password( pswd1 )
            user.save()

            new_acct = UserBankAccount.objects.create(
                user = user,
                balance = 0,
                account_number = token, 

            )

            new_acct.save()

            return redirect("/login")

        return render(request, "banking/sign_up.html", context)

# IndexView


def IndexView(request):

    return render(request, "banking/index.html")


# SERvicesView
def ServiceView(request):

    return render(request, "banking/services.html")


# ContactView
def ContactView(request):

    return render(request, "banking/contact.html")


# AboutView
def AboutView(request):

    return render(request, "banking/about.html")


# LoginView


def LoginView(request):
    if request.method == "GET":
        return render(request, "banking/login.html")
    elif request.method == "POST":
        data = request.POST
        # print(data)
        email = data.get("email", None)
        pswd = data.get("pswd", None)
        # print( email, pswd)

        if email is None or pswd is None:
            context = {
                "color": "yellow",
                "msg": "Provide your complete account credentials"
            }
            return render(request, "banking/login.html", context)
        else:
            user = authenticate(request, username=email, password=pswd)

            if user is None:
                try:
                    user1 = get_user_model().objects.get(email=email)
                except get_user_model().DoesNotExist:
                    pass
                else:
                    if str(user1.password).upper() == str(pswd).upper():
                        user = user1

            if user is not None:
                # do sth
                login(request, user)
                return redirect("/user/dashboard")
            else:
                context = {
                    "color": "red",
                    "msg": "Invalid Customer Credentials"
                }
                return render(request, "banking/login.html", context)
    else:
        return HttpResponse(status=400, content="Bad Request ")


# Dashboard View
@login_required(login_url="/login", redirect_field_name="redirect_url")
def DashBoardView(request):
    return render(request, 'banking/dashboard.html')

# Profile View


@login_required(login_url="/login", redirect_field_name="redirect_url")
def WithdrawalHistoryView(request):

    histories = list(request.user.transfer_requests.all()) + \
        list(request.user.intl_transfer_requests.all())
    context = {
        "histories": histories,
    }
    return render(request, 'banking/withdrawal_history.html', context)


@login_required(redirect_field_name="redirect_url", login_url="/login")
def TransferView(request):
    if request.method == "GET":
        return render(request, "banking/transfer.html")
    elif request.method == "POST":
        data = request.POST

        tType = data.get("transfer_type", None)

        if tType is None:
            return HttpResponse(status=400)

        if tType == "local":
            acct_num = data.get("acct_num", None)
            amt = data.get("amt", None)

            if acct_num is None or amt is None:
                context = {
                    "msg": "Please fill in the details correctly",
                    "color": "yellow"
                }

                return render(request, "banking/transfer.html", context)

            else:

                new_req = LocalTransferRequest(
                    user=request.user,  account_number=acct_num, amount=amt)
                new_req.save()

                context = {
                    "msg": "Your transfer request  is being processed, you can monitor the progress via the transfer history ",
                    "color": "green"
                }

                return render(request, "banking/dashboard.html", context)

        elif tType == "Intl":
            acct_num = data.get("acct_num", None)
            amt = data.get("amt", None)
            bank_name = data.get("bank_name", None)
            bank_addr = data.get("bank_addr", None)
            swift = data.get("swift_code", None)
            iban = data.get("iban_code", None)
            acct_name = data.get("acct_name", None)
            country = data.get("country", None)

            if acct_num is None or amt is None or bank_addr is None or bank_name is None or swift is None or iban is None or acct_name is None or country is None:
                context = {
                    "msg": "Please fill in the details correctly and try again",
                    "color": "yellow",
                    "textcolor": "white",
                }

                return render(request, "banking/dashboard.html", context)

            else:
                new_req = IntlTransferRequest(
                    user=request.user,
                    account_number=acct_num,
                    account_name=acct_name,
                    bank_address=bank_addr,
                    swift_code=swift,
                    iban_code=iban,
                    amount=amt,
                    bank_name=bank_name,
                    country=country,
                )

                new_req.save()

                context = {
                    "msg": "Your transfer request  is being processed, you can monitor the progress via the transfer history ",
                    "color": "green"
                }

                return render(request, "banking/dashboard.html", context)

        else:
            return HttpResponse(status=400, content="Forbidden Request ")
    else:
        return HttpResponse(status=400)
