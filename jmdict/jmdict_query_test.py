import sqlite3

conn = sqlite3.connect("jmdict.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT entries.kanji, entries.reading, extra_info.pos, entries.meaning,
               extra_info.dialect, extra_info.misc
    FROM entries
    JOIN kanji ON entries.id = kanji.entry_id
    JOIN extra_info ON entries.id = extra_info.entry_id
    WHERE kanji.kanji = ?
""",('遊ぶ',))

cursor.execute("""
    SELECT * FROM entries WHERE reading LIKE '%そわそわ%';
""")

print(cursor.fetchall())

conn.close()