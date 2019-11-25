from bigbuy import BigBuy, BBError


bb = BigBuy(app_key = 'YmU4NzU4ZTEwMWQzOTlmNzAwMWMxZmY0N2E3MGVhYzFhZTBlMzFkOTdlOGJjOTY0OTQ1MGZlYzg3NDkxZDc0ZA', mode="sandbox")
test = 10
try:
    order = bb.check_order({})
    print(order)
except BBError as e:
    print(e.BBCode)
    print(e.BBMessage)



# curl  -H "Authorization: Bearer YmU4NzU4ZTEwMWQzOTlmNzAwMWMxZmY0N2E3MGVhYzFhZTBlMzFkOTdlOGJjOTY0OTQ1MGZlYzg3NDkxZDc0ZA" -H 'Content-type: application/json' -H 'Accept: application/json' https://api.sandbox.bigbuy.eu/rest/shipping/orders.json -d '{"order":{"delivery":{"isoCountry":"ES","postcode":"46005"},"products":[{"reference":"V1300179","quantity":1}]}}'
