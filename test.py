from bigbuy import BigBuy

bb = BigBuy(app_key = 'OWNhZmMyMzkxYTc3Y2ZlZGZiN2U5NTY2ZmM5NWRjMTU2ZWY2MjgyMTFlMmU1MzU5NmFiMTU2ZTJlNjlmMGM2NA')
print(bb.get_products(pageSize=1))
