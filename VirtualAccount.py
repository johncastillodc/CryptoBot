class VirtualAccount:

    def __init__(self):
        self.usd_balance = 1000
        self.btc_amount = 1      ## Should be the number o bitcoins that represent USD$1000 during the right testing year
        self.btc_balance = 1000
        self.btc_price = 0
        self.bought_btc_at = 0
        self.last_transaction_was_sell = False;