
import os
import sys 

data_sales_path = sys.argv

if len(data_sales_path) <= 1:
    print('\tAn incorrect path has been used. \
    \n\tPlease re-run this script with a valid system path!')
    sys.exit()

valid_path = os.path.exists(data_sales_path[1])
if not valid_path:
    print(f"\tUnfortunately the path '{data_sales_path[1]}' \
        \tisn't a valid path. Verify that this is the correct path.\
        \n\tIf you have encountered an input error please retry!")
    sys.exit()




    





