import json
from .types import *
from .objects import *
from .types import *
from .account import PublicKey
from .chains import default_prefix

#: Operation ids
operations = {}
operations["transfer"] = 0
operations["limit_order_create"] = 1
operations["limit_order_cancel"] = 2
operations["call_order_update"] = 3
operations["fill_order"] = 4
operations["account_create"] = 5
operations["account_update"] = 6
operations["account_whitelist"] = 7
operations["account_upgrade"] = 8
operations["account_transfer"] = 9
operations["asset_create"] = 10
operations["asset_update"] = 11
operations["asset_update_bitasset"] = 12
operations["asset_update_feed_producers"] = 13
operations["asset_issue"] = 14
operations["asset_reserve"] = 15
operations["asset_fund_fee_pool"] = 16
operations["asset_settle"] = 17
operations["asset_global_settle"] = 18
operations["asset_publish_feed"] = 19
operations["witness_create"] = 20
operations["witness_update"] = 21
operations["proposal_create"] = 22
operations["proposal_update"] = 23
operations["proposal_delete"] = 24
operations["withdraw_permission_create"] = 25
operations["withdraw_permission_update"] = 26
operations["withdraw_permission_claim"] = 27
operations["withdraw_permission_delete"] = 28
operations["committee_member_create"] = 29
operations["committee_member_update"] = 30
operations["committee_member_update_global_parameters"] = 31
operations["vesting_balance_create"] = 32
operations["vesting_balance_withdraw"] = 33
operations["worker_create"] = 34
operations["custom"] = 35
operations["assert"] = 36
operations["balance_claim"] = 37
operations["override_transfer"] = 38
operations["transfer_to_blind"] = 39
operations["blind_transfer"] = 40
operations["transfer_from_blind"] = 41
operations["asset_settle_cancel"] = 42
operations["asset_claim_fees"] = 43


def getOperationNameForId(i) :
    """ Convert an operation id into the corresponding string
    """
    for key in operations :
        if int(operations[key]) is int(i) :
            return key
    return "Unknown Operation ID %d" % i


class Operation() :
    def __init__(self, op) :
        if isinstance(op, list) and len(op) == 2:
            if isinstance(op[0], int):
                self.opId = op[0]
                name = self.getOperationNameForId(self.opId)
            else:
                self.opId = self.operations().get(op[0], None)
                name = op[0]
                if self.opId is None:
                    raise ValueError("Unknown operation")
            self.name = name[0].upper() + name[1:]  # klassname
            try:
                klass = self._getklass(self.name)
            except:
                raise NotImplementedError("Unimplemented Operation %s" % self.name)
            self.op = klass(op[1])
        else:
            self.op = op
            self.name = type(self.op).__name__.lower()  # also store name
            self.opId = self.operations()[self.name]

    def operations(self):
        return operations

    def getOperationNameForId(self, i) :
        return getOperationNameForId(i)

    def _getklass(self, name):
        module = __import__("graphenebase.operations", fromlist=["operations"])
        class_ = getattr(module, name)
        return class_

    def __bytes__(self) :
        return bytes(Id(self.opId)) + bytes(self.op)

    def __str__(self) :
        return json.dumps([self.opId, self.op.toJson()])


"""
    Actual Operations
"""


class Transfer(GrapheneObject) :
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" in kwargs:
                memo = Optional(Memo(kwargs["memo"]))
            else:
                memo = Optional(None)
            super().__init__(OrderedDict([
                ('fee'       , Asset(kwargs["fee"])),
                ('from'      , ObjectId(kwargs["from"], "account")),
                ('to'        , ObjectId(kwargs["to"], "account")),
                ('amount'    , Asset(kwargs["amount"])),
                ('memo'      , memo),
                ('extensions', Set([])),
            ]))


class Asset_publish_feed(GrapheneObject):
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('publisher', ObjectId(kwargs["publisher"], "account")),
                ('asset_id', ObjectId(kwargs["asset_id"], "asset")),
                ('feed', PriceFeed(kwargs["feed"])),
                ('extensions', Set([])),
            ]))


class Asset_update(GrapheneObject):
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "new_issuer" in kwargs:
                new_issuer = Optional(ObjectId(kwargs["new_issuer"], "account"))
            else:
                new_issuer = Optional(None)
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('issuer', ObjectId(kwargs["issuer"], "account")),
                ('asset_to_update', ObjectId(kwargs["asset_to_update"], "asset")),
                ('new_issuer', new_issuer),
                ('new_options', AssetOptions(kwargs["new_options"])),
                ('extensions', Set([])),
            ]))


class Op_wrapper(GrapheneObject):
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('op', Operation(kwargs["op"])),
            ]))


