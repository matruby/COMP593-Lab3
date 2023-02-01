
import os
import sys # {REQ-1}
import pandas as pd
import datetime

def main():
    """Main program function"""
    data_sales_path = sys.argv # csv path variable

    return None


def valid_input(file_path):
    """Ensures the path is passed as an arg and is a valid path"""
    if len(data_sales_path) <= 1: # {REQ-2} 
        # Error message to user
        print('\tAn incorrect path has been used. \
        \n\tPlease re-run this script with a valid system path!')
        sys.exit()

    valid_path = os.path.exists(data_sales_path[1])
    if not valid_path: # {REQ-3}
        # Error message to user
        print(f"\tUnfortunately the path '{data_sales_path[1]}' \
            \tisn't a valid path. Verify that this is the correct path.\
            \n\tIf you have encountered an input error please retry!")
        sys.exit()

    elif valid_path and valid_path[-4:] == '.csv':
        return file_path

def all_dates(path_of_csv):
    """Creates a list of all dates from the files with no dupes""" 
    # Convert the csv to to a dataframe
    sales_data_df = pd.read_csv(path_of_csv[1]) 
    # Normalize the datetime so you can just take the exact date
    sales_data_df['ORDER DATE'] = pd.to_datetime(sales_data_df['ORDER DATE'])
    sales_data_df['ORDER DATE'] = sales_data_df['ORDER DATE'].dt.date
    # Sort the dates inplace from oldest to new
    sales_data_df.sort_values(by='ORDER DATE', inplace=True)

    # Convert the dates to a list 
    date_list = sales_data_df['ORDER DATE'].tolist()
    # Store dates in the proper date
    proper_format = [date.strftime("%Y,%m,%d") for date in date_list]

    # Remove the duplicates
    no_dupes = []
    [no_dupes.append(entry) for entry in proper_format if entry not in no_dupes]
    
    return no_dupes


def order_total(df):
    """Used to find the total cost of order and grand total"""
    # Value for the grand total
    g_total = 0
    # List to hold the total cost per order
    total_lst = []
    for ent in range(len(df)): 
        # Pull the quantity and variable of the individual item 
        quantity = df.iloc[ent].at['ITEM QUANTITY']
        price = df.iloc[ent].at['ITEM PRICE']
        # Figure out the total price 
        total_price = (price * quantity) 
        # Add total price to the grand total 
        g_total += total_price
        # Properly format the total string
        price_formatted = f'${total_price:,}'
        total_lst.append(price_formatted)

    # Insert all the totals in the new column
    df.insert(7, 'TOTAL PRICE', total_lst)

    # Add the final row by creating a df and adding it to the
    # main df.
    final_row = pd.DataFrame({'ITEM PRICE':['GRAND TOTAL'], 
        'TOTAL PRICE':[f'${g_total:,}']})
    df = pd.concat([df, final_row], ignore_index=True, axis=0)
    # Deal with nan changing other values to floats.
    df['ORDER ID'] = df['ORDER ID'].astype('Int32')
    df['ITEM NUMBER'] = df['ITEM NUMBER'].astype('Int32')
    df['ITEM QUANTITY'] = df['ITEM QUANTITY'].astype('Int32')
    return df

def add_dollar_signs(df):
    """Add dollar signs to Item Price"""
    for ent in range(len(df)):
        price = df.iloc[ent].at['ITEM PRICE']
        df.at[ent, 'ITEM PRICE']=f'${price}'

    return df 



if __name__ == '__main__':
    main()


