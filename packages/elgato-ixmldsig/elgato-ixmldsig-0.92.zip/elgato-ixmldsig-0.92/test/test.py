# -*- coding: utf-8 -*-

from ixmldsig import Signer
import pytz
import os

cert_private = os.path.join(os.path.dirname(__file__), 'payee-key.pem')
cert_public = os.path.join(os.path.dirname(__file__), 'payee-cert.pem')
cert_ca = os.path.join(os.path.dirname(__file__), 'elgato-ca-cert.pem')
cert_ca_crl = os.path.join(os.path.dirname(__file__), 'elgato-ca-crl.pem')

directory = '.'
timezone = pytz.timezone("Europe/Sarajevo")

source = 'sample-invoice.xml'
destination = 'signed-invoice.xml'
key_password = 'pearljam'

signer=Signer(directory, cert_private=cert_private, cert_public=cert_public, timezone=timezone,
                    cert_ca=cert_ca, cert_ca_crl=cert_ca_crl)

def evt_handler(result, error=0, end=False):
    print result, error, end

print("Signing")
for s in signer.sign(key_password=key_password, source=source, destination=destination):
    pass

print("Verification")
for s in signer.verify(source=destination):
    pass
