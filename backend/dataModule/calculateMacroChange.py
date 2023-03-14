import pandas as pd


def get_macro_data(type):
    macro_data = pd.read_csv("./dataset/macro dataset/" + type + ".csv")
    return macro_data


def verify_date(df, date):
    verified_date = df.loc[df["DATE"] >= date, "DATE"].iloc[0]
    return verified_date


def calculate_change(df, col_name, start_date, end_date):
    start_date, end_date = verify_date(
        df, start_date), verify_date(df, end_date)

    initial_val = float(df.loc[df['DATE'] == start_date][col_name])
    new_val = float(df.loc[df['DATE'] == end_date][col_name])

    change = round(((new_val - initial_val) / initial_val) * 100, 2)
    return change


def calculate_change_rate(df, col_name, start_date, end_date):

    start_date, end_date = verify_date(
        df, start_date), verify_date(df, end_date)

    # initial_val = float(df.loc[df['DATE'] == start_date][col_name])
    # new_val = float(df.loc[df['DATE'] == end_date][col_name])

    initial_val, new_val = '.', '.'

    while initial_val == '.':
        for idx in range(df.index[df['DATE'] == start_date][0], len(df)):
            if df.iloc[idx][col_name] != '.':
                initial_val = float(df.iloc[idx][col_name])
                break

    while new_val == '.':
        for idx in range(df.index[df['DATE'] == end_date][0], len(df)):
            if df.iloc[idx][col_name] != '.':
                new_val = float(df.iloc[idx][col_name])
                break

    change = round(new_val - initial_val, 2)
    return change


def get_stock_symbols_data():
    stock_tkr_data = pd.read_csv("./dataset/MegaCap Stock Symbols.csv")
    return stock_tkr_data


def process_macro_data(start_date, end_date):
    changes = []

    df = get_macro_data("CPI")
    changes.append(calculate_change(df, "CPIAUCSL", start_date, end_date))  # CPI
    df = get_macro_data("Federal Funds Rate")
    changes.append(calculate_change_rate(df, "DFF", start_date, end_date))  # Federal Funds Rate
    df = get_macro_data("Retail Price")
    changes.append(calculate_change(df, "PCUARETTRARETTR", start_date, end_date))  # Retail Price
    df = get_macro_data("Treasury yield 2 years")
    changes.append(calculate_change_rate(df, "DGS2", start_date, end_date))  # Treasury yield 2 years
    df = get_macro_data("Treasury yield 10 years")
    changes.append(calculate_change_rate(df, "DGS10", start_date, end_date))  # Treasury yield 10 years
    df = get_macro_data("Treasury yield 20 years")
    changes.append(calculate_change_rate(df, "DGS20", start_date, end_date))  # Treasury yield 20 years
    df = get_macro_data("Treasury yield 30 years")
    changes.append(calculate_change_rate(df, "DGS30", start_date, end_date))  # Treasury yield 30 years
    df = get_macro_data("Unemployment")
    changes.append(calculate_change(df, "UNEMPLOY", start_date, end_date))  # Unemployment

    return changes

    # if type == "CPI":
    #     change = calculate_change(df, "CPIAUCSL", start_date, end_date)
    # elif type == "Federal Funds Rate":
    #     change = calculate_change_rate(df, "DFF", start_date, end_date)
    # elif type == "Retail Price":
    #     change = calculate_change(df, "PCUARETTRARETTR", start_date, end_date)
    # elif type == "Treasury yield 2 years":
    #     change = calculate_change_rate(df, "DGS2", start_date, end_date)
    # elif type == "Treasury yield 10 years":
    #     change = calculate_change_rate(df, "DGS10", start_date, end_date)
    # elif type == "Treasury yield 20 years":
    #     change = calculate_change_rate(df, "DGS20", start_date, end_date)
    # elif type == "Treasury yield 30 years":
    #     change = calculate_change_rate(df, "DGS30", start_date, end_date)
    # elif type == "Unemployment":
    #     change = calculate_change(df, "UNEMPLOY", start_date, end_date)
    # return change


################################## TESTING #########################################
# # normal input test
# types = ["CPI", "Federal Funds Rate", "Retail Price",
#          "Treasury yield 2yrs", "Treasury yield 10yrs",
#          "Treasury yield 20yrs", "Treasury yield 30yrs",
#          "Unemployment"]

# start_date = "2017-01-01"
# end_date = "2018-01-01"
# print("From: " + start_date, " To: " + end_date)
# for type in types:
#     print(process_macro_data(type, start_date, end_date))
# print()


# # test end date invalid (auto correct end date)
# start_date = "2017-01-01"
# end_date = "2018-01-21"
# print("From: " + start_date, " To: " + end_date)
# for type in types:
#     print(process_macro_data(type, start_date, end_date))
# print()

# # test date invalid 2 (auto correct end date)
# start_date = "2021-01-01"
# end_date = "2021-03-01"
# print("From: " + start_date, " To: " + end_date)
# for type in types:
#     print(process_macro_data(type, start_date, end_date))
# print()

# # test date invalid 3 (auto correct end date)
# start_date = "2021-05-01"
# end_date = "2022-07-01"
# print("From: " + start_date, " To: " + end_date)
# for type in types:
#     print(process_macro_data(type, start_date, end_date))
# print()

# # test date invalid 4 (auto correct end date)
# start_date = "2022-06-15"
# end_date = "2022-08-10"
# print("From: " + start_date, " To: " + end_date)
# for type in types:
#     print(process_macro_data(type, start_date, end_date))
# print()

# # test date invalid 5 (auto correct end date)
# start_date = "2022-07-01"
# end_date = "2022-10-01"
# print("From: " + start_date, " To: " + end_date)
# for type in types:
#     print(process_macro_data(type, start_date, end_date))
# print()
