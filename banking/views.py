from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import UserBankAccount
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from .models import WithdrawalHistory, LocalTransferRequest, IntlTransferRequest, AuthCode
from django.views import View
from datetime import datetime
from django.core.mail import send_mail
import uuid


def generate_account_number():
    letters = "abcdefghijklmnopqrstuvwxyz"
    token = uuid.uuid4().int
    # print( token )
    return token


class ConfirmTransferView(View):
    def get(self, request, type,  id):

        context = {
            'tId': id,
            'tType': type,
        }
        # print( "hello pple", context)
        return render(request, "banking/confirmation.html", context)

    def post(self, request, type=None, id=None):
        data = request.POST

        otp = data.get("otp", None)
        transfer_id = data.get("transfer_id", None)
        transfer_type = data.get("transfer_type", None)

        # print( "\n\nEnv", data )

        if otp is None or transfer_type is None or transfer_id is None:
            context = {

                "msg": "Please enter the OTP sent to your mail",
                "color": "yellow",
            }
            return render(request, "banking/confirmation.html", context)

        otp = str(otp.strip())
        transfer_id = str(transfer_id.strip())
        transfer_type = str(transfer_type.strip())

        # print("\n\nOTP ENTERED ", otp, "\n\n")

        # auth part information

        auth = None
        try:
            auth = AuthCode.objects.get(code=otp)
        except AuthCode.DoesNotExist:
            context = {

                "msg": "The  OTP you entered is invalid",
                "color": "red",
            }
            return render(request, "banking/confirmation.html", context)
        else:
            pass

        # lets continue
        # Get the particular transfer pointed by the id and type
        transfer = None
        # print( "\n\nEnvs: ", transfer_type, transfer_id, "\n\n")

        if transfer_type == "local":
            try:
                transfer = LocalTransferRequest.objects.get(tx_ref=transfer_id)
            except LocalTransferRequest.DoesNotExist:
                pass
            else:
                pass
        elif transfer_type == "Intl":
            try:
                transfer = IntlTransferRequest.objects.get(tx_ref=transfer_id)
            except IntlTransferRequest.DoesNotExist:
                pass
            else:
                pass

        if transfer is None:
            context = {

                "msg": "Invalid Reference Code",
                "color": "red",
            }
            return render(request, "banking/confirmation.html", context)

        elif auth.transfer_id == transfer.tx_ref:

            transfer.verified = True
            transfer.save()

            context = {

                "msg": "OTP validated, transfer placed, you can monitor your transfers from the history page",
                "color": "green",
                'text_color': "white",
            }
            return render(request, 'banking/dashboard.html', context)

        else:
            context = {

                "msg": "Invalid OTP",
                "color": "red",
                'text_color' : "white",
            }
            return render(request, "banking/confirmation.html", context)


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
        if (len(lname) < 3):
            errors += "Lastname is Required  <br>"
        if (len(email) < 8):
            errors += "Email is Required  <br>"
        if (int(age) < 21):
            errors += "Age must be more than 18 years  <br>"
        if (len(state) < 3):
            errors += "State is Required  <br>"
        if (len(country) < 3):
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
                firstname=fname,
                lastname=lname,
                email=email,
                age=age,
                state=state,
                country=country,

            )

            user.set_password(pswd1)
            user.save()

            new_acct = UserBankAccount.objects.create(
                user=user,
                balance=0,
                account_number=token,

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


# LOgout
def LogoutView(request):
    logout(request)
    return redirect("/")


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
        tId = None

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

                tId = new_req.tx_ref

                # generate verification code for transfer
                new_code = AuthCode.objects.create(
                    transfer_type="local", transfer_id=tId)
                new_code.save()
                # print("\n\n\nYour OTP is ", new_code.code )

                context = {
                    "msg": "Your transfer request  is being processed, you can monitor the progress via the transfer history ",
                    "color": "green"
                }

                message = 'Hello dear {0}, A transfer transaction has been requested on your account.Enter the code below to proceed.<br> <h3>{1}<h3> <br>Please do not share this with anyone.Thanks for banking with us.'.format(
                    request.user.firstname, new_code.code)

                send_mail(
                    subject="Transfer Request Confirmation for " + str(request.user.email),
                    from_email="Truecitizenbank@gmail.com",
                    recipient_list=[request.user.email, ],
                    message = '',
                    fail_silently=False,
                    html_message= message,
                )

                return redirect(reverse("banking:confirmtransfer",  kwargs={
                    "type": tType, "id": tId
                }))

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

                return render(request, "banking/transfer.html", context)

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

                tId = new_req.tx_ref

                # generate verification code for transfer
                new_code = AuthCode.objects.create(
                    transfer_type="intl", transfer_id=tId)
                new_code.save()
                print("\n\n\nYour OTP is ", new_code.code)

                context = {
                    "msg": "Your transfer request  is being processed, you can monitor the progress via the transfer history ",
                    "color": "green"
                }

                return redirect(reverse("banking:confirmtransfer",  kwargs={
                    "type": tType, "id": tId
                }))

        else:
            return HttpResponse(status=400, content="Forbidden Request ")
    else:
        return HttpResponse(status=400)
