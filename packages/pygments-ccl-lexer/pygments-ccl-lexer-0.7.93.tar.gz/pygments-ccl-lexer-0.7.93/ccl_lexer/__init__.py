from pygments.lexers.sql import language_callback
from pygments.token import Keyword, Name, Operator, Text, Comment, Number, String, Punctuation, Token
from pygments.lexer import bygroups, words
from pygments.lexers.sql import PostgresLexer
from ccl_definition import TOKEN_ASSIGNMENTS, CCL_TOKENS
import re
# from pygments.lexers._postgres_builtins import KEYWORDS, DATATYPES, \
# PSEUDO_TYPES, PLPGSQL_KEYWORDS


__all__ = ['CCL_Lexer']


def add_words(words, type):
    regex = r'(?i)(' + '|'.join(words) + r')\b'
    return (regex, type)


class CCL_Lexer(PostgresLexer):
    name = 'CCL'
    aliases = ['ccl', 'prg']
    filenames = ['*.ccl']


    flags = re.IGNORECASE

    root = [
        (r'\s+', Text),
        (r'--.*\n?', Comment.Single),
        (r'/\*', Comment.Multiline, 'multiline-comments')
    ]

        # (r'(' + '|'.join(s.replace(" ", "\s+")
        #                  for s in DATATYPES + PSEUDO_TYPES)
        #  + r')\b', Name.Builtin),
    for _type, words in CCL_TOKENS.items():
        root.append((words(words, suffix=r'\b'), _type))

    root.extend(
        [(r'[+*/<>=~!@#%^&|`?-]+', Operator),
        # (r'::', Operator),  # cast
        (r'\$\d+', Name.Variable),
        (r'([0-9]*\.[0-9]*|[0-9]+)(e[+-]?[0-9]+)?', Number.Float),
        (r'[0-9]+', Number.Integer),
        (r"((?:E|U&)?)(')", bygroups(String.Affix, String.Single), 'string'),
        # quoted identifier
        (r'((?:U&)?)(")', bygroups(String.Affix, String.Name), 'quoted-ident'),
        (r'(?s)(\$)([^$]*)(\$)(.*?)(\$)(\2)(\$)', language_callback),
        (r'[a-z_]\w*', Name),

        # psql variable in SQL
        (r""":(['"]?)[a-z]\w*\b\1""", Name.Variable),

        (r'[;:()\[\]{},.]', Punctuation),
    ])
    multiline_comments = [
        (r'/\*', Comment.Multiline, 'multiline-comments'),
        (r'\*/', Comment.Multiline, '#pop'),
        (r'[^/*]+', Comment.Multiline),
        (r'[/*]', Comment.Multiline)
    ],
    string_type = [
        (r"[^']+", String.Single),
        (r"''", String.Single),
        (r"'", String.Single, '#pop'),
    ]
    quoted_ident = [
        (r'[^"]+', String.Name),
        (r'""', String.Name),
        (r'"', String.Name, '#pop'),
    ]
    tokens = {
    'root': root,
    'multiline-comments': multiline_comments,
    'string': string_type,
    'quoted-ident': quoted_ident
    }








def ignore():

    root = [
        (r'\s*', Text),
        (r'[0-9]+', Number.Integer),
        (r'([0-9]*\.[0-9]*|[0-9]+)(e[+-]?[0-9]+)?', Number.Float),

        # (r'\/\*(\*(?!\/)|[^*])*\*\/', Comment.Multiline),
        # (r';.*?\n', Comment.Single),
        # (r'\$[a-zA-Z0-9_]*\b', Name),
    ]

    for _type, words in CCL_TOKENS.items():
        root.append(add_words(words, TOKEN_ASSIGNMENTS[_type]))

    root.extend([
        # (r'[+*/<>=~!@#%^&|`?-]', Operator),
        # (r'[0-9]+', Number.Integer),
        # (r"'(''|[^'])*'", String.Single),
        # (r'"(""|[^"])*"', String.Symbol),
        # (r'[;:()\[\],\.]', Punctuation),
        (r'.*[\n[\s]?]?', Text),
    ])

    tokens = {
        'root': root,
        # 'multiline-comments': [
        #     # (r'/\*', Comment.Multiline, 'multiline-comments'),
        #     # (r'\*/', Comment.Multiline, '#pop'),
        #     # (r'[^/\*]+', Comment.Multiline),
        #     # (r'[/*]', Comment.Multiline)
        # ],
    }
