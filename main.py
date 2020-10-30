import requests
import json
import pprint
import matplotlib.pyplot as plt


def main():
    # http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/{startDate}/{endDate}/
    # {table} - table A contains MID, table C contaions BIS/ASK values
    # {code} - currency code, ie SEK
    # {startDate} - start date YYYY-MM-DD
    # {endDate} - end date YYYY-MM-DD

    startDay = '2020-10-01'
    endDay = '2020-10-30'
    table = 'a'
    code = 'sek'

    url = 'http://api.nbp.pl/api/exchangerates/rates/%s/%s/%s/%s/?format=json' % (table, code, startDay, endDay)
    response = requests.get(url)
    prices = response.json()
    rates = prices['rates']

    for rate in rates:
        print(f"{rate['effectiveDate']}, {rate['mid']}")

    effectiveDate = [rate['effectiveDate'] for rate in rates]
    ccPrice = [rate['mid'] for rate in rates]
    plt.plot(effectiveDate, ccPrice)
    plt.show()


if __name__ == '__main__':
    main()
