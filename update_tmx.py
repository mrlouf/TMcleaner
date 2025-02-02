import re
import sys

from xml_utils import update_tmx

""" Text update rules """



def normalise_interrogation(lang_code, segment_text):
    if lang_code.startswith("fr"):
        segment_text = re.sub(r"(\S)\?", r"\1 ?", segment_text)
    return segment_text

def normalise_exclamation(lang_code, segment_text):
    if lang_code.startswith("fr"):
        segment_text = re.sub(r"(\S)!", r"\1 !", segment_text)
    return segment_text

def normalise_semicolon(lang_code, segment_text):
    if lang_code.startswith("fr"):
        segment_text = re.sub(r"(\S);", r"\1 ;", segment_text)
    return segment_text
        
def normalise_colon(lang_code, segment_text):
    if lang_code.startswith("fr"): # and not segment_text.find(r"(http|www)"): # Exclude URLs
        segment_text = re.sub(r"(\S):", r"\1 :", segment_text)
    return segment_text
        
def normalise_openquote(lang_code, segment_text):
    if lang_code.startswith("fr"):
        segment_text = re.sub(r"«(\S)", r"« \1", segment_text)
    return segment_text

def normalise_endquote(lang_code, segment_text):
    if lang_code.startswith("fr"):
        segment_text = re.sub(r"(\S)»", r"\1 »", segment_text)
    return segment_text

if __name__ == "__main__":

    original_tmx_file = sys.argv[1]
	
    text_update_rules = [
        normalise_interrogation,
        normalise_exclamation,
        normalise_semicolon,
        normalise_colon,
        normalise_openquote,
        normalise_endquote
    ]

    update_tmx(original_tmx_file, text_update_rules)

    