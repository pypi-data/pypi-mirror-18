"""
SQLAlchemy models for Wallets
"""
from __init__ import sa, Base, LedgerAmount

__all__ = ['Quote', 'QuoteRequest', 'Payment']


class QuoteRequest(Base):
    """A Request for a quote to convert one currency to another."""
    __tablename__ = "quote_request"
    __name__ = "quote_request"
    id = sa.Column(sa.Integer, sa.Sequence('quote_request_id_seq'), primary_key=True)
    asset_specified = sa.Column(sa.Enum("in", "out", name='asset_specified'))
    in_amount = sa.Column(LedgerAmount, nullable=False)
    out_amount = sa.Column(LedgerAmount, nullable=False)
    fixed_rate = sa.Column(sa.Boolean, nullable=False)

    out_address = sa.Column(sa.String(80), nullable=False)
    return_address = sa.Column(sa.String(80), nullable=False)

    in_currency = sa.Column(sa.String(4), nullable=False)
    out_currency = sa.Column(sa.String(4), nullable=False)

    def __init__(self, out_address, return_address, in_amount, in_currency, 
                 out_amount, out_currency, fixed_rate=False):
        if in_amount > 0:
            self.in_amount = in_amount
            self.asset_specified = 'in'
            self.out_amount = 0
        elif out_amount > 0:
            self.out_amount = out_amount
            self.asset_specified = 'out'
            self.in_amount = 0
        self.in_currency = in_currency
        self.out_currency = out_currency
        self.out_address = out_address
        self.return_address = return_address
        self.fixed_rate = fixed_rate


class Quote(Base):
    """A Quote to convert one currency to another."""
    __tablename__ = "quote"
    __name__ = "quote"
    id = sa.Column(sa.Integer, sa.Sequence('quote_id_seq'), primary_key=True)
    in_amount = sa.Column(LedgerAmount, nullable=False)
    out_amount = sa.Column(LedgerAmount, nullable=False)
    in_address = sa.Column(sa.String(80), nullable=False)
    out_address = sa.Column(sa.String(80), nullable=False)
    return_address = sa.Column(sa.String(80), nullable=False)
    in_currency = sa.Column(sa.String(4), nullable=False)
    out_currency = sa.Column(sa.String(4), nullable=False)
    rate = sa.Column(LedgerAmount, nullable=False)

    def __init__(self, in_amount, in_currency, 
                 out_amount, out_currency, in_address, out_address, 
                 return_address, rate):
        self.in_amount = in_amount
        self.out_amount = out_amount
        self.in_currency = in_currency
        self.out_currency = out_currency
        self.in_address = in_address
        self.out_address = out_address
        self.return_address = return_address
        self.rate = rate


class Payment(Base):
    """A Payment, reflecting that money was sent out."""
    __tablename__ = "payment"
    __name__ = "payment"
    id = sa.Column(sa.Integer, sa.Sequence('payment_id_seq'), primary_key=True)
    out_amount = sa.Column(LedgerAmount, nullable=False)
    out_address = sa.Column(sa.String(80), nullable=False)
    out_currency = sa.Column(sa.String(4), nullable=False)
    debit_id = sa.Column(sa.Integer, nullable=True)

    def __init__(self, in_amount, in_currency, 
                 out_amount, out_currency, debit_id=None):
        self.in_amount = in_amount
        self.out_amount = out_amount
        self.in_currency = in_currency
        self.out_currency = out_currency
        self.debit_id = debit_id

