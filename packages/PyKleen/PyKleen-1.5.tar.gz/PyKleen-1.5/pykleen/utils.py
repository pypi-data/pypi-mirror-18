# -*- coding: utf-8 -*-
import math
import re

WSP = r'[ \t]'
CRLF = r'(?:\r\n)'
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'
QUOTED_PAIR = r'(?:\\.)'
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + WSP + r'+)'
CTEXT = r'[' + NO_WS_CTL + r'\x21-\x27\x2a-\x5b\x5d-\x7e]'
CCONTENT = r'(?:' + CTEXT + r'|' + QUOTED_PAIR + r')'

COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + r')*' + FWS + r'?\)'
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + FWS + '?' + COMMENT + '|' + \
       FWS + ')'
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?'
QTEXT = r'[' + NO_WS_CTL + \
        r'\x21\x23-\x5b\x5d-\x7e]'
QCONTENT = r'(?:' + QTEXT + r'|' + \
           QUOTED_PAIR + r')'
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
                r'?' + QCONTENT + r')*' + FWS + \
                r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
             QUOTED_STRING + r')'
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'
DCONTENT = r'(?:' + DTEXT + r'|' + \
           QUOTED_PAIR + r')'
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
                 r'(?:' + FWS + r'?' + DCONTENT + \
                 r')*' + FWS + r'?\]' + CFWS + r'?'
DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
         DOMAIN_LITERAL + r')'
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN

# A valid address will match exactly the 3.4.1 addr-spec.
VALID_ADDRESS_REGEXP = re.compile(r'^' + ADDR_SPEC + r'$')

PHONENUMBER_DUTCH_MOBILE = re.compile(r'^(\+316|06)[0-9]{8}$')
PHONENUMBER_DUTCH_PHONE = re.compile(r'^(\+31|0)[0-9]{9}$')


class Strength(object):
    FAILURE = 0
    WARNING = 1
    SUFFICIENT = 2
    EXCEPTIONAL = 3

    def __init__(self, value: str):
        self.value = value
        self.size = len(value)
        self.score = 0
        self.requirements = 0
        self.tests = list()


def calculate_strength(value: str) -> Strength:
    strength = Strength(value)

    tests = [
        number_of_characters,
        uppercase_letters,
        lowercase_letters,
        numbers,
        symbols,
        middle_numbers_or_symbols,
        requirements,
        letters_only,
        numbers_only,
        repeat_characters,
        consecutive_uppercase_letters,
        consecutive_lowercase_letters,
        consecutive_numbers,
        sequential,
    ]

    for test in tests:
        score, measure = test(strength)
        strength.score += score
        strength.tests.append([test.__name__, score, measure])

    strength.score = max(min(strength.score, 100), 0)

    return strength


def number_of_characters(s: Strength):
    minimum_length = 8
    result = s.size * 4

    if result > minimum_length * 4:
        s.requirements += 1
        return result, Strength.EXCEPTIONAL
    elif result == minimum_length * 4:
        s.requirements += 1
        return result, Strength.SUFFICIENT
    else:
        return result, Strength.FAILURE


def uppercase_letters(s: Strength):
    count = len(re.findall(r'[A-Z]', s.value))
    result = (s.size - count) * 2 if s.size > count > 0 else 0

    if result > 2:
        s.requirements += 1

    if count > 1:
        return result, Strength.EXCEPTIONAL
    elif count == 1:
        return result, Strength.SUFFICIENT
    else:
        return result, Strength.FAILURE


def lowercase_letters(s: Strength):
    count = len(re.findall(r'[a-z]', s.value))
    result = (s.size - count) * 2 if s.size > count > 0 else 0

    if result > 0:
        s.requirements += 1

    if count > 1:
        return result, Strength.EXCEPTIONAL
    elif count == 1:
        return result, Strength.SUFFICIENT
    else:
        return result, Strength.FAILURE


def numbers(s: Strength):
    count = len(re.findall(r'[0-9]', s.value))
    result = count * 4 if s.size > count > 0 else 0

    if result > 4:
        s.requirements += 1
        return result, Strength.EXCEPTIONAL
    elif result == 4:
        s.requirements += 1
        return result, Strength.SUFFICIENT
    else:
        return result, Strength.FAILURE


