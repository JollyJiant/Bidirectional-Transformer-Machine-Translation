from PythonTmx import from_tmx
import html
import re
from bs4 import BeautifulSoup

MIN_LEN = 3
MAX_LEN = 100
CHAR_RATIO_THRESHOLD = 0.65
LEN_RATIO_THRESHOLD = 0.30

def check_bracket_balance(segment):
    brackets = {'(': ')', '[': ']', '{': '}'}
    stack = []

    for char in segment:
        if char in brackets:
            stack.append(char)
        elif char in brackets.values():
            if not stack or brackets[stack.pop()] != char:
                return False

    return not stack

def remove_line_breaks(segment):
    replacements = ['\\n', '\\r', '\\t', '\\f', '\\v', '\\b']
    replacements.extend(['\n', '\r', '\t', '\f', '\v', '\b'])
    for replacement in replacements:
        segment = segment.replace(replacement, '')
    return segment

def clean(segment):
    # Detect and fix technical issues in the content – make sure no extra CRs or LFs!
    segment = remove_line_breaks(segment)
    segment = segment.replace('\\', '') # remove any instance of \

    # Normalize escaped characters/entities
    soup = BeautifulSoup(segment, 'html.parser')
    segment = soup.get_text()
    segment = re.sub(r'<.*?\d?[^\s]>', '', segment)
    segment = re.sub(r'&[a-z]+;', '', segment)

    # Normalize quotation marks
    segment = re.sub(r'“|”|«|»|‹|›|„|“|„|”|「|」|『|』', '\"', segment)
    segment = re.sub(r'‘|’', '\'', segment)
    # Toss out segments with imbalanced quotes
    balanced_quotes = segment.count('"') % 2 == 0
    if not balanced_quotes: return ''

    # Remove footnotes
    segment = re.sub(r'\b([a-zA-Z]+)\.\d+\b', r'\1', segment)

    # Remove segments that are too short or too long
    total_words = len(segment.split())
    if total_words < MIN_LEN or total_words > MAX_LEN: return ''

    # Check if a segment contains mostly/all non-text content
    total_chars = len(segment)
    alpha_chars = sum([char.isalpha() for char in segment])
    ratio = alpha_chars / total_chars
    if ratio < CHAR_RATIO_THRESHOLD: return ''

    # Remove unbalanced brackets
    if not check_bracket_balance(segment): return ''

    # Normalize whitespaces
    segment = re.sub(r'\s+', ' ', segment)

    return segment

en_set = set()
hy_set = set()

en_file = open('Final Project/Data/raw/en.txt', 'w')
hy_file = open('Final Project/Data/raw/hy.txt', 'w')

filenames = [
    # "tmx_files/MultiCCAligned.tmx",
    # "tmx_files/TED2020.tmx",
    # "tmx_files/NeuLab-TedTalks.tmx",
    "tmx_files/wikimedia.tmx",
]

for filename in filenames:
    tmx_file = from_tmx(filename)
    for tu in tmx_file.tus:
        en_tuv, hy_tuv = tu.tuvs
        en_contents = en_tuv.segment._content
        hy_contents = hy_tuv.segment._content

        en_value = ''.join([item if type(item)==str else 'UNKNOWN_TMX_OBJECT' for item in en_contents])
        hy_value = ''.join([item if type(item)==str else 'UNKNOWN_TMX_OBJECT' for item in hy_contents])

        if 'UNKNOWN_TMX_OBJECT' in en_value or 'UNKNOWN_TMX_OBJECT' in hy_value: continue

        en_value = clean(en_value)
        hy_value = clean(hy_value)

        if not (en_value and hy_value): continue
        if en_value == hy_value: continue

        en_len = len(en_value.split())
        hy_len = len(hy_value.split())
        len_ratio = min(en_len/hy_len, hy_len/en_len)
        if len_ratio <= LEN_RATIO_THRESHOLD: continue

        # skip duplicates (the source AND target pair have already been included)
        # this still allows a source with 2 different translations to be included
        if en_value in en_set and hy_value in hy_set: continue
        en_set.add(en_value)
        hy_set.add(hy_value)
        
        en_file.write(en_value + '\n')
        hy_file.write(hy_value + '\n')

en_file.close()
hy_file.close()
