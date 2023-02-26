import pandas as pd


def get_macro_data(type):
    macro_data = pd.read_csv("./macro dataset/" + type + ".csv")
    return macro_data


def calculate_change(df, col_name, start_date, end_date):
    initial_val = float(df.loc[df['DATE'] == start_date][col_name])
    new_val = float(df.loc[df['DATE'] == end_date][col_name])

    change = round(((new_val - initial_val) / initial_val) * 100, 2)
    return change


def calculate_change_rate(df, col_name, start_date, end_date):
    init_val, new_val = '.', '.'

    while init_val == '.':
        for idx in range(df.index[df['DATE'] == start_date][0], len(df)):
            if df.iloc[idx][col_name] != '.':
                init_val = float(df.iloc[idx][col_name])
                break

    while new_val == '.':
        for idx in range(df.index[df['DATE'] == end_date][0], len(df)):
            if df.iloc[idx][col_name] != '.':
                new_val = float(df.iloc[idx][col_name])
                break

    change = round(new_val - init_val, 2)
    return change


def get_stock_symbols_data():
    stock_tkr_data = pd.read_csv(
        "./MegaCap Stock Symbols.csv")
    return stock_tkr_data


def process_macro_data(type, start_date, end_date):
    df = get_macro_data(type)

    if type == "CPI":
        change = calculate_change(df, "CPIAUCSL", start_date, end_date)
    elif type == "Federal Funds Rate":
        change = calculate_change_rate(df, "DFF", start_date, end_date)
    elif type == "Retail Price":
        change = calculate_change(df, "PCUARETTRARETTR", start_date, end_date)
    elif type == "Treasury yield 2yrs":
        change = calculate_change_rate(df, "DGS2", start_date, end_date)
    elif type == "Treasury yield 10yrs":
        change = calculate_change_rate(df, "DGS10", start_date, end_date)
    elif type == "Treasury yield 20yrs":
        change = calculate_change_rate(df, "DGS20", start_date, end_date)
    elif type == "Treasury yield 30yrs":
        change = calculate_change_rate(df, "DGS30", start_date, end_date)
    elif type == "Unemployment":
        change = calculate_change(df, "UNEMPLOY", start_date, end_date)
    return change


print(process_macro_data("CPI", "2017-01-01", "2018-01-01"))
print(process_macro_data("Federal Funds Rate", "2017-01-01", "2018-01-01"))
print(process_macro_data("Retail Price", "2017-01-01", "2018-01-01"))
print(process_macro_data("Treasury yield 2yrs", "2017-01-01", "2018-01-01"))
print(process_macro_data("Treasury yield 10yrs", "2017-01-01", "2018-01-01"))
print(process_macro_data("Treasury yield 20yrs", "2017-01-01", "2018-01-01"))
print(process_macro_data("Treasury yield 30yrs", "2017-01-01", "2018-01-01"))
print(process_macro_data("Unemployment", "2017-01-01", "2018-01-01"))
