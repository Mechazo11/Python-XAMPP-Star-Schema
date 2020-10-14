import mysql.connector
from mysql.connector import Error

# Import names of dimensions for use in this datamart
with open('dimension_name.txt', 'r') as d_file:
    dim_list = d_file.read()
#print(dim_list) # String
dim_list = dim_list.split(",") # This is a list of strings

# Context manager method
with open('datamart_name.txt', 'r') as f:
    datamart = f.read()

dim_store = "dim_store" # This is a default database that contains our dimension tables

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database= datamart
)

cursor = connection.cursor(prepared=True)

# Test if we are connected to the correct datamart
try:
    cursor.execute(f"CREATE DATABASE {datamart}")
except:
    print(f"Successfully connected to the {datamart}")

print("")
print('---------------------------------------')

# Create Fact Table
fact_name = input("Fact table name --> ")

try:
    sql = (f"CREATE TABLE {fact_name} ({fact_name}_dummy VARCHAR (5))")
    cursor.execute(sql)
except:
    print("Fact table already present!")

with open('fact_table_name.txt', 'w') as f_fact:
    f_fact.write(fact_name)

print("")
print('---------------------------------------')

# Define Measures to the Fact table
measure_x = []
a = True
while (a == True):
    measure_number = input("Number of Measures in integer value: ")
    if(measure_number.isdigit() == True):
        a = False
    else:
        print("Not integer digits try again")

for x1 in range(int(measure_number)): # Loop to get attribute names
    add = input("Name of measure attribute in string --> ")
    measure_x.append(add)
    try:
        sql = (f"ALTER TABLE {fact_name} ADD {add} INT(6)")
        #print(sql) # Debug
        cursor.execute(sql)
    except:
        print("Failed to add measure/ Measure already exsits")
print(measure_x) # Debug

print("")
print('---------------------------------------')

# Drop dummy column

try:
    sql = (f"ALTER TABLE {fact_name} DROP COLUMN {fact_name}_dummy")
    cursor.execute(sql)
except:
    print("Dummy key already dropped")

print("")
print('---------------------------------------')

################# Import Dimensions #######################

# Read a text and split it back to list
with open('dimension_name.txt', 'r') as d_file:
    dim_list = d_file.read()

# List of dimension names available
dim_list = dim_list.split(",")
dim_list.reverse() # Put in reverse order so they come up sequentially in fk columns
#print(dim_list) # Debug test

dim_counter = 0

# This loop imports the dimensions
for x in range(len(dim_list)):
    dim_counter = dim_counter + 1
    dim_starter = str(dim_counter * 100)
    #print("Dimension " + str(dim_counter))
    dim_name = dim_list[x]
    try:
        sql = (f"CREATE TABLE {datamart}.{dim_name} LIKE {dim_store}.{dim_name}")
        #print(sql)
        cursor.execute(sql)
        sql=(f"ALTER TABLE {dim_name} AUTO_INCREMENT = {dim_starter}")
        #print(sql)    
        cursor.execute(sql)
    except:
        print("Failed to import dimension / Table already exsits")

print("")
print('---------------------------------------')

################# Create Composite Key #######################

for dimension in dim_list:
    # Create a column
    sql = (f"ALTER TABLE `{fact_name}` ADD `{dimension}_FK` INT NOT NULL FIRST")
    #print(sql)
    try:
        cursor.execute(sql)
    except:
        print("FK column already present")
    
    # Add Foreign Key constraints
    sql = (f"ALTER TABLE `{fact_name}` ADD CONSTRAINT `{dimension}_CONST` FOREIGN KEY (`{dimension}_FK`) REFERENCES `{dimension}`(`{dimension}_ID`) ON DELETE RESTRICT ON UPDATE RESTRICT")
    #print(sql)
    try:
        cursor.execute(sql)
    except:
        print("Constraint already present")

# This command will create the composite primary key

dimension = [] # Reset it
dim_list.reverse() # Flip back to original

# Loop to add the _FK string to each of them
for i in range(len(dim_list)):
    dim_list[i] = dim_list[i] + "_FK"
print(dim_list)

dim_list_string = ",".join(dim_list)
print(dim_list_string)

sql = (f"ALTER TABLE {fact_name} ADD PRIMARY KEY({dim_list_string})")
#print(sql)
#cursor.execute(sql) 
try:
    cursor.execute(sql)
except:
    print("Error in adding composite primary key")


connection.close()
print("")
print('----------------End of Script --------------------')

