# fuck ive completely forgotten how to use python lmfao??
# i forgot how to comment lol

# aqt is the Anki Qt (graphical user interface) package
# mw is the main window object (can manage cards, interact with anki menus, etc.)
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from anki.notes import Note

import sqlite3
import os


try:
    from aqt import mw
except ImportError:
    print("aqt module not available")
    raise



#------------------------------------------------------------------------------------------------#
# SQL FUNCTIONS
# gives the part of speech, meaning, dialect, and misc info for a word from jmdict database
def jmdict_definition(word):
    conn_dict = sqlite3.connect("C:/Users/Danika/AppData/Roaming/Anki2/addons21/4522106556/jmdict.db")
    cursor_dict = conn_dict.cursor()

    cursor_dict.execute("""
        SELECT DISTINCT entries.reading, extra_info.pos, entries.meaning, extra_info.misc
        FROM entries
        JOIN extra_info ON entries.id = extra_info.entry_id
        LEFT JOIN kanji ON entries.id = kanji.entry_id
        WHERE kanji.kanji = ? OR entries.reading LIKE ?
    """,(word,f'%{word}%'))

    # ok im lazy but pos = [0], meaning = [1], dialect = [2], misc = [3] lol
    word_info = [thing for thing in cursor_dict.fetchone() if thing not in (None, '')]

    conn_dict.close()

    return word_info

# grabs the kindle vocab word, the sentence its used in, the book 
# take your sensitive ass back to PYTHON we SQL in this bitch!!!!!!!!!!!!

# where the vocabulary database is located when i plug my kindle in
# add this back in when I get that far :) 
# vocab_path = "D:/system/vocabulary/vocab.db"
# conn_kindle = sqlite3.connect(vocab_path)

def kindle_vocab():
    conn_kindle = sqlite3.connect("C:/Users/Danika/AppData/Roaming/Anki2/addons21/4522106556/vocab.db")
    cursor_kindle = conn_kindle.cursor()
    cursor_kindle.execute("""
        SELECT WORDS.word, LOOKUPS.usage, BOOK_INFO.title
        FROM WORDS
        JOIN LOOKUPS ON WORDS.id = LOOKUPS.word_key
        JOIN BOOK_INFO ON LOOKUPS.book_key = BOOK_INFO.id 
        LIMIT 3;
    """)

    kindle_vocab = cursor_kindle.fetchall()
    conn_kindle.close()

    return kindle_vocab





#------------------------------------------------------------------------------------------------#
# Create flashcards in Anki for each word
def create_anki_cards():
    # Get the list of kindle vocab words and their info
    vocab_list = kindle_vocab()

    for word, usage, book_title in vocab_list:
        # Get the definition from the JMDict database
        word_definition = jmdict_definition(word)

        if word_definition:
            reading, pos, definition, other = word_definition

            # Prepare the card fields (front and back)
            word = word
            sentence = usage
            kana = reading
            pos = pos
            definition = definition
            other = other
            book_title = book_title



            # Check if the deck exists, otherwise create a new one
            # Make sure its a subdeck of Kindle Mining
            deck_name = "Kindle Mining::" + book_title
            deck_id = mw.col.decks.id(deck_name)

            # If deck doesn't exist, create it
            if not deck_id:
                mw.col.decks.add(deck_name)
                deck_id = mw.col.decks.id(deck_name)
            
            model = mw.col.models.by_name("KINDLE MINING")

            # Log to ensure deck_id is correct
            print(f"Deck ID for '{deck_name}': {deck_id}")

            # Create a new Anki card 
            note = Note(mw.col, model)

            # Set fields for anki card
            note.fields[0] = word
            note.fields[1] = sentence
            note.fields[2] = kana
            note.fields[3] = pos
            note.fields[4] = definition
            note.fields[5] = other
            note.fields[6] = book_title      

            # Ensure deck is being assigned correctly by setting 'did'
            print(f"Assigning to deck ID: {deck_id}")  # Debugging line to confirm deck assignment
            note.did = deck_id  # Assign the correct deck ID

            # Add the note to the deck
            mw.col.add_note(note, deck_id)

    # Sync the collection to make sure the cards get added
    mw.col.save()
    showInfo("Deck created successfully!")







#------------------------------------------------------------------------------------------------#
# Set up the menu action in Anki
action = QAction("Import from Kindle", mw)
action.triggered.connect(create_anki_cards)
mw.form.menuTools.addAction(action)