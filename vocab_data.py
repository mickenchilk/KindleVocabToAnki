# fuck ive completely forgotten how to use python lmfao??
# i forgot how to comment lol
import sqlite3

# the connection to the JMDict Japanese dictionary
conn_dict = sqlite3.connect("./jmdict.db")
cursor_dict = conn_dict.cursor()

# the connection to the vocabulary database for my kindle lookups
conn_kindle = sqlite3.connect("./vocab.db")
cursor_kindle = conn_kindle.cursor()

# where the vocabulary database is located when i plug my kindle in
# add this back in when I get that far :) 
# vocab_path = "D:/system/vocabulary/vocab.db"



#gives a list of definitions for given word
def kanji_def(word):
    cursor_dict.execute("""
        SELECT DISTINCT entries.kanji, entries.reading, extra_info.pos, entries.meaning,
                extra_info.dialect, extra_info.misc
        FROM entries
        JOIN extra_info ON entries.id = extra_info.entry_id
        LEFT JOIN kanji ON entries.id = kanji.entry_id
        WHERE kanji.kanji = ? OR entries.reading LIKE ?
    """,(word,f'%{word}%'))

    definitions =  cursor_dict.fetchone()

    return definitions

# grab kindle vocab
# take your sensitive ass back to PYTHON we SQL in this bitch!!!!!!!!!!!!
cursor_kindle.execute("""
    SELECT WORDS.word, LOOKUPS.usage
    FROM WORDS
    JOIN LOOKUPS ON WORDS.id = LOOKUPS.word_key
    LIMIT 15;
""")

test = cursor_kindle.fetchall()

print("--------- TEST VOCABULARY LIST FROM KINDLE WITH DEFINITIONS FROM JMDICT: ---------------")
for item in test:
    print(item)

# grab definitions
print("--------- DEFINITIONS FROM JMDICT DATABSE: ---------------")
for stem, usage in test:
    print(f"Word: {stem}")
    print(f"Definition: {kanji_def(stem)}")
    print(f"Usage/sentence: {usage}")
    print('\n')

# close open connections 
cursor_dict.close()
conn_kindle.close()
conn_dict.close()