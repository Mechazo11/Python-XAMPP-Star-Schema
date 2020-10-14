import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
)

cursor = connection.cursor(prepared=True)

print('---------------------------------------')

# Ask for the name of the datamart here
print('Enter name of datamart in smallcaps.')
datamart = input('Enter datamart name --> ')

# Create a file named datamart.txt and store that value
# Each time, this script is called, it will overwrite the first file
with open('datamart_name.txt', 'w') as f:
    f.write(datamart)

#print(f"CREATE DATABASE {datamart}") #Debug
sql = (f"CREATE DATABASE {datamart}")

try:
    cursor.execute(sql)
    print('Database created successfully!')
except:
    print("Database already exsists")

connection.close()

print('------------- End of script------------')


# ------------------------------------------------------------
# References
# Creating a database https://dev.mysql.com/doc/refman/8.0/en/creating-database.html
# https://www.guru99.com/python-mysql-example.html
# sql = ("ALTER TABLE {} ADD {}_fk INT(5)".format(fact_name,dim_x[i]))