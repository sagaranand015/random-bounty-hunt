from pickletools import uint8
from typing import Final

from pyteal import *
from beaker import *


class SamplingContract(Application):

    rnd_number: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.bytes, descr="Just for the storage of Random Number"
    )

    beacon_app_id: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.uint64,
        default=Int(110096026),
        descr="The App ID of the randomness beacon. Should adhere to ARC-21",
    )

    @external(authorize=Authorize.only(Global.creator_address()))
    def configure(self, app_id: abi.Uint64):
        """Allows configuration of the application state values

        Args:
            app_id: The uint64 app id of the beacon app to use
        """
        return Seq(
            self.beacon_app_id.set(app_id.get()),
        )

    @external
    def get_random(self, acct_round: abi.Uint64, *, output: abi.DynamicBytes):
        return Seq(
            (randomness := abi.DynamicBytes()).decode(
                self.get_randomness(acct_round)
            ),
            output.set(randomness),
        )

    @internal(TealType.bytes)
    def get_randomness(self, acct_round: abi.Uint64):
        """requests randomness from random oracle beacon for requested round"""
        return Seq(
            # Prep arguments
            (round := abi.Uint64()).set(acct_round),
            (user_data := abi.make(abi.DynamicArray[abi.Byte])).set([]),
            # Get randomness from oracle
            # (aid := (110096026)),
            InnerTxnBuilder.ExecuteMethodCall(
                app_id=self.beacon_app_id,
                method_signature="must_get(uint64,byte[])byte[]",
                args=[round, user_data],
            ),
            # Remove first 0 bytes (ABI return prefix)
            # and return the rest
            Suffix(InnerTxn.last_log(), Int(0)),
        )

    @create
    def create(self):
        return self.initialize_application_state()

    @update(authorize=Authorize.only(Global.creator_address()))
    def update(self):
        return Approve()

    @opt_in
    def opt_in(self):
        return Approve()


if __name__ == "__main__":
    SamplingContract().dump("./artifacts")
