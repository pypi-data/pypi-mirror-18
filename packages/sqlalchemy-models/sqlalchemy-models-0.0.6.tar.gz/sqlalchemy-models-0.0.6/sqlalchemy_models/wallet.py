"""
SQLAlchemy models for Wallets
"""
from alchemyjsonschema.dictify import datetime_rfc3339

from __init__ import sa, orm, Base, LedgerAmount
from ledger import Amount
import datetime

__all__ = ['Balance', 'Address', 'Credit', 'Debit', 'HWBalance']


class Balance(Base):
    """A user's balance in a single currency. Only the latest record is valid."""
    id = sa.Column(sa.Integer, sa.Sequence('balance_id_seq'), primary_key=True)
    total = sa.Column(LedgerAmount, nullable=False)
    available = sa.Column(LedgerAmount, nullable=False)
    currency = sa.Column(sa.String(4), nullable=False)  # i.e. BTC, DASH, USD
    time = sa.Column(sa.DateTime(), default=datetime.datetime.utcnow)
    reference = sa.Column(sa.String(256), nullable=True)

    # foreign key reference to the owner of this
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('user.id'),
        nullable=False)
    user = orm.relationship("User", foreign_keys=[user_id])

    def __init__(self, total, available, currency, reference, user_id, time=None):
        self.total = total
        self.available = available
        self.currency = currency
        self.reference = reference
        self.user_id = user_id
        self.time = time if time is not None else datetime.datetime.utcnow()
        self.load_commodities()

    def __repr__(self):
        return "<Balance(total=%s, available=%s, currency='%s', reference='%s', user_id=%s, time=%s)>" % (
                   self.total, self.available, self.currency,
                   self.reference, self.user_id, datetime_rfc3339(self.time))

    @orm.reconstructor
    def load_commodities(self):
        """
        Load the commodities for Amounts in this object.
        """
        if isinstance(self.available, Amount):
            self.available = Amount("{0:.8f} {1}".format(self.available.to_double(), self.currency))
        else:
            self.available = Amount("{0:.8f} {1}".format(self.available, self.currency))
        if isinstance(self.total, Amount):
            self.total = Amount("{0:.8f} {1}".format(self.total.to_double(), self.currency))
        else:
            self.total = Amount("{0:.8f} {1}".format(self.total, self.currency))


class Address(Base):
    """A payment network Address or account number."""
    id = sa.Column(sa.Integer, sa.Sequence('address_id_seq'), primary_key=True)
    # i.e. 1PkzTWAyfR9yoFw2jptKQ3g6E5nKXPsy8r, 	XhwWxABXPVG5Z3ePyLVA3VixPRkARK6FKy
    address = sa.Column(sa.String(64), nullable=False)
    currency = sa.Column(sa.String(4), nullable=False)  # i.e. BTC, DASH, USD
    network = sa.Column(sa.String(64), nullable=False)  # i.e. Bitcoin, Dash, Crypto Capital
    address_state = sa.Column(sa.Enum("pending", "active", "blocked", name='address_state'), nullable=False)

    # foreign key reference to the owner of this
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('user.id'),
        nullable=False)
    user = orm.relationship("User", foreign_keys=[user_id])

    def __init__(self, address, currency, network, state, user_id):
        self.address = address
        self.currency = currency
        self.network = network
        self.address_state = state
        self.user_id = user_id


class Credit(Base):
    """A Credit, which adds tokens to a User's Balance."""
    id = sa.Column(sa.Integer, sa.Sequence('credit_id_seq'), primary_key=True)
    amount = sa.Column(LedgerAmount, nullable=False)
    address = sa.Column(sa.String(64),
                        nullable=False)  # i.e. 1PkzTWAyfR9yoFw2jptKQ3g6E5nKXPsy8r, XhwWxABXPVG5Z3ePyLVA3VixPRkARK6FKy
    currency = sa.Column(sa.String(4), nullable=False)  # i.e. BTC, DASH, USD
    network = sa.Column(sa.String(64), nullable=False)  # i.e. Bitcoin, Dash, Crypto Capital
    transaction_state = sa.Column(sa.Enum("unconfirmed", "complete", "error", "canceled", name='transaction_state'), nullable=False)
    reference = sa.Column(sa.String(256), nullable=True)  # i.e. invoice#1
    ref_id = sa.Column(sa.String(256), nullable=False,
                       unique=True)  # i.e. 4cef42f9ff334b9b11bffbd9da21da54176103d92c1c6e4442cbe28ca43540fd:0
    time = sa.Column(sa.DateTime(), nullable=False)

    # foreign key reference to the owner of this
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('user.id'),
        nullable=False)
    user = orm.relationship("User", foreign_keys=[user_id])

    def __init__(self, amount, address, currency, network, transaction_state, reference, ref_id, user_id, time):
        self.amount = amount
        self.address = address
        self.currency = currency
        self.network = network
        self.transaction_state = transaction_state
        self.reference = reference
        self.ref_id = ref_id
        self.user_id = user_id
        # self.time = pytz.utc.localize(time)
        self.time = time.replace(tzinfo=None)
        self.load_commodities()

    def __repr__(self):
        return "<Credit(amount=%s, address='%s', currency='%s', network='%s', transaction_state='%s', reference='%s', " \
               "ref_id='%s', time=%s)>" % (
                   self.amount, self.address, self.currency, self.network,
                   self.transaction_state, self.network, self.ref_id, datetime_rfc3339(self.time))

    def get_ledger_entry(self):
        date = self.time.strftime('%Y/%m/%d %H:%M:%S')
        ledger = "%s %s %s %s\n" % (date, self.reference, 'credit', self.currency)
        ledger += "    Assets:{0}:{1}:credit    {2}\n".format(self.network, self.currency, self.amount)
        ledger += "    Equity:Wallet:{0}:debit   {1}\n".format(self.currency, -self.amount)
        ledger += "\n"
        return ledger

    @orm.reconstructor
    def load_commodities(self):
        """
        Load the commodities for Amounts in this object.
        """
        if isinstance(self.amount, Amount):
            self.amount = Amount("{0:.8f} {1}".format(self.amount.to_double(), self.currency))
        else:
            self.amount = Amount("{0:.8f} {1}".format(self.amount, self.currency))


