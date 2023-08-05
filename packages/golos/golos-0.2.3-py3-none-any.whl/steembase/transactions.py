from collections import OrderedDict
from binascii import hexlify, unhexlify
from calendar import timegm
from datetime import datetime
import json
import struct
import time

from steembase.account import PublicKey
from graphenebase.types import *
from .signedtransactions import Signed_Transaction as GrapheneSigned_Transaction
from .operations import *
from .chains import known_chains

timeformat = '%Y-%m-%dT%H:%M:%S%Z'

chain = "STEEM"
# chain = "TEST"


class Signed_Transaction(GrapheneSigned_Transaction):
    """ Overwrite default chain:
    """
    def __init__(self, *args, **kwargs):
        super(Signed_Transaction, self).__init__(*args, **kwargs)

    def sign(self, wifkeys, chain=chain):
        return super(Signed_Transaction, self).sign(wifkeys, chain)

    def verify(self, pubkey, chain=chain):
        return super(Signed_Transaction, self).verify(pubkey, chain)

"""
    Auxiliary Calls
"""


def getBlockParams(ws) :
    """ Auxiliary method to obtain ``ref_block_num`` and
        ``ref_block_prefix``. Requires a websocket connection to a
        witness node!
    """
    dynBCParams = ws.get_dynamic_global_properties()
    ref_block_num = dynBCParams["head_block_number"] & 0xFFFF
    ref_block_prefix = struct.unpack_from("<I", unhexlify(dynBCParams["head_block_id"]), 4)[0]
    return ref_block_num, ref_block_prefix


def formatTimeFromNow(secs=0) :
    """ Properly Format Time that is `x` seconds in the future

     :param int secs: Seconds to go in the future (`x>0`) or the past (`x<0`)
     :return: Properly formated time for Graphene (`%Y-%m-%dT%H:%M:%S`)
     :rtype: str

    """
    return datetime.utcfromtimestamp(time.time() + int(secs)).strftime(timeformat)
