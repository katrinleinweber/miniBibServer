# Conversions to/from HTML and LaTeX for Latin1 and Latin2 text entities.

# You need to run // sudo pip install bidict // to get this facility.
from bidict import namedbidict
import re

HTMLEntities = namedbidict('HTMLEntities', 'html_lookup', 'latex_lookup')

entities = HTMLEntities({
    "uogon":    "\\k{u}",
    "Uogon":     "\\k{U}",
    "uring":     "\\r{u}",
    "Uring":     "\\r{U}",
    "utilde":    "\\~{u}",
    "Utilde":    "\\~{U}",
    "wcirc":     "\\^{w}",
    "Wcirc":     "\\^{W}",
    "ycirc":     "\\^{y}",
    "Ycirc":     "\\^{Y}",
    "Yuml":      "\\\"{Y}",
    "zacute":    "\\'{z}",
    "Zacute":    "\\'{Z}",
    "zcaron":    "\\v{z}",
    "Zcaron":    "\\v{Z}",
    "zdot":      "\\.{z}",
    "Zdot":      "\\.{Z}",
    "ncaron":    "\\v{n}",
    "Ncaron":    "\\v{N}",
    "ncedil":    "\\c{n}",
    "Ncedil":    "\\c{N}",
    "odblac":    "\\H{o}",
    "Odblac":    "\\H{O}",
    "Omacr":     "\\={O}",
    "omacr":     "\\={o}",
    "oelig":     "\\oe",
    "OElig":     "\\OE",
    "racute":    "\\'{r}",
    "Racute":    "\\'{R}",
    "rcaron":    "\\v{r}",
    "Rcaron":    "\\v{R}",
    "rcedil":    "\\c{r}",
    "Rcedil":    "\\c{R}",
    "sacute":    "\\'{s}",
    "Sacute":    "\\'{S}",
    "scaron":    "\\v{s}",
    "Scaron":    "\\v{S}",
    "scedil":    "\\c{s}",
    "Scedil":    "\\c{S}",
    "scirc":     "\\^{s}",
    "Scirc":     "\\^{S}",
    "tcaron":    "\\v{t}",
    "Tcaron":    "\\v{T}",
    "tcedil":    "\\c{t}",
    "Tcedil":    "\\c{T}",
    "ubreve":    "\\u{u}",
    "Ubreve":    "\\u{U}",
    "udblac":    "\\H{u}",
    "Udblac":    "\\H{U}",
    "umacr":     "\\={u}",
    "Umacr":     "\\={U}",
    "Gdot":      "\\.{G}",
    "hcirc":     "\\^{h}",
    "Hcirc":     "\\^{H}",
    "Idot":      "\\.{I}",
    "Imacr":     "\\={I}",
    "imacr":     "\\={\\i}",
#    "ijlig":     "i\\kern -.15em j",
#    "IJlig":     "I\\kern -.15em J",
    "inodot":    "\\i",
    "iogon":     "\\k{i}",
    "Iogon":     "\\k{I}",
    "itilde":    "\\~{\\i}",
    "Itilde":    "\\~{I}",
    "jcirc":     "\\^{\\j}",
    "Jcirc":     "\\^{J}",
    "kcedil":    "\\c{k}",
    "Kcedil":    "\\c{K}",
    "kgreen":    "\\textsc{k}",
    "lacute":    "\\'{l}",
    "Lacute":    "\\'{L}",
    "lcaron":    "\\v{l}",
    "Lcaron":    "\\v{L}",
    "lcedil":    "\\c{l}",
    "Lcedil":    "\\c{L}",
    "lstrok":    "\\l",
    "Lstrok":    "\\L",
    "nacute":    "\\'{n}",
    "Nacute":    "\\'{N}",
    "eng":       "\\ng",
    "ENG":       "\\NG",
#    "napos":     "n\\kern-.2em\\textsf{'}",
    "abreve":    "\\u{a}",
    "Abreve":    "\\u{A}",
    "amacr":     "\\={a}",
    "Amacr":     "\\={A}",
    "aogon":     "\\k{a}",
    "Aogon":     "\\k{A}",
    "cacute":    "\\'{c}",
    "Cacute":    "\\'{C}",
    "ccaron":    "\\v{c}",
    "Ccaron":    "\\v{C}",
    "ccirc":     "\\^{c}",
    "Ccirc":     "\\^{C}",
    "cdot":      "\\.{c}",
    "Cdot":      "\\.{C}",
    "dcaron":    "\\v{d}",
    "Dcaron":    "\\v{D}",
    "dstrok":    "\\dj",
    "Dstrok":    "\\DJ",
    "ecaron":    "\\v{e}",
    "Ecaron":    "\\v{E}",
    "edot":      "\\.{e}",
    "Edot":      "\\.{E}",
    "emacr":     "\\={e}",
    "Emacr":     "\\={E}",
    "eogon":     "\\k{e}",
    "Eogon":     "\\k{E}",
    "gacute":    "\\'{g}",
    "gbreve":    "\\u{g}",
    "Gbreve":    "\\u{G}",
    "Gcedil":    "\\c{G}",
    "gcirc":     "\\^{g}",
    "Gcirc":     "\\^{G}",
    "gdot":      "\\.{g}",
    "Igrave":    "\\`{I}",
    "iuml":      "\\\"{\\i}",
    "Iuml":      "\\\"{I}",
    "ntilde":    "\\~{n}",
    "Ntilde":    "\\~{N}",
    "oacute":    "\\'{o}",
    "Oacute":    "\\'{O}",
    "ocirc":     "\\^{o}",
    "Ocirc":     "\\^{O}",
    "ograve":    "\\`{o}",
    "Ograve":    "\\`{O}",
    "oslash":    "\\o",
    "Oslash":    "\\O",
    "otilde":    "\\~{o}",
    "Otilde":    "\\~{O}",
    "ouml":      "\\\"{o}",
    "Ouml":      "\\\"{O}",
    "szlig":     "\\ss",
    "thorn":     "\\th",
    "THORN":     "\\TH",
    "uacute":    "\\'{u}",
    "Uacute":    "\\'{U}",
    "ucirc":     "\\^{u}",
    "Ucirc":     "\\^{U}",
    "ugrave":    "\\`{u}",
    "Ugrave":    "\\`{U}",
    "uuml":      "\\\"{u}",
    "Uuml":      "\\\"{U}",
    "yacute":    "\\'{y}",
    "Yacute":    "\\'{Y}",
    "yuml":      "\\\"{y}",
    "aacute":    "\\'{a}",
    "Aacute":    "\\'{A}",
    "acirc":     "\\^{a}",
    "Acirc":     "\\^{A}",
    "agrave":    "\\`{a}",
    "Agrave":    "\\`{A}",
    "aring":     "\\aa",
    "Aring":     "\\AA",
    "atilde":    "\\~{a}",
    "Atilde":    "\\~{A}",
    "auml":      "\\\"{a}",
    "Auml":      "\\\"{A}",
    "aelig":     "\\ae",
    "AElig":     "\\AE",
    "ccedil":    "\\c{c}",
    "Ccedil":    "\\c{C}",
    "eth":       "\\dh",
    "ETH":       "\\DH",
    "eacute":    "\\'{e}",
    "Eacute":    "\\'{E}",
    "ecirc":     "\\^{e}",
    "Ecirc":     "\\^{E}",
    "egrave":    "\\`{e}",
    "Egrave":    "\\`{E}",
    "euml":      "\\\"{e}",
    "Euml":      "\\\"{E}",
    "iacute":    "\\'{\\i}",
    "Iacute":    "\\'{I}",
    "icirc":     "\\^{\\i}",
    "Icirc":     "\\^{I}",
    "igrave":    "\\`{\\i}"
}
)

