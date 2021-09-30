import re


def normalize_uzbek(text):
    """Cyrillic to uzbek and other goodies"""
    text = text.casefold()
    cyrillic_to_latin = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'yo',
        'ж': 'j',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'x',
        'ц': 's',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sh',
        'ы': 'i',
        'ь': '',
        'э': 'e',
        'ю': 'yu',
        'я': 'ya',
    }
    res = []
    for c in text:
        res.append(cyrillic_to_latin.get(c, c))

    res = ''.join(res)
    res = res.replace('w', 'sh')
    res = re.sub('c(?!h)', 'ch', res)
    return res
