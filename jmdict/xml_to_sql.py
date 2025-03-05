import sqlite3
import xml.etree.ElementTree as ET

# make tree out of xml dictionary
# we making a datbase because this file is huge and i need to look up like 1000 words each time
tree = ET.parse("./jmdict/JMDict.xml")
root = tree.getroot()

# establish a connection to the (currently) empty databse
conn = sqlite3.connect("jmdict.db")
cursor = conn.cursor()

# create (currently) empty tables

# main table with words, readings and definitions
cursor.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kanji TEXT,
    reading TEXT,
    meaning TEXT
);
""")

# tables for querying specific readings and kanji
cursor.execute("""
CREATE TABLE IF NOT EXISTS kanji (
    entry_id INTEGER,
    kanji TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    entry_id INTEGER,
    reading TEXT
);
""")

# table with extra information like part of speech, dialect, etc.
cursor.execute("""
CREATE TABLE IF NOT EXISTS extra_info (
    entry_id INTEGER,
    pos TEXT,
    dialect TEXT,
    priority TEXT,
    misc TEXT,
    FOREIGN KEY(entry_id) REFERENCES entries(id)
);
""")

conn.commit()

print("database set up! 📜✨")

# now we grab the definitions and extra info for each entry
for entry in root.findall("entry"):
    kanji_elements = [keb.text for keb in entry.findall("./k_ele/keb")]
    reading_elements = [reb.text for reb in entry.findall("./r_ele/reb")]
    meanings = [gloss.text for gloss in entry.findall("./sense/gloss")]

    # for if there are multiple kanji/readings for a single entry
    # get an easy to read string format, and query using the kanji & readings tables
    kanji_text = ", ".join(kanji_elements) if kanji_elements else None
    reading_text = ", ".join(reading_elements)
    meaning_text = ";  ".join(meanings)

    cursor.execute("INSERT INTO entries (kanji, reading, meaning) VALUES (?, ?, ?)", 
                   (kanji_text,reading_text,meaning_text))
    
    entry_id = cursor.lastrowid # get id of the row we just made for kanji, reading, and misc info

    for kanji in kanji_elements:
        cursor.execute("INSERT INTO kanji (entry_id, kanji) VALUES (?,?)",
                       (entry_id,kanji))
    
    for reading in reading_elements:
        cursor.execute("INSERT INTO readings (entry_id, reading) VALUES (?,?)",
                       (entry_id,reading))

    pos_list = [pos.text for pos in entry.findall("./sense/pos")]
    dialect_list = [dial.text for dial in entry.findall("./sense/dial")]
    priority_list = [pri.text for pri in entry.findall("./k_ele/k_pri")]
    misc_list = [misc.text for misc in entry.findall("./sense/misc")]

    # add them into the extra db table
    cursor.execute("INSERT INTO extra_info (entry_id,pos,dialect,priority,misc) VALUES (?, ?, ?, ?, ?)",
                   (entry_id, pos_list[0], ", ".join(dialect_list),", ".join(priority_list),", ".join(misc_list)))
    
conn.commit()

print("inserted dictionary entries! 📜✨ dialects, pos, and more are now stored!!")

conn.close()