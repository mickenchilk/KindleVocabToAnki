# fuck ive completely forgotten how to use python lmfao??
# i forgot how to comment lol
import sqlite3
import requests

# where the vocabulary database is located when i plug my kindle in
vocab_path = "D:/system/vocabulary/vocab.db"

# for when i used the jisho api,,, too slow :)
# def get_jisho_def(word):
#     url = f"https://jisho.org/api/v1/search/words?keyword={word}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         #json serialize that hoe!
#         data = response.json()
#         if data["data"]:
#             word_data = data["data"][0]
#             definitions = []
#             for sense in word_data["senses"]:
#                 definitions.extend(sense.get("english_definitions",[]))

#             return definitions
#         else:
#             return f"No definitions found for {word}"
#     else:
#         return f"Error! {response.status_code}"

#gives a list of definitions for given word
def kanji_def(word):
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

    definitions = []
    
    for i in cursor.fetchall:
        definitions.append(i)

    conn.close()
    return definitions

# establish a connection to the db using sqlite
conn = sqlite3.connect(vocab_path)
cursor = conn.cursor()

# take your sensitive ass back to PYTHON we SQL in this bitch!!!!!!!!!!!!
cursor.execute("""
    SELECT WORDS.word, LOOKUPS.usage
    FROM WORDS
    JOIN LOOKUPS ON WORDS.id = LOOKUPS.word_key
    LIMIT 20;
""")
test = cursor.fetchall()

conn.close()

print("HEEEEEEEEELP!!!!!!!")
for item in test:
    print(item)

for stem, usage in test:
    print(get_jisho_def(stem))
