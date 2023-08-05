from .characters import add_diacritic
from .characters import ACUTE, CIRCUMFLEX, SHORT, LONG, SMOOTH, ROUGH
from .syllabify import onset_nucleus_coda, syllabify, UNKNOWN, syllable_length
from .syllabify import syllable_accent, ultima, penult, antepenult


def syllable_add_accent(s, a):
    o, n, c = onset_nucleus_coda(s)
    if o in [SMOOTH, ROUGH]:
        return add_diacritic(add_diacritic(n, o), a) + c
    else:
        return o + add_diacritic(n, a) + c


def add_accent(s, accent_type):
    pos, accent = accent_type
    final = s[1 - pos:] if pos > 1 else [""]
    return "".join(s[:-pos] + [syllable_add_accent(s[-pos], accent)] + final)


OXYTONE = 1, ACUTE
PERISPOMENON = 1, CIRCUMFLEX
PAROXYTONE = 2, ACUTE
PROPERISPOMENON = 2, CIRCUMFLEX
PROPAROXYTONE = 3, ACUTE


def display_accent_type(accent_type):
    return {
        OXYTONE: "oxytone",
        PERISPOMENON: "perispomenon",
        PAROXYTONE: "paroxytone",
        PROPERISPOMENON: "properispomenon",
        PROPAROXYTONE: "proparoxytone",
    }[accent_type]


def make_oxytone(w):
    return add_accent(syllabify(w), OXYTONE)


def make_paroxytone(w):
    return add_accent(syllabify(w), PAROXYTONE)


def make_proparoxytone(w):
    return add_accent(syllabify(w), PROPAROXYTONE)


def make_perispomenon(w):
    s = syllabify(w)
    if PERISPOMENON in possible_accentuations(s):
        return add_accent(s, PERISPOMENON)
    else:
        return add_accent(s, OXYTONE)


def make_properispomenon(w):
    s = syllabify(w)
    if PROPERISPOMENON in possible_accentuations(s):
        return add_accent(s, PROPERISPOMENON)
    else:
        return add_accent(s, PAROXYTONE)


def get_accent_type(w):
    u = syllable_accent(ultima(w))
    if u == ACUTE:
        return OXYTONE
    elif u == CIRCUMFLEX:
        return PERISPOMENON
    p = syllable_accent(penult(w))
    if p == ACUTE:
        return PAROXYTONE
    elif p == CIRCUMFLEX:
        return PROPERISPOMENON
    a = syllable_accent(antepenult(w))
    if a == ACUTE:
        return PROPAROXYTONE


def possible_accentuations(
        s, treat_final_AI_OI_short=True, default_short=False
):
    ultima_length = syllable_length(s[-1], treat_final_AI_OI_short)
    penult_length = syllable_length(s[-2], False) if len(s) >= 2 else None
    if ultima_length == UNKNOWN and default_short:
        ultima_length = SHORT
    if penult_length == UNKNOWN and default_short:
        penult_length = SHORT

    if ultima_length == SHORT:
        if len(s) >= 2:
            if len(s) >= 3:
                yield PROPAROXYTONE
            if penult_length == SHORT:
                yield PAROXYTONE
            elif penult_length == LONG:
                yield PROPERISPOMENON
            elif penult_length == UNKNOWN:
                # conditional on short penult
                yield PAROXYTONE
                # conditional on long penult
                yield PROPERISPOMENON
        yield OXYTONE
    elif ultima_length == LONG:
        if len(s) >= 2:
            yield PAROXYTONE
        yield OXYTONE
        yield PERISPOMENON
    elif ultima_length == UNKNOWN:
        if len(s) >= 2:
            if len(s) >= 3:
                # conditional on short ultima
                yield PROPAROXYTONE
            if penult_length == SHORT:
                yield PAROXYTONE
            elif penult_length == LONG:
                # conditional on short ultima
                yield PROPERISPOMENON
            elif penult_length == UNKNOWN:
                # conditional on short penult
                yield PAROXYTONE
                # conditional on long penult
                yield PROPERISPOMENON
        # conditional on long ultima
        yield PERISPOMENON
        yield OXYTONE


def recessive(w, treat_final_AI_OI_short=True, default_short=False):
    if "|" in w:
        pre, w = w.split("|")
    else:
        pre = ""

    s = syllabify(w)
    return pre + add_accent(
        s,
        sorted(
            possible_accentuations(s, treat_final_AI_OI_short, default_short),
            reverse=True
        )[0]
    )


def on_penult(w, default_short=False):
    if "|" in w:
        pre, w = w.split("|")
    else:
        pre = ""

    s = syllabify(w)
    accentuations = list(
        possible_accentuations(s, default_short=default_short)
    )
    if PROPERISPOMENON in accentuations:
        return pre + add_accent(s, PROPERISPOMENON)
    elif PAROXYTONE in accentuations:
        return pre + add_accent(s, PAROXYTONE)


def persistent(w, lemma):
    w = w.replace("|", "")

    place, accent = get_accent_type(lemma)
    s = syllabify(w)
    possible = list(possible_accentuations(s))
    place2 = len(s) - len(syllabify(lemma)) + place
    accent_type = (place2, accent)
    if accent_type not in possible:
        if accent == ACUTE and (place2, CIRCUMFLEX) in possible:
            accent_type = (place2, CIRCUMFLEX)
        else:
            for i in range(1, 4):
                if (place2 - i, ACUTE) in possible:
                    accent_type = (place2 - i, ACUTE)
                    break
    return add_accent(s, accent_type)