# print "entities.html_lookup euml should give " + "\\\"{e}: [" + entities.html_lookup["euml"] + "]."
# print "entities.latex_lookup \\'{a} should give " +  "aacute: [" + entities.latex_lookup["\\'{a}"] + "]."

"""
This direction is comparatively straightforward.
"""
def replace_html_accents (text):
    return re.sub(r"&([A-Za-z]+);", lambda match: entities.html_lookup[match.group(1)], text)

"""
The other direction requires that we need to compile
the LaTeX regexps into something we can use, so that's
what the next line does.
"""
match_latex_accents = re.compile('\\\\' + "(" + r'k{u}' + r'|' + r'k{U}' + r'|' + r'r{u}' + r'|' + r'r{U}' + r'|' + r'~{u}' + r'|' + r'~{U}' + r'|' + r'\^{w}' + r'|' + r'\^{W}' + r'|' + r'\^{y}' + r'|' + r'\^{Y}' + r'|' + r'"{Y}' + r'|' + r"'{z}" + r'|' + r"'{Z}" + r'|' + r'v{z}' + r'|' + r'v{Z}' + r'|' + r'.{z}' + r'|' + r'.{Z}' + r'|' + r'v{n}' + r'|' + r'v{N}' + r'|' + r'c{n}' + r'|' + r'c{N}' + r'|' + r'H{o}' + r'|' + r'H{O}' + r'|' + r'={O}' + r'|' + r'={o}' + r'|' + r'oe' + r'|' + r'OE' + r'|' + r"'{r}" + r'|' + r"'{R}" + r'|' + r'v{r}' + r'|' + r'v{R}' + r'|' + r'c{r}' + r'|' + r'c{R}' + r'|' + r"'{s}" + r'|' + r"'{S}" + r'|' + r'v{s}' + r'|' + r'v{S}' + r'|' + r'c{s}' + r'|' + r'c{S}' + r'|' + r'\^{s}' + r'|' + r'\^{S}' + r'|' + r'v{t}' + r'|' + r'v{T}' + r'|' + r'c{t}' + r'|' + r'c{T}' + r'|' + r'u{u}' + r'|' + r'u{U}' + r'|' + r'H{u}' + r'|' + r'H{U}' + r'|' + r'={u}' + r'|' + r'={U}' + r'|' + r'.{G}' + r'|' + r'\^{h}' + r'|' + r'\^{H}' + r'|' + r'.{I}' + r'|' + r'={I}' + r'|' + r'={\\i}' + r'|' + r'\i' + r'|' + r'k{i}' + r'|' + r'k{I}' + r'|' + r'~{\\i}' + r'|' + r'~{I}' + r'|' + r'\^{\\j}' + r'|' + r'\^{J}' + r'|' + r'c{k}' + r'|' + r'c{K}' + r'|' + r'textsc{k}' + r'|' + r"'{l}" + r'|' + r"'{L}" + r'|' + r'v{l}' + r'|' + r'v{L}' + r'|' + r'c{l}' + r'|' + r'c{L}' + r'|' + r'l' + r'|' + r'L' + r'|' + r"'{n}" + r'|' + r"'{N}" + r'|' + r'ng' + r'|' + r'NG' + r'|' + r'u{a}' + r'|' + r'u{A}' + r'|' + r'={a}' + r'|' + r'={A}' + r'|' + r'k{a}' + r'|' + r'k{A}' + r'|' + r"'{c}" + r'|' + r"'{C}" + r'|' + r'v{c}' + r'|' + r'v{C}' + r'|' + r'\^{c}' + r'|' + r'\^{C}' + r'|' + r'.{c}' + r'|' + r'.{C}' + r'|' + r'v{d}' + r'|' + r'v{D}' + r'|' + r'dj' + r'|' + r'DJ' + r'|' + r'v{e}' + r'|' + r'v{E}' + r'|' + r'.{e}' + r'|' + r'.{E}' + r'|' + r'={e}' + r'|' + r'={E}' + r'|' + r'k{e}' + r'|' + r'k{E}' + r'|' + r"'{g}" + r'|' + r'u{g}' + r'|' + r'u{G}' + r'|' + r'c{G}' + r'|' + r'\^{g}' + r'|' + r'\^{G}' + r'|' + r'.{g}' + r'|' + r"'{I}" + r'|' + r'"{\\i}' + r'|' + r'"{I}' + r'|' + r'~{n}' + r'|' + r'~{N}' + r'|' + r"'{o}" + r'|' + r"'{O}" + r'|' + r'\^{o}' + r'|' + r'\^{O}' + r'|' + r"`{o}" + r'|' + r"`{O}" + r'|' + r'o' + r'|' + r'O' + r'|' + r'~{o}' + r'|' + r'~{O}' + r'|' + r'"{o}' + r'|' + r'"{O}' + r'|' + r'ss' + r'|' + r'th' + r'|' + r'TH' + r'|' + r"'{u}" + r'|' + r"'{U}" + r'|' + r'\^{u}' + r'|' + r'\^{U}' + r'|' + r"`{u}" + r'|' + r"`{U}" + r'|' + r'"{u}' + r'|' + r'"{U}' + r'|' + r"'{y}" + r'|' + r"'{Y}" + r'|' + r'"{y}' + r'|' + "'{a}" + r'|' + r"'{A}" + r'|' + r'\^{a}' + r'|' + r'\^{A}' + r'|' + r"`{a}" + r'|' + r"`{A}" + r'|' + r'aa' + r'|' + r'AA' + r'|' + r'~{a}' + r'|' + r'~{A}' + r'|' + r'"{a}' + r'|' + r'"{A}' + r'|' + r'ae' + r'|' + r'AE' + r'|' + r'c{c}' + r'|' + r'c{C}' + r'|' + r'dh' + r'|' + r'DH' + r'|' + r"'{e}" + r'|' + r"'{E}" + r'|' + r'\^{e}' + r'|' + r'\^{E}' + r'|' + r"`{e}" + r'|' + r"`{E}" + r'|' + r'"{e}' + r'|' + r'"{E}' + r'|' + r"'{\\i}" + r'|' + r"'{I}" + r'|' + r'\^{\\i}' + r'|' + r'\^{I}' + r'|' + r"`{\\i}" + ")")

