# -*- coding: utf-8 -*-

from typing import (
    Any,
    List,
)

from eth_typing import (
    HexStr,
)
from eth_typing.abi import TypeStr
from eth_utils import (
    add_0x_prefix,
    remove_0x_prefix,
)
from eth_utils import (
    combomethod,
)
from web3 import (
    Web3 as OriginalWeb3,
)
from web3._utils.encoding import (
    hex_encode_abi_type,
)


class Web3(OriginalWeb3):
    @combomethod
    def solidity_pack(cls, abi_types: List[TypeStr], values: List[Any]) -> str:
        """
        Executes keccak256 exactly as Solidity does.
        Takes list of abi_types as inputs -- `[uint24, int8[], bool]`
        and list of corresponding values  -- `[20, [-1, 5, 0], True]`
        """
        if len(abi_types) != len(values):
            raise ValueError(
                "Length mismatch between provided abi types and values.  Got "
                f"{len(abi_types)} types and {len(values)} values."
            )

        if isinstance(cls, type):
            w3 = None
        else:
            w3 = cls
        normalized_values = cls.normalize_values(w3, abi_types, values)

        hex_string = add_0x_prefix(
            HexStr(
                "".join(
                    remove_0x_prefix(hex_encode_abi_type(abi_type, value))
                    for abi_type, value in zip(abi_types, normalized_values)
                )
            )
        )
        return hex_string
