import sqlite3
import time
import pandas

# Read data to Pandas 
# data = pandas.read_csv("dataset.csv", low_memory=False)


# Create SQLite client
conn = sqlite3.connect('dataset.db')


# a) calculate top 25 most common 'makes'
def query_a_sqlite(conn, print_result=False):
    start_time = time.time()
    cursor = conn.execute('SELECT Make, count(*) as number_of_citations FROM citations WHERE Make IS NOT NULL AND Make != "" GROUP BY Make ORDER BY number_of_citations DESC LIMIT 25')
    rows = cursor.fetchall()
    end_time = time.time()
    if(print_result):
        for row in rows:
            print(row)
    return end_time - start_time

# b) calculate most common 'Color' for each 'Make'
def query_b_sqlite(conn, print_result=False):
    start_time = time.time()
    cursor = conn.execute('''
        SELECT Make, Color FROM (
            SELECT 
                ROW_NUMBER() OVER(PARTITION BY Make ORDER BY Make DESC) AS RowNumber,
                Make, 
                Color, 
                count(*) as number_of_citations 
            FROM 
                citations 
            WHERE 
                Make IS NOT NULL 
                AND Make != "" 
                AND Color != "" 
            GROUP BY 
                Make, 
                Color 
            ORDER BY 
                Make, 
                number_of_citations DESC, 
                Color) as A 
        WHERE RowNumber = 1
    ''')
    rows = cursor.fetchall()
    end_time = time.time()
    if(print_result):
        for row in rows:
            print(row)
    return end_time - start_time

# c) find the first ticket issued for each 'Make'
def query_c_sqlite(conn, print_result=False):
    start_time = time.time()
    cursor = conn.execute('Select Make, min("Issue Date") from citations group by Make')
    rows = cursor.fetchall()
    end_time = time.time()
    if(print_result):
        for row in rows:
            print(row)
    return end_time - start_time



print("\nSQLite")

print("a) Top 25 most common makes:")
run_1 = query_a_sqlite(conn)
print("Run 1: %s seconds" % run_1)
run_2 = query_a_sqlite(conn)
print("Run 2: %s seconds" % run_2)
run_3 = query_a_sqlite(conn)
print("Run 3: %s seconds" % run_3)
print("-----------------")
print("Average run time: %s seconds", (run_1 + run_2 + run_3) / 3)
print()


print("b) calculate most common 'Color' for each 'Make':")
run_1 = query_b_sqlite(conn)
print("Run 1: %s seconds" % run_1)
run_2 = query_b_sqlite(conn)
print("Run 2: %s seconds" % run_2)
run_3 = query_b_sqlite(conn)
print("Run 3: %s seconds" % run_3)
print("-----------------")
print("Average run time: %s seconds", (run_1 + run_2 + run_3) / 3)
print()

print("c) find the first ticket issued for each 'Make':")
run_1 = query_c_sqlite(conn)
print("Run 1: %s seconds" % run_1)
run_2 = query_c_sqlite(conn)
print("Run 2: %s seconds" % run_2)
run_3 = query_c_sqlite(conn)
print("Run 3: %s seconds" % run_3)
print("-----------------")
print("Average run time: %s seconds", (run_1 + run_2 + run_3) / 3)
print()


