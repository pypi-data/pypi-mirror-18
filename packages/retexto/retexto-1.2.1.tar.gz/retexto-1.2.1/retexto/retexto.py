# -*- coding: UTF-8 -*-
import re
import unicodedata
import string
import sys
from .unicodes_codes import *
from .stopwords import *


PY2 = int(sys.version[0]) == 2

if PY2:
    from unidecode import unidecode
    TEXT_TYPE = unicode
    BINARY_TYPE = str
    STR_TYPES = (str, unicode)
    IS_CHAR = list(unicode(string.ascii_letters, 'utf-8'))
else:
    TEXT_TYPE = str
    BINARY_TYPE = bytes
    unicode = str
    STR_TYPES = (str, )
    IS_CHAR = list(string.ascii_letters)
    basestring = (str, bytes)
    unidecode = str

MAP_CHARS = dict()
MAP_CHARS.update({ord(' '): ' '})
for c in IS_CHAR:
    MAP_CHARS.update({ord(unicode(c)): c})
ENCODE = 'utf-8'
STR_PUNC = list(string.punctuation)
REGEX_HTML = re.compile(r'<[^>]*>')
REGEX_MENTIONS = re.compile(r'\S*[@](?:\[[^\]]+\]|\S+)')
REGEX_TAGS = re.compile(r'\S*[#](?:\[[^\]]+\]|\S+)')
REGEX_SMILES = re.compile(r'([j|h][aeiou]){2,}')
REGEX_VOWELS = re.compile(r'([aeiou])\1+')
REGEX_CONSONANTS = re.compile(r'([b-df-hj-np-tv-z])\1+')
REGEX_SPACES = re.compile(r' +')
REGEX_URLS = re.compile(r'(www|http|https)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|\
[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
MAP_SPECIALS = dict((
    (ord(u'Á'), u'a'), (ord(u'É'), u'e'), (ord(u'Í'), u'i'),
    (ord(u'Ó'), u'o'), (ord(u'Ú'), u'u'), (ord(u'Ñ'), u'ñ'),
    (ord(u'À'), u'a'), (ord(u'È'), u'e'), (ord(u'Ì'), u'i'),
    (ord(u'Ò'), u'o'), (ord(u'Ù'), u'u'), (ord(u'ç'), u'c'),
    (ord(u'á'), u'a'), (ord(u'é'), u'e'), (ord(u'í'), u'i'),
    (ord(u'ó'), u'o'), (ord(u'ú'), u'u'), (ord(u'ñ'), u'ñ'),
    (ord(u'à'), u'a'), (ord(u'è'), u'e'), (ord(u'ì'), u'i'),
    (ord(u'ò'), u'o'), (ord(u'ù'), u'u'), (ord(u'ü'), u'u'),
    (ord(u'ä'), u'a'), (ord(u'ë'), u'e'), (ord(u'ï'), u'i'),
    (ord(u'ö'), u'o'), (ord(u'ü'), u'u'), (ord(u'ÿ'), u'y'),
    (ord(u'Ç'), u'c')
))
# REGEX_EMOJIS = re.compile(r'[\uDC00-\uDFFF]')
# REGEX_EMOJIS = re.compile(ur'[U00010000-U0010ffff]')
# REGEX_EMOJIS = re.compile(r'[\uDC00-\uDFFF]', re.UNICODE)
# REGEX_EMOJIS = re.compile(r'[U00010000-U0010ffff]', re.UNICODE)
REGEX_EMOJIS = re.compile(u'[\U0001F600-\U0001F64F]', re.UNICODE)


# print unidecode(u'😂'.decode(ENCODE))
class ReTexto:
    @classmethod
    def __init__(self, text):
        if len(text):
            self.TEXT = text.rstrip()
        else:
            raise 'len text is 0'

    @classmethod
    def __repr__(self):
        return self.TEXT

    @staticmethod
    def is_unicode(v, encoding='utf-8'):
        if isinstance(encoding, basestring):
            encoding = ((encoding,),) + \
                        (('windows-1252',), (ENCODE, 'ignore'))
        if isinstance(v, BINARY_TYPE):
            for e in encoding:
                try:
                    return v.decode(*e)
                except:
                    pass
            return v
        return unicode(v)

    @classmethod
    def remove_html(self, by=''):
        try:
            return ReTexto(re.sub(REGEX_HTML, by, self.TEXT))
        except Exception as e:
            print(e)

    @classmethod
    def remove_mentions(self, by=''):
        try:
            return ReTexto(re.sub(
                                REGEX_MENTIONS,
                                by, self.is_unicode(self.TEXT)))
        except Exception as e:
            print(e)

    @classmethod
    def remove_tags(self, by=''):
        try:
            return ReTexto(re.sub(REGEX_TAGS, by, self.TEXT))
        except Exception as e:
            print(e)

    @classmethod
    def remove_smiles(self, by=''):
        try:
            return ReTexto(re.sub(REGEX_SMILES, by, self.TEXT))
        except Exception as e:
            print(e)

    @classmethod
    def remove_punctuation(self, by=''):
        l_text = []
        for char in list(self.TEXT):
            if not (char in STR_PUNC):
                l_text.append(char)
                continue
            l_text.append(by)
        return ReTexto(''.join(l_text))

    @classmethod
    def remove_nochars(self, preserve_tilde=False):
        chars = MAP_CHARS
        if preserve_tilde:
            chars.update(MAP_SPECIALS)
        l_char = chars.keys()
        l_text = []
        for char in list(self.TEXT):
            c = ord(char)
            if c in l_char:
                l_text.append(char)
                continue
        return ReTexto(''.join(l_text))

    @classmethod
    def remove_stopwords(self, lang=None):
        l_text = []
        sw = stopwords(lang)
        for char in self.split_words():
            if not (self.is_unicode(char) in sw):
                l_text.append(char)
        return ReTexto(' '.join(l_text))

    @classmethod
    def convert_specials(self):
        return ReTexto(unidecode(self.is_unicode(self.TEXT)))

    @classmethod
    def convert_emoji(self):
        text = self.TEXT
        if PY2:
            if not isinstance(self.TEXT, unicode):
                text = self.TEXT.decode('utf-8')
            r = re.sub(REGEX_EMOJIS, lambda m: emoji_name(m), text)
            r = r.encode(ENCODE)
        else:
            r = re.sub(REGEX_EMOJIS, lambda m: emoji_name(m), text)
        return ReTexto(r)

    @classmethod
    def remove_url(self, by=''):
        return ReTexto(re.sub(REGEX_URLS, '', self.TEXT))

    @classmethod
    def remove_duplicate_consonants(self):
        return ReTexto(re.sub(REGEX_CONSONANTS, r'\1', self.TEXT))

    @classmethod
    def remove_duplicate(self, r='a-z'):
        p = re.compile(r'([%s])\1+' % r)
        return ReTexto(re.sub(p, r'\1', self.TEXT))

    @classmethod
    def remove_duplicate_vowels(self):
        return ReTexto(re.sub(REGEX_VOWELS, r'\1', self.TEXT))

    @classmethod
    def remove_multispaces(self):
        return ReTexto(re.sub(REGEX_SPACES, ' ', self.TEXT))

    @classmethod
    def split_words(self, uniques=False):
        l = self.TEXT.split()
        return list(set(l)) if uniques else l

    @classmethod
    def lower(self):
        return ReTexto(self.TEXT.lower())
