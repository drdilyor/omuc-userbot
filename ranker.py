import json
import logging
import re

from Levenshtein import distance  # noqa

from util import normalize_uzbek

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_score(text: str):
    keywords = {
        'cert': {
            'weight': 5,
            'in_text': [
                'sertifikat',
                'sertifikatlar',
                'sert',
                'sertlar',
                'serfikat',
                'serfikatlar',
            ],
            'value': 0.0,
        },
        'sotish': {
            'weight': 5,
            'in_text': [
                'sotiladi',
                'sotamiz',
                'sotaman',
                'sotish',
            ],
            'value': 0.0,
        },
        'olib_beramiz': {
            'weight': 5,
            'in_text': [
                'olib beramiz',
                'oberamiz',
                'olib beraman',
                'oberaman',
                'oberish',
            ],
            'value': 0.0,
        },
        'qanday_oladi': {
            'weight': 5,
            'in_text': [
                *[
                    f'{i} {j}'
                    for i in (
                        'qanday',
                        'qanday qilib',
                        'qanaqa',
                        'qanaqa qilib',
                        'qanaqilib',
                        'qayerdan',
                        'qattan',
                    )
                    for j in (
                        'oladi',
                        'olish',
                    )
                ],
                'qattan',
                'olish',
                'oldi',
                'olmoq',
                'oladi',
            ],
            'value': 0.0,
        },
        'laboratoriya': {
            'weight': 5,
            'in_text': [
                'lab',
                'laboratoriya',
                'labratoriya',
                'laboratoriyasi',
                'laboratoriyasini',
                'laboratoriyasining',
                'laboratoriyadan',
                'labini',
                'labning',
                'labining',
                'labdan',
            ],
            'value': 0.0,
        },
        'javob': {
            'weight': 4,
            'in_text': [
                'javob',
                'javoblari',
                'javobi',
                'javobini',
            ],
            'value': 0.0,
        },
        'arzon': {
            'weight': 3,
            'in_text': [
                'arzon',
                'arzan',
                'arzondan',
                'arzongina',
            ],
            'value': 0.0,
        },
        'narxi': {
            'weight': 3,
            'in_text': [
                'narx',
                'narxlar',
                'narxi',
                'narxlari',
                'puli',
            ],
            'value': 0.0,
        },
        'kelishamiz': {
            'weight': 3,
            'in_text': [
                'kelishamiz',
                'kelishilgan',
                'kelishish',
            ],
            'value': 0.0,
        },
        'kerak': {
            'weight': 3,
            'in_text': [
                'kerak',
                'keray',
                'kerey',
                'kere',
                'kk',
            ],
            'value': 0.0,
        },
        'emoji_100': {
            'weight': 3,
            'in_text': ['💯'],
            'value': 0.0,
        },
        'kim': {
            'weight': 2,
            'in_text': [
                'kim',
                'kimga',
                'kimni',
            ],
            'value': 0.0,
        },
    }

    text = normalize_uzbek(text)
    text_words = re.findall(r'[a-z0-9💯]+', text)
    i = 0
    log.debug(f'{text_words=}')
    while i < len(text_words):
        for keyword, sus in keywords.items():
            current_max = 0.0
            for susword in sus['in_text']:
                sus_word_count = susword.count(' ') + 1
                text_word = ' '.join(text_words[i:i + sus_word_count]).casefold()
                log.debug(f'{text_word=}')
                log.debug(f'{susword=}')
                log.debug(f'{sus_word_count=}')

                if text_word == susword:
                    log.debug('exact match')
                    current_max = max(current_max, 1.0)
                    break
                elif len(susword) != 1 and distance(text_word, susword) == 1:
                    log.debug('very likely match')
                    current_max = max(current_max, 0.5)
                    break
                else:
                    log.debug('no match')
            sus['value'] += current_max

        i += 1

    sum_weighted = 0
    for sus in keywords.values():
        sum_weighted += sus['weight'] * sus['value']

    log.debug(json.dumps({k: v['value'] for k, v in keywords.items()}))
    log.info(f'{sum_weighted=} {text=}')
    return sum_weighted
