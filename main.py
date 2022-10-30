import os
from platform import system

import ebooklib
import tqdm
from bs4 import BeautifulSoup
from ebooklib import epub

ENDER_KEY = {
    "a": "⏃",
    "b": "⏚",
    "c": "☊",
    "d": "⎅",
    "e": "⟒",
    "f": "⎎",
    "g": "☌",
    "h": "⊑",
    "i": "⟟",
    "j": "⟊",
    "k": "☍",
    "l": "⌰",
    "m": "⋔",
    "n": "⋏",
    "o": "⍜",
    "p": "⌿",
    "q": "☌",
    "r": "⍀",
    "s": "⌇",
    "t": "⏁",
    "u": "⎍",
    "v": "⎐",
    "w": "⍙",
    "x": "⌖",
    "y": "⊬",
    "z": "⋉",
}

LATIN_KEY = {
    "a": "mm",
    "b": "yu",
    "c": "ch",
    "d": "h",
    "e": "dd",
    "f": "rrr",
    "g": "H",
    "h": "o",
    "i": "ya",
    "j": "ua",
    "k": "a",
    "l": "i",
    "m": "î",
    "n": "w",
    "o": "ae",
    "p": "uo",
    "q": "v",
    "r": "g",
    "s": "n",
    "t": "sss",
    "u": "ai",
    "v": "f",
    "w": "z",
    "x": "t",
    "y": "yo",
    "z": "kh"
}


def clear_console():
    if system() == "Windows":
        return os.system("cls")
    else:
        return os.system("clear")


def chapter_to_str(chapter) -> str:
    """
    Takes a chapter parsed by the epub library and returns its content as plain text
    :param chapter: The chapter to read
    :return: Text content of the chapter
    """
    soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
    text = [para.get_text() for para in soup.find_all("p")]
    return " ".join(text)


def convert_epub_with_script(filename: str) -> None:
    """
    Converts an epub file in English / Latin script to a .txt file in Ender
    :param filename:
    :return:
    """

    # parse the epub file and find its documents/chapters
    book = epub.read_epub(filename)
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

    # let the user know what's going on
    print(f"Loaded epub containing {len(items)} chapters.")

    # iterate through the chapters and convert, saving after each chapter
    for item in tqdm.tqdm(items):

        input_text = chapter_to_str(item).lower()

        output_text = ""

        for c in tqdm.tqdm([char for char in input_text]):
            try:
                output_text += ENDER_KEY[c]
            except KeyError:
                output_text += c

        with open(filename.replace(".epub", ".txt"), "a", encoding="utf-8") as fh:
            fh.write(output_text)


def convert_epub_no_script(filename: str) -> None:
    # parse the epub file and find its documents/chapters
    book = epub.read_epub(filename)
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

    # let the user know what's going on
    print(f"Loaded epub containing {len(items)} chapters.")

    # iterate through the chapters and convert, saving after each chapter
    for item in tqdm.tqdm(items):

        input_text = chapter_to_str(item).lower()

        output_text = ""

        for c in tqdm.tqdm([char for char in input_text]):
            try:
                output_text += LATIN_KEY[c]
            except KeyError:
                output_text += c

        with open(filename.replace(".epub", ".txt"), "a", encoding="utf-8") as fh:
            fh.write(output_text)


def main():
    # get the file name
    file_input = input("Filename (epub): ")

    # check if the file exists; if not, re-request.
    if os.path.exists(file_input) and file_input.endswith(".epub"):
        print("Valid file located.")
    else:
        clear_console()
        print("Please enter the path to an existing .epub file.")
        main()

    # check if the user wants to use Ender script
    ender_script = input("Use Ender script? (y/n)")

    # prompt to begin conversion then convert
    input("Press [RETURN] to begin conversion")
    if ender_script == "y":
        convert_epub_with_script(file_input)
    else:
        convert_epub_no_script(file_input)

    # show when complete
    input("Conversion complete!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        input(f"{e}")