class Proposal_create(GrapheneObject):
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "review_period_seconds" in kwargs:
                review = Optional(Uint32(kwargs["review_period_seconds"]))
            else:
                review = Optional(None)
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('expiration_time', PointInTime(kwargs["expiration_time"])),
                ('proposed_ops',
                    Array([Op_wrapper(o) for o in kwargs["proposed_ops"]])),
                ('review_period_seconds', review),
                ('extensions', Set([])),
            ]))


class Proposal_update(GrapheneObject):
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            for o in ['active_approvals_to_add',
                      'active_approvals_to_remove',
                      'owner_approvals_to_add',
                      'owner_approvals_to_remove',
                      'key_approvals_to_add',
                      'key_approvals_to_remove']:
                if o not in kwargs:
                    kwargs[o] = []

            super().__init__(OrderedDict([
                ('fee'       ,                  Asset(kwargs["fee"])),
                ('fee_paying_account',          ObjectId(kwargs["fee_paying_account"], "account")),
                ('proposal',                    ObjectId(kwargs["proposal"], "proposal")),
                ('active_approvals_to_add',
                    Array([ObjectId(o, "account") for o in kwargs["active_approvals_to_add"]])),
                ('active_approvals_to_remove',
                    Array([ObjectId(o, "account") for o in kwargs["active_approvals_to_remove"]])),
                ('owner_approvals_to_add',
                    Array([ObjectId(o, "account") for o in kwargs["owner_approvals_to_add"]])),
                ('owner_approvals_to_remove',
                    Array([ObjectId(o, "account") for o in kwargs["owner_approvals_to_remove"]])),
                ('key_approvals_to_add',
                    Array([PublicKey(o) for o in kwargs["key_approvals_to_add"]])),
                ('key_approvals_to_remove',
                    Array([PublicKey(o) for o in kwargs["key_approvals_to_remove"]])),
                ('extensions',                  Set([])),
            ]))


class Limit_order_create(GrapheneObject):
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('seller', ObjectId(kwargs["seller"], "account")),
                ('amount_to_sell', Asset(kwargs["amount_to_sell"])),
                ('min_to_receive', Asset(kwargs["min_to_receive"])),
                ('expiration', PointInTime(kwargs["expiration"])),
                ('fill_or_kill', Bool(kwargs["fill_or_kill"])),
                ('extensions', Set([])),
            ]))


class Limit_order_cancel(GrapheneObject):
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('fee_paying_account', ObjectId(kwargs["fee_paying_account"], "account")),
                ('order', ObjectId(kwargs["order"], "limit_order")),
                ('extensions', Set([])),
            ]))


class Call_order_update(GrapheneObject):
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('funding_account', ObjectId(kwargs["funding_account"], "account")),
                ('delta_collateral', Asset(kwargs["delta_collateral"])),
                ('delta_debt', Asset(kwargs["delta_debt"])),
                ('extensions', Set([])),
            ]))


class Asset_fund_fee_pool(GrapheneObject):
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('from_account', ObjectId(kwargs["from_account"], "account")),
                ('asset_id', ObjectId(kwargs["asset_id"], "asset")),
                ('amount', Int64(kwargs["amount"])),
                ('extensions', Set([])),
            ]))


class Override_transfer(GrapheneObject) :
    def __init__(self, *args, **kwargs) :
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "memo" in kwargs:
                memo = Optional(Memo(kwargs["memo"]))
            else:
                memo = Optional(None)
            super().__init__(OrderedDict([
                ('fee'       , Asset(kwargs["fee"])),
                ('issuer'    , ObjectId(kwargs["issuer"], "account")),
                ('from'      , ObjectId(kwargs["from"], "account")),
                ('to'        , ObjectId(kwargs["to"], "account")),
                ('amount'    , Asset(kwargs["amount"])),
                ('memo'      , memo),
                ('extensions', Set([])),
            ]))


class Account_create(GrapheneObject) :
    def __init__(self, *args, **kwargs) :
        # Allow for overwrite of prefix
        prefix = kwargs.pop("prefix", default_prefix)

        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('fee'              , Asset(kwargs["fee"])),
                ('registrar'        , ObjectId(kwargs["registrar"], "account")),
                ('referrer'         , ObjectId(kwargs["referrer"], "account")),
                ('referrer_percent' , Uint16(kwargs["referrer_percent"])),
                ('name'             , String(kwargs["name"])),
                ('owner'            , Permission(kwargs["owner"], prefix=prefix)),
                ('active'           , Permission(kwargs["active"], prefix=prefix)),
                ('options'          , AccountOptions(kwargs["options"], prefix=prefix)),
                ('extensions'       , Set([])),
            ]))
