from pyteal import *
from algosdk.mnemonic import *
from algosdk.future import transaction
from algosdk.atomic_transaction_composer import *
from algosdk.logic import get_application_address
from .sampling import *
from beaker import *
from .constants import *

ACCOUNT_ADDRESS = to_public_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SECRET = to_private_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SIGNER = AccountTransactionSigner(ACCOUNT_SECRET)


def get_algorand_client_ref():
    """
    Returns a handle to the pre-configured algorand client, for interactions with the Algorand Blockchain
    """
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_HOST)
    return algod_client


def get_app_client_ref(app_id: int):
    """
    Returns a handle to the pre-configured algorand APP client for operations on the Sampling App(SC)
    """
    if app_id == 0:
        raise Exception(
            "Please configure the environment with a pre-deployed Algorand APP_ID"
        )

    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_HOST)
    app_client = client.ApplicationClient(
        algod_client, SamplingContract(), signer=ACCOUNT_SIGNER, app_id=app_id
    )
    return app_client
