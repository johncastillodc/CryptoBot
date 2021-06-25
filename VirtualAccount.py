class VirtualAccount:

    def __init__(self):
        self.usd_balance = 1000
        self.btc_amount = 1      ## always 1 BTC 
        self.btc_balance = 1000  ## 1000 dollars in 2016. TESTING_YEARS values were hardcode for bitcoin to avoid editions
        self.btc_price = 0
        self.bought_btc_at = 0
        self.last_transaction_was_sell = False;
    
 ## if COIN == "bitcoin":
 ##     if TESTING_YEARS == 2013:
 ##         self.account.btc_balance= 144
 ##     if TESTING_YEARS == 2014:
 ##         self.account.btc_balance = 771
 ##     if TESTING_YEARS == 2015:
 ##         self.account.btc_balance= 314
 ##     if TESTING_YEARS == 2016:
 ##         self.account.btc_balance = 434
 ##     if TESTING_YEARS == 2017:
 ##         self.account.btc_balance = 998
 ##     if TESTING_YEARS == 2018:
 ##         self.account.btc_balance = 13657
 ##     if TESTING_YEARS == 2019:
 ##         self.account.btc_balance= 3843
 ##     if TESTING_YEARS == 2020:
 ##         self.account.btc_balance = 7200
 ##     if TESTING_YEARS == 2021:
 ##         self.account.btc_balance = 29374