"""
Now this function is very similar to the other one, just needed a little more debugging.
"""
def printmatch(match):
    # print "Match: " + match.group(0)
    return "&" + entities.latex_lookup[match.group(0)] + ";"

def replace_latex_accents (text):
    return re.sub (match_latex_accents, lambda match: printmatch(match) , text)

# sample_text = r"\Degree{1926}{Ph.D.}{E&ouml;tv&ouml;s Lor&aacute;nd University}{Az &aacute;ltal&aacute;nos halmazelm&eacute;let axiomatikus fel&eacute;p&iacute;t&eacute;se [Die Axiomatisierung der Mengenlehre, Mathematische Zeitschrift 27, 669-752 (1928)]}{http://genealogy.math.ndsu.nodak.edu/id.php?id=53213}"

#sample_text= "\Degree{1926}{Ph.D.}{E\"{o}tv\"{o}s Lor\'{a}nd University}{Az \'{a}ltal\'{a}nos halmazelm\'{e}let axiomatikus fel\'{e}p\'{\i}t\'{e}se [Die Axiomatisierung der Mengenlehre, Mathematische Zeitschrift 27, 669-752 (1928)]}{http://genealogy.math.ndsu.nodak.edu/id.php?id=53213}"

print replace_html_accents(sample_text)
print replace_latex_accents(replace_html_accents(sample_text))

