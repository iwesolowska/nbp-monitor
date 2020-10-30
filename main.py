import requests
import json
import pprint
import matplotlib.pyplot as plt
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry


def main():
    # http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/{startDate}/{endDate}/
    # {table} - table A contains MID, table C contains BIS/ASK values
    # {code} - currency code, ie SEK
    # {startDate} - start date YYYY-MM-DD
    # {endDate} - end date YYYY-MM-DD

    gui = widgets_setup()
    gui.mainloop()


def widgets_setup():
    ccy_values = ['AUD', 'BRL', 'CAD', 'CHF', 'COP', 'CZK', 'EUR', 'GBP', 'HKD', 'HUF', 'INR', 'JPY', 'MXN', 'NOK',
                  'PLN', 'RUB', 'SEK', 'USD']
    gui = tk.Tk()
    gui.geometry('800x300')
    gui.title('NBP Monitor')

    title_label = tk.Label(gui, text='Welcome to NBP currency monitor!')
    title_label.grid(row=0, sticky=tk.NSEW)

    gui.rowconfigure(1, weight=1)
    plot_stats_frame = tk.Frame(gui)
    plot_stats_frame.grid(row=1)

    control_frame = tk.Frame(gui)
    control_frame.grid(row=2)

    ccy_label = tk.Label(control_frame, text='Choose currency: ')
    ccy_label.pack(fill=tk.Y, side=tk.LEFT)
    ccy_combo = ttk.Combobox(control_frame, values=ccy_values)
    ccy_combo.pack(fill=tk.Y, side=tk.LEFT)

    start_date_label = tk.Label(control_frame, text='Choose start date: ')
    start_date_label.pack(fill=tk.Y, side=tk.LEFT)
    start_cdr = DateEntry(control_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=2020, date_pattern='yyyy-mm-dd')
    start_cdr.pack(fill=tk.Y, side=tk.LEFT)

    end_date_label = tk.Label(control_frame, text='Choose end date: ')
    end_date_label.pack(fill=tk.Y, side=tk.LEFT)
    end_cdr = DateEntry(control_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=2020, date_pattern='yyyy-mm-dd')
    end_cdr.pack(fill=tk.Y, side=tk.LEFT)

    def b_pressed():
        fetch_nbp_data(start_cdr.get(), end_cdr.get(), 'a', ccy_combo.get())

    draw_button = tk.Button(control_frame, text='Show data', command=b_pressed)
    draw_button.pack(fill=tk.Y, side=tk.RIGHT)

    return gui


def fetch_nbp_data(start_day, end_day, table, code):
    url = 'http://api.nbp.pl/api/exchangerates/rates/%s/%s/%s/%s/?format=json' % (table, code, start_day, end_day)
    response = requests.get(url)
    prices = response.json()
    rates = prices['rates']

    for rate in rates:
        print(f"{rate['effectiveDate']}, {rate['mid']}")

    effective_date = [rate['effectiveDate'] for rate in rates]
    cc_price = [rate['mid'] for rate in rates]
    plt.style.use('dark_background')
    plt.plot(effective_date, cc_price, 'o-')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('%s prices \nFrom %s to %s' % (code.upper(), start_day, end_day))
    plt.show()


if __name__ == '__main__':
    main()
