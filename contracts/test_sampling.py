import os
from algosdk.mnemonic import *
from algosdk.future import transaction
from algosdk.atomic_transaction_composer import *
from algosdk.logic import get_application_address
from sampling import *
from beaker import *
import time
from constants import *

ACCOUNT_ADDRESS = to_public_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SECRET = to_private_key(ROOT_ACCOUNT_MNEMONIC)
ACCOUNT_SIGNER = AccountTransactionSigner(ACCOUNT_SECRET)

WAIT_DELAY = 11


def get_create_random_app(app_id: int = 0):
    """
    Creates a store app and returns the appId. If the app_id exists already, return the application address
    """
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_HOST)
    app_client = client.ApplicationClient(
        algod_client, SamplingContract(), signer=ACCOUNT_SIGNER, app_id=app_id
    )

    if app_id == 0:
        # Create  an app client for our app
        app_id, app_addr, _ = app_client.create()
        print(f"Created app at {app_id} {app_addr}")
        app_client.fund(5 * consts.algo)
        print("Funded app")
        app_client.opt_in()
        print("Opted in")
    else:
        app_addr = get_application_address(app_id)

    app_state = app_client.get_application_state()
    print(f"Current app state:{app_state}")
    acct_state = app_client.get_account_state()
    print(f"Current account state:{acct_state}")

    # app_client.call(
    #     RandomContract.configure,
    #     app_id=110096026,
    # )

    sp = algod_client.suggested_params()
    # Add 3 rounds to the first available round to give us a little
    # padding time
    # round = sp.first + 3
    round = sp.first

    # wait an extra couple rounds
    wait_round = round + 10

    sp = algod_client.suggested_params()
    current_round = sp.first

    print(f"Starting at round: {round}, current_round: {current_round}")

    sum = 0
    while current_round < wait_round:
        t1 = time.time()
        algod_client.status_after_block(current_round)
        current_round += 1
        t2 = time.time()
        diff = t2 - t1
        sum = sum + diff
        print(f"Currently at round {current_round}, {t1}, {t2}, diff: {diff}")

    print("======== Average val is: ", sum / 10)

    print("Settling...")
    sp = algod_client.suggested_params()
    sp.flat_fee = True
    sp.fee = 2000  # cover this and 1 inner transaction

    user_data = bytes("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjY4ODAwMDMsImlhdCI6MTY2Njc5MzYwMywic3ViIjoiYW5vdGhlciB0d28ifQ.06WHtumdc4XBKFhrh-Bmf3fEY1Al9Qdc6X93GB3reak", encoding='utf8')

    res = app_client.call(
        SamplingContract.get_random,
        acct_round=round,
        u_data=user_data,
        suggested_params=sp,
        foreign_apps=[110096026],
    )
    print("======== res is: ", res)
    print("======== res.return_value is: ", res.return_value)
    print("======== res.raw_value is: ", res.raw_value)
    print("======== res.tx_id is: ", res.tx_id)
    print("======== res.tx_value is: ", res.tx_info)

    l = len(res.raw_value)
    for i in range(0, l):
        print(f"{res.raw_value[i]}", end=" ")

    # print("======== res.raw_value[0] is: ", res.raw_value[0])
    # print("======== res.raw_value[1] is: ", res.raw_value[1])

    # r = res.raw_value[0].decode('utf-8')
    # (r := TealType.uint64()).decode(res.raw_value)
    # print("========= r is: ", r)


if __name__ == "__main__":

    print("Starting deploy of the Sampling App(SC) on Algorand...")
    # appID: 118533297
    get_create_random_app(118533297)

    # deployed_app_id = int(os.environ["SAMPLING_APP_ID"])
    # if not deployed_app_id:
    #     print("Starting deploy of the Sampling App(SC) on Algorand...")
    #     get_create_random_app()
    # else:
    #     # appID: 118504938
    #     get_create_random_app(deployed_app_id)
