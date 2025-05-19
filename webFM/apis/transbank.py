# apis/transbank.py
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from django.conf import settings

# Configura la instancia de Webpay
options = WebpayOptions(
    commerce_code=settings.TRANSBANK_COMMERCE_CODE,
    api_key=settings.TRANSBANK_API_KEY,
    integration_type=IntegrationType.TEST
)

transaction = Transaction(options)
