
import os
import sys # {REQ-1}

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

def orders_sub_dirs():
    """Create sub directorys for certain orders"""

    return None



if __name__ == '__main__':
    main()
    





