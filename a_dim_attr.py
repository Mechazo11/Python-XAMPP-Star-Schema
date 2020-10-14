import mysql.connector
from mysql.connector import Error

# create the dim_store database if it not created yet
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    #database="dim_store"
)

cursor = connection.cursor(prepared=True)

sql = (f"CREATE DATABASE dim_store")
print("") # Improved readability
try:
    cursor.execute(sql)
    print('dim_store database created successfully!')
except:
    print("dim_store database already exsists")

connection.close()

# Connect to dim_store and start taking inputs for dimension tables
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="dim_store"
)

cursor = connection.cursor(prepared=True)

print('---------------------------------------')

# Ask user for number of dimensions
dim_number = input("How many dimensions in number: ")
dim_counter = 0
dim_list = [] # A list to hold the names of the dimensions

# Master loop for creating dimensions with chosen attributes
for x in range(int(dim_number)):
    print('---------------------------------------')
    print("")

    dim_counter = dim_counter + 1
    dim_starter = str(dim_counter * 100)
    print("Dimension " + str(dim_counter))

    dim_name = "" # Clear the name variable for next run
    dim_name = input("Dimension name, string --> ")
    dim_list.append(dim_name)
    
    #Firt create just the table with the Dimension name and primary_key
    try:
        sql=(f"CREATE TABLE {dim_name} ({dim_name}_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT)")
        #print(sql)    
        cursor.execute(sql)
        # Set autoincrement to a multiple of the dimension number
        sql=(f"ALTER TABLE {dim_name} AUTO_INCREMENT = {dim_starter}")
        #print(sql)    
        cursor.execute(sql)
    except:
        print("Error in creating dimension table")

    # Ask for number of attributes
    attr_x = []
    a = True
    print("") # Improved readibility
    while (a == True):
        attr_number = input("Number of Attributes in integer value: ")
        if(attr_number.isdigit() == True):
            a = False
        else:
            print("Not integer digits try again")
    
    for x1 in range(int(attr_number)): # Loop to get attribute names
        add = input("Attribute name, string --> ")
        attr_x.append(add)
        # Add this attribute to the end of the current dimension table
        try:
            sql = ("ALTER TABLE {} ADD {} VARCHAR(50)".format(dim_name,attr_x[x1]))
            #print(sql)
            cursor.execute(sql)
        except:
            print('Error in creating dimension attribute')

    print(attr_x) # Here we have the neccessary attributes

# Store the values of dimensions in a txt file here
x = ",".join(dim_list)
with open('dimension_name.txt', 'w') as d_file:
    d_file.write(x)

print(x) # Debug

connection.close()
print("")
print('----------------End of Script --------------------')
# End of script

# Boilerplates
# print("")
# print('---------------------------------------')
# print('----------------End of Script --------------------')
# Assigning a unique ID seed number : https://stackoverflow.com/questions/2130635/how-to-make-a-primary-key-start-from-1000
# To change the indexing number we will need to execute two separate statements
#sql=("CREATE TABLE {} ({}_ID int PRIMARY KEY AUTO_INCREMENT)".format(dim_name, dim_name))

# https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/