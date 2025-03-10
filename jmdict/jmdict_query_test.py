import sqlite3

conn = sqlite3.connect("vocab.db")
cursor = conn.cursor()

# Query to get the list of tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all the results (table names)
tables = cursor.fetchall()

# Print the tables
for table in tables:
    print(table[0])

cursor.execute("pragma table_info(book_info);")

print("BOOK COLUMNS")
book_info = cursor.fetchall()
for i in book_info:
    print(i)

cursor.execute("pragma table_info(WORDS);")

print("WORD COPLUMNS")
words = cursor.fetchall()
for i in words:
    print(i)

cursor.execute("pragma table_info(lookups);")

print("lookups COPLUMNS")
lookups = cursor.fetchall()
for i in lookups:
    print(i)

cursor.execute("""
    select words.id, book_info.id
    from words, book_info
    limit 15;
""")
word_book = cursor.fetchall()
for i in word_book:
    print(i)

# Close the connection
cursor.close()
conn.close()