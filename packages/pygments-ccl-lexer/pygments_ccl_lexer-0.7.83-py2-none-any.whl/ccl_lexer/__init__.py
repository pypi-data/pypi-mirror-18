from pygments.lexers.sql import language_callback
from pygments.token import Keyword, Name, Operator, Text, Comment, Number, String, Punctuation, Token
# from pygments.lexers._postgres_builtins import KEYWORDS, DATATYPES, \
# PSEUDO_TYPES, PLPGSQL_KEYWORDS
from pygments.lexer import RegexLexer
from ccl_definition import TOKEN_ASSIGNMENTS, CCL_TOKENS


__all__ = ['CCL_Lexer']


def add_words(words, type):
    regex = r'(?i)(' + '|'.join(words) + r')\b'
    return (regex, type)


class CCL_Lexer(RegexLexer):
    name = 'CCL'
    aliases = ['ccl', 'prg']
    filenames = ['*.ccl']

    root = [
        (r'\s*', Text),
        (r'[0-9]+', Number.Integer),
        (r'([0-9]*\.[0-9]*|[0-9]+)(e[+-]?[0-9]+)?', Number.Float),

        # (r'\/\*(\*(?!\/)|[^*])*\*\/', Comment.Multiline),
        # (r';.*?\n', Comment.Single),
        # (r'\$[a-zA-Z0-9_]*\b', Name),
    ]

    # for _type, words in CCL_TOKENS.items():
    #     root.append(add_words(words, TOKEN_ASSIGNMENTS[_type]))

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
