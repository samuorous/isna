**Isna** **is** a **s**imple **N**ER **a**nnotator.

# Abstract

This tool helps to manually generate named entity recognition (NER) annotations used mostly to generate training data for natural language processing tools.

Given a sentence Isna focuses on a quick workflow to mark parts and tag them.

```
Jane lives in Berlin
PER  O     O  LOC 
```

# Usage
Isna will use 3 files:
* `sentences.txt` One sentence to process per line.
* `tags.txt` The generated tags.
* `available_tags.txt` The available NER tags.

To tag a list of sentences:
* Clone this repo.
* Create a new Folder `<foo>` in `/data`.
* In `<foo>` place a new file `sentences.txt` with one sentence per line.
* Add in `<foo>` a file `available_tags.txt` with one available tag per line.
* Change `SESSION_DIR` in `config.py` to your `<foo>` folder.
* Take a look at `config.py` and change settings if they do not match your needs.
* Run `server.py`.
* Isna will initialize `tags.txt` with `unknown_tag`.
* Open 127.0.0.1:5000 in your Browser and mark parts of the sentence using the mouse.
* Hit the associated key to tag the marked part.
* Deselect with right click.
* Hit "Store changes" to update `tags.txt` with your markings.
