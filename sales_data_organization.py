
import os
import sys # {REQ-1}
import pandas as pd
from datetime import datetime

def main():
    """Main program function"""
    data_sales_path = sys.argv 
    # Ensure the input for the path is valid
    csv_path = data_sales_path[1]
    # Make sure that the path is valid
    valid_input(data_sales_path)
    # Dataframe object of Main CSV
    sales_df = pd.read_csv(csv_path)
    # Get all the dates for the files with no dupes
    a_dates = all_dates(sales_df)  
    # Re load the CSV
    sales_df = pd.read_csv(csv_path)
    # Seperate the dates
    for date in a_dates:
        split_date = date.split(',')
        date_form1 = f'{int(split_date[1])}/{int(split_date[2])}/{split_date[0]}'
        date_form2 = f'{split_date[0]}-{split_date[1]}-{split_date[2]}'
        specific_df = sales_df.loc[sales_df['ORDER DATE'] == date_form1]
        print(file_mod_and_write(specific_df, csv_path, date_form2))
        
    return None


def valid_input(file_path):
    """Ensures the path is passed as an arg and is a valid path"""
    if len(file_path) <= 1:  
        # Error message to user
        print('\tAn incorrect path has been used. \
        \n\tPlease re-run this script with a valid system path!')
        sys.exit()

    valid_path = os.path.exists(file_path[1])
    valid_file = os.path.isfile(file_path[1])
    if not valid_path and not valid_file: 
        # Error message to user
        print(f"\tUnfortunately the path '{data_sales_path[1]}' \
            \tisn't a valid path. Verify that this is the correct path.\
            \n\tIf you have encountered an input error please retry!")
        sys.exit()

def all_dates(df):
    """Creates a list of all dates from the files with no dupes""" 
    # Convert the csv to to a dataframe
    # Normalize the datetime so you can just take the exact date
    df['ORDER DATE'] = pd.to_datetime(df['ORDER DATE'])
    df['ORDER DATE'] = df['ORDER DATE'].dt.date
    # Sort the dates inplace from oldest to new
    df.sort_values(by='ORDER DATE', inplace=True)
    # Convert the dates to a list 
    date_list = df['ORDER DATE'].tolist()
    # Store dates in the proper date
    proper_format = [date.strftime("%Y,%m,%d") for date in date_list]
    # Remove the duplicates
    no_dupes = []
    [no_dupes.append(entry) for entry in proper_format if entry not in no_dupes]
    
    return no_dupes

def file_mod_and_write(df, file_path, order_date):
    """Assign all the proper formatting and then writing to each file"""
    df = order_total(df)
    # Add dollar signs to the ITEM PRICE column
    df = add_dollar_signs(df) 
    # Create the correct directory
    parent_path = file_path
    file_path = create_folder(order_date, parent_path)
    # Sort the Dataframe by the item number in ascending order
    df = ascending_itm_num(df) 
    # Deleted the columns that weren't needed
    del df['ORDER ID']
    del df['ADDRESS']
    del df['CITY']
    del df['STATE']
    del df['POSTAL CODE']
    del df['COUNTRY']
    # Write the Dataframe to an excel file 
    write_excel(df, order_date, file_path)

    return f'* Order_{order_date} folder created \n * {order_date}.xlsx created'

# {REQ-8}
def ascending_itm_num(df):
    """Arrange the df by item numbers"""
    new_df = df.sort_values(by='ITEM NUMBER')
    return new_df

# {REQ-9} and {REQ-10}
def order_total(df):
    """Used to find the total cost of order and grand total"""
    # Drop the columns that aren't needed
    df.drop(columns=['ORDER ID', 'ADDRESS', 'CITY', 'STATE', 'POSTAL CODE', 'COUNTRY'])
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
    # Create the final row
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
 
def write_excel(order_df, order_date, order_path):
    """Convert the data frame to an excel file and properly format it"""
    # Set the path to save the file to 
    order_path += f'\\{order_date}.xlsx'
    # Create a worksheet to make edits to the file
    writer = pd.ExcelWriter(order_path, engine='xlsxwriter')
    # Create the Excel object
    order_df.to_excel(writer, sheet_name='Order Info', index=False)
    # Create a .book and allow it to be edited 
    workbook = writer.book
    worksheet = writer.sheets['Order Info']
    # Format the file correctly
    worksheet.set_column(0, 0, 11)
    worksheet.set_column(1, 1, 13)
    worksheet.set_column(2, 5, 15)
    worksheet.set_column(6, 7, 13)
    worksheet.set_column(8, 8, 10)
    worksheet.set_column(9, 9, 35)
    # Save the excel file
    writer.close()

def create_folder(order_date, parent_path): 
    """Create all of the order_folders"""
    # Directory we're going to be adding the subdirectories to 
    split_path = parent_path.split('\\')
    s_path_len = len(split_path)
    # Remove the file and just have the raw path to the csv
    final_path = "\\".join(split_path[:s_path_len - 1])
 
    parent_dir = f'{final_path}\\Orders\\'
    # Properly format the date
    split_date = order_date.split(',')
    proper_date = '-'.join(split_date)
    current_dir_name = f'Orders_{proper_date}'
    # Join the individual dirs with the parent dir 
    final_path = parent_dir + current_dir_name 
    # make the directory
    os.makedirs(final_path)
    
    return final_path

if __name__ == '__main__':
    main()


