import ccxt
import os
import sys
import re
from pprint import pprint


leverage = 10
API_KEY = 'YOUR API KEY'
SECRET_KEY = 'YOUR SECRET KEY'



def table(values):
    first = values[0]
    keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
    widths = [max([len(str(v[k])) for v in values]) for k in keys]
    string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
    return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


def setLeverageAndMarginType(symbol, leverage):
    market = exchange.market(symbol)
    res = exchange.setLeverage(leverage, market['id'] )
    print(res)
    print('Changing your', symbol, 'position margin mode to ISOLATED:')
    try:
        response = exchange.fapiPrivate_post_margintype({
        'symbol': market['id'],
        'marginType': 'ISOLATED',
        })
        print(response)
    except Exception as e:
        print(e)
        
exchange = ccxt.binanceusdm({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'options': { 'adjustForTimeDifference': True }
})




def coin(value):
    match = re.search('BTCUSDT|LTCUSDT|ETHUSDT', value['symbol'])
    if match:
        return True
    else:
        return False

def coin2(value):
    print(value['symbol'])
    return True

# print(res)
# res = exchange.setLeverage(10, "ETH/USDT" )
# print(res)
# res = exchange.setLeverage(10, "LTC/USDT" )
# print(res)



markets = exchange.load_markets()
setLeverageAndMarginType('BTC/USDT', leverage)
print()
setLeverageAndMarginType('ETH/USDT', leverage)
print()
setLeverageAndMarginType('LTC/USDT', leverage)
print()



exchange.verbose = False  # UNCOMMENT THIS AFTER LOADING THE MARKETS FOR DEBUGGING

print('----------------------------------------------------------------------')

print('Fetching your balance:')
response = exchange.fetch_balance()
pprint(response['total'])  # make sure you have enough futures margin...
# pprint(response['info'])  # more details

print('----------------------------------------------------------------------')

# https://binance-docs.github.io/apidocs/futures/en/#position-information-v2-user_data

print('Getting your positions:')
response = exchange.fapiPrivateV2_get_positionrisk()
print( type(response) )
print( table( list(filter(coin, response)) ))
#print(table(response))

print('----------------------------------------------------------------------')

# https://binance-docs.github.io/apidocs/futures/en/#change-position-mode-trade
# res = exchange.fapiPrivatePostPositionSideDual({'dualSidePosition':'true'})

print("PositionSide (HEDGE) is set to:")
res = exchange.fapiPrivateGetPositionSideDual()
print(res)
print()

print('Setting your positions to Hedge mode:')
response = exchange.fapiPrivate_post_positionside_dual({'dualSidePosition': True})
print(response)


print('Getting your current position mode (One-way or Hedge Mode):')
response = exchange.fapiPrivate_get_positionside_dual()
if response['dualSidePosition']:
    print('You are in Hedge Mode')
else:
    print('You are in One-way Mode')

print('----------------------------------------------------------------------')




# print('----------------------------------------------------------------------')

# # https://binance-docs.github.io/apidocs/futures/en/#change-margin-type-trade

# print('Changing your', symbol, 'position margin mode to CROSSED:')
# response = exchange.fapiPrivate_post_margintype({
#     'symbol': market['id'],
#     'marginType': 'CROSSED',
# })
# print(response)

# print('Changing your', symbol, 'position margin mode to ISOLATED:')
# response = exchange.fapiPrivate_post_margintype({
#     'symbol': market['id'],
#     'marginType': 'ISOLATED',
# })
# print(response)

# print('----------------------------------------------------------------------')