def symbols(s: Strength):
    count = len(re.findall(r'[^a-zA-Z0-9]', s.value))
    result = count * 6 if s.size > count > 0 else 0

    if result > 6:
        s.requirements += 1
        return result, Strength.EXCEPTIONAL
    elif result == 6:
        s.requirements += 1
        return result, Strength.SUFFICIENT
    else:
        return result, Strength.FAILURE


def middle_numbers_or_symbols(s: Strength):
    count = len(re.findall(r'[^a-zA-Z]', s.value[1:-1]))
    result = count * 2

    if result > 2:
        return result, Strength.EXCEPTIONAL
    elif result == 2:
        return result, Strength.SUFFICIENT
    else:
        return result, Strength.FAILURE


def requirements(s: Strength):
    result = s.requirements if s.requirements >= 4 else 0
    result *= 2

    if result > 8:
        return result, Strength.EXCEPTIONAL
    elif result == 8:
        return result, Strength.SUFFICIENT
    else:
        return result, Strength.FAILURE


def letters_only(s: Strength):
    if re.match(r'^[a-zA-Z]+$', s.value) is not None:
        return -s.size, Strength.WARNING
    else:
        return 0, Strength.SUFFICIENT


def numbers_only(s: Strength):
    if re.match(r'^[0-9]+$', s.value) is not None:
        return -s.size, Strength.WARNING
    else:
        return 0, Strength.SUFFICIENT


def repeat_characters(s: Strength):
    repetition = 0
    increment = 0

    for lx, letter in enumerate(s.value):
        found = False
        for ox, other in enumerate(s.value):
            if letter != other or lx == ox:
                # ignore different letters and the current letter
                continue

            found = True
            increment += abs(s.size / (ox - lx))

        if found:
            # when duplicate letters are found, calculate penalty
            repetition += 1
            uniqueness = s.size - repetition
            if uniqueness:
                increment = math.ceil(increment / uniqueness)
            else:
                increment = math.ceil(increment)

    if increment == 0:
        return 0, Strength.SUFFICIENT
    else:
        return -increment, Strength.WARNING


def consecutive_uppercase_letters(s: Strength):
    count = len(re.findall(r'[A-Z][A-Z]', s.value))
    result = count * 2

    if result == 0:
        return 0, Strength.SUFFICIENT
    else:
        return -result, Strength.WARNING


def consecutive_lowercase_letters(s: Strength):
    result = 0
    for item in re.findall(r'[a-z][a-z]+', s.value):
        result += len(item) - 1

    result *= 2

    if result == 0:
        return 0, Strength.SUFFICIENT
    else:
        return -result, Strength.WARNING


def consecutive_numbers(s: Strength):
    result = 0
    for item in re.findall(r'[0-9][0-9]', s.value):
        result += len(item)

    result *= 2

    if result == 0:
        return 0, Strength.SUFFICIENT
    else:
        return -result, Strength.WARNING


def sequential(s: Strength):
    sequences = [
        'abcdefghijklmnopqrstuvwxyz',
        'qwertyuiop',
        'asdfghjkl',
        'zxcvbnm',
        '1234567890',
        '!@#$%^&*()-=',
    ]
    sequences += [x[::-1] for x in sequences]

    result = 0

    letters = list(s.value.lower())
    lx = -1
    while len(letters):
        letter = letters.pop(0)
        lx += 1
        occurrences = 0

        for sequence in sequences:
            if letter not in sequence:
                continue

            next_letters = s.value[lx + 1:]
            for occurrences, next_letter in enumerate(next_letters):
                compare = sequence[occurrences + 1]
                if next_letter != compare:
                    occurrences -= 1
                    break

            if occurrences > 0:
                break

        if occurrences > 0:
            result += occurrences
            letters = letters[occurrences:]

    result *= 3

    if result == 0:
        return 0, Strength.SUFFICIENT
    else:
        return -result, Strength.WARNING
