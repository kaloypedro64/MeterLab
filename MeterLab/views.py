from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required
from MeterLab.settings import AREA_CHOICES

from Users.models import userarea

MASTER_KEY = "Some-long-base-key-to-use-as-encryption-key"
login_url = 'login'
# Create your views here.


@login_required(login_url=login_url)
def dashboard(request):
    if request.user.is_authenticated:
        transaction_area = userarea.objects.get(userid=request.user.id)
        return render(request, 'dashboard.html', {'transaction_area': AREA_CHOICES[int(transaction_area.area)]})
    else:
        return render(request, 'base/login.html')

def genwrite_key():
    key = Fernet.generate_key()
    with open("pass.key", "wb") as key_file:
        key_file.write(key)


def call_key():
    return open("pass.key", "rb").read()


# def encrypt_val(clear_text):
#     enc_secret = AES.new(MASTER_KEY[:32])
#     tag_string = (str(clear_text) +
#                   (AES.block_size -
#                    len(str(clear_text)) % AES.block_size) * "\0")
#     cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))

#     return cipher_text


# def decrypt_val(cipher_text):
#     dec_secret = AES.new(MASTER_KEY[:32])
#     raw_decrypted = dec_secret.decrypt(base64.b64decode(cipher_text))
#     clear_val = raw_decrypted.decode().rstrip("\0")
#     return clear_val