class Debit(Base):
    """A Debit, which subtracts tokens from a User's Balance."""
    id = sa.Column(sa.Integer, sa.Sequence('debit_id_seq'), primary_key=True)
    amount = sa.Column(LedgerAmount, nullable=False)
    fee = sa.Column(LedgerAmount, nullable=False)
    address = sa.Column(sa.String(64), nullable=False)  # i.e. 1PkzTWAyfR9yoFw2jptKQ3g6E5nKXPsy8r,  XhwWxABXPVG5Z3ePyLVA3VixPRkARK6FKy
    currency = sa.Column(sa.String(4), nullable=False)  # i.e. BTC, DASH, USDT
    network = sa.Column(sa.String(64), nullable=False)  # i.e. Bitcoin, Dash, Crypto Capital
    transaction_state = sa.Column(sa.Enum("unconfirmed", "complete", "error", "canceled", name='transaction_state'), nullable=False)
    reference = sa.Column(sa.String(256), nullable=True)  # i.e. invoice#1
    ref_id = sa.Column(sa.String(256),
                       nullable=False)  # i.e. 4cef42f9ff334b9b11bffbd9da21da54176103d92c1c6e4442cbe28ca43540fd
    time = sa.Column(sa.DateTime(), nullable=False)

    # foreign key reference to the owner of this
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('user.id'),
        nullable=False)
    user = orm.relationship("User", foreign_keys=[user_id])

    def __init__(self, amount, fee, address, currency, network, transaction_state, reference, ref_id, user_id, time):
        self.amount = abs(amount)
        self.fee = abs(fee)
        self.address = address
        self.currency = currency
        self.network = network
        self.transaction_state = transaction_state
        self.reference = reference
        self.ref_id = ref_id
        self.user_id = user_id
        # self.time = pytz.utc.localize(time)
        self.time = time.replace(tzinfo=None)
        self.load_commodities()

    def __repr__(self):
        return "<Debit(amount=%s, fee=%s, address='%s', currency='%s', network='%s', transaction_state='%s', reference='%s', " \
               "ref_id='%s', time=%s)>" % (
                   self.amount, self.fee, self.address,
                   self.currency, self.network, self.transaction_state,
                   self.reference, self.ref_id, datetime_rfc3339(self.time))

    def get_ledger_entry(self):
        date = self.time.strftime('%Y/%m/%d %H:%M:%S')
        ledger = "%s %s %s %s\n" % (date, self.reference, 'debit', self.currency)
        assert self.amount > 0
        ledger += "    Assets:{0}:{1}:debit    {2}\n".format(self.network, self.currency, -self.amount)
        if self.fee > 0:
            ledger += "    Equity:Wallet:{0}:credit   {1}\n".format(self.currency, self.amount - self.fee)
            ledger += "    Expenses:MinerFee   {0}\n".format(self.fee)
        else:
            ledger += "    Equity:Wallet:{0}:credit   {1}\n".format(self.currency, self.amount)
        ledger += "\n"
        return ledger

    @orm.reconstructor
    def load_commodities(self):
        """
        Load the commodities for Amounts in this object.
        """
        if isinstance(self.fee, Amount):
            self.fee = Amount("{0:.8f} {1}".format(self.fee.to_double(), self.currency))
        else:
            self.fee = Amount("{0:.8f} {1}".format(self.fee, self.currency))
        if isinstance(self.amount, Amount):
            self.amount = Amount("{0:.8f} {1}".format(self.amount.to_double(), self.currency))
        else:
            self.amount = Amount("{0:.8f} {1}".format(self.amount, self.currency))


class HWBalance(Base):
    """A Hot Wallet Balance, for internal use only"""
    id = sa.Column(sa.Integer, sa.Sequence('hwbalance_id_seq'), primary_key=True)
    available = sa.Column(LedgerAmount, nullable=False)
    total = sa.Column(LedgerAmount, nullable=False)
    currency = sa.Column(sa.String(4), nullable=False)  # i.e. BTC, DASH, USDT
    network = sa.Column(sa.String(64), nullable=False)  # i.e. Bitcoin, Dash, Crypto Capital
    time = sa.Column(sa.DateTime(), default=datetime.datetime.utcnow)

    def __init__(self, available, total, currency, network):
        self.available = available
        self.total = total
        self.currency = currency
        self.network = network
        self.load_commodities()

    @orm.reconstructor
    def load_commodities(self):
        """
        Load the commodities for Amounts in this object.
        """
        if isinstance(self.available, Amount):
            self.available = Amount("{0:.8f} {1}".format(self.available.to_double(), self.currency))
        else:
            self.available = Amount("{0:.8f} {1}".format(self.available, self.currency))
        if isinstance(self.total, Amount):
            self.total = Amount("{0:.8f} {1}".format(self.total.to_double(), self.currency))
        else:
            self.total = Amount("{0:.8f} {1}".format(self.total, self.currency))
