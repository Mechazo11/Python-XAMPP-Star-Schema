import mysql.connector
from mysql.connector import Error

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="dim_store"
)
cursor = connection.cursor(prepared=True)

print("---------------------------------------------------------")
print("")
  
concept_name = input("Enter name of the concept table, string --> ")

try:
    sql =("CREATE TABLE {0} ({0}_ID int PRIMARY KEY AUTO_INCREMENT,dim_name VARCHAR(50), level VARCHAR(50))".format(concept_name))
    #print(sql)
    cursor.execute(sql)
except:
    print("Concept table already exsists")
print("")

# Automatic clearing of all tables each time the script is run
cursor.execute("TRUNCATE TABLE concept")

# Instruction to the user
print("This table has two columns named 'dim_name' and 'level'")
print("")
print("---------------------------------------------------------")
print("")
print("You will be asked to enter the number of dimensions")
print("Followed by prompt to input dimension names and the corresponding concept levels")
print("Data in entered in the following schema....")
print("dimension == lvl0 << lvl1 << lvl2 << .... << lvlM")
print("---------------------------------------------------------")
print("")
print("Example")
print("location == city << street << country << state")
print("---------------------------------------------------------")
print("")

#Ask user for number of dimensions
dim_number = input("How many dimensions in number: ")
dim_counter = 0

for x in range(int(dim_number)):
    dim_counter = dim_counter + 1
    print("Dimension " + str(dim_counter))

    # Get dimension name
    d_value = input("Dimension name, string --> ")
    level_value = input("Levels, string --> ")

    print("")
    print("---------------------------------------------------------")

    # Put the name of the dimension here
    sql = (f"INSERT INTO `{concept_name}` (`dim_name`, `level`) VALUES ('{d_value}', '{level_value}')")
    #print(sql) #Debug
    cursor.execute(sql)
    connection.commit()

connection.close()
print("------------------------End of Script --------------------------")
# end of script

# Fetching rows and columns from a table using MYSQL
# https://pynative.com/python-mysql-select-query-to-fetch-data/

# Inserting data into a table
# https://www.guru99.com/insert-into.html
# BE VERY CAREFUL, TO CHOOSE TABLE AND COLUMNS, use backtick (``) and for data single quote ('')