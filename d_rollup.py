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

print("")

# Test if we are connected to the correct datamart
try:
    cursor.execute(f"CREATE DATABASE {datamart}")
except:
    print(f"Successfully connected to the {datamart}")

print("")
print('---------------------------------------')

print("Example of Rollup operation using chosen dimension and chosen measure")

print("")
print('---------------------------------------')

# Print out the whole table

print("")
print("Print out the contents of the fact table")

with open('fact_table_name.txt', 'r') as f_fact:
    fact_name = f_fact.read()

print("customer_FK, product_FK, quantity")

sql = (f"SELECT * FROM {fact_name}")
cursor.execute(sql) 
myresult = cursor.fetchall()

for i in myresult:
	print(f"{i}")

print("")
print('---------------------------------------')

# Put up a console
# Ask user to input names of dimension and measure to aggregate upon

d_name = input("Choose dimension --> ")
measure_name = input("Choose measure --> ")

# Printing out aggregate for customers
sql = (f"SELECT {d_name}_FK, SUM({measure_name}) AS total_by_{d_name} FROM {fact_name} GROUP BY {d_name}_FK")
#print(sql)
cursor.execute(sql) # Now I need to read these data

print("")

# Print out cursor header before printing out the data values
ls = []
num_fields = len(cursor.description)
for i1 in cursor.description:
     ls.append(i1[0])
print(ls)

# This prints out the aggregated result
i = ""
for i,j in cursor:
    print(f"[{int(i)} --> {int(j)}]")

print("")
print('---------------------------------------')

print('----------------End of Script --------------------')
# https://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query


# # Print out the whole store table here
# sql = "SELECT * FROM store"
# cursor.execute(sql) 
# myresult = cursor.fetchall()
# print("customer_FK -- product_FK -- quantity")
# for i in myresult:
# 	print(f"{i}")

# print("")
# print('---------------------------------------')



# Printing out aggregate for customers
# sql = ("SELECT customer_FK, SUM(quantity) AS total_by_customer FROM store GROUP BY customer_FK")
# #print(sql)
# cursor.execute(sql) # Now I need to read these data

# # Print out cursor header before printing out the data values
# ls = []
# num_fields = len(cursor.description)
# for i1 in cursor.description:
#      ls.append(i1[0])
# print(ls)

# # This prints out the aggregated result
# i = ""
# for i,j in cursor:
#     print(f"[{int(i)} --> {int(j)}]")

# print("")
# print('---------------------------------------')
