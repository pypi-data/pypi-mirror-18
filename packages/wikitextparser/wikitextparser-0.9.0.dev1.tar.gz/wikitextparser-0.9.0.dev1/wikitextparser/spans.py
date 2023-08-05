﻿"""Define the functions required for parsing wikitext into spans."""


import re


# According to https://www.mediawiki.org/wiki/Manual:$wgLegalTitleChars
# illegal title characters are: r'[]{}|#<>[\u0000-\u0020]'
INVALID_TITLE_CHARS_PATTERN = r'\x00-\x1f\|\{\}\[\]<>\n'
# Templates
TEMPLATE_PATTERN = (
    r'\{\{\s*'
    r'[^' + INVALID_TITLE_CHARS_PATTERN + r']*'
    r'\s*(\|[^{}]*?\}\}|\}\})'
)
INVALID_NAME_TEMPLATE_REGEX = re.compile(
    r'\{\{\s*'
    r'[_\s]*'
    r'\s*(\|[^{}]*?\}\}|\}\})'
)
TEMPLATE_NOT_PARAM_REGEX = re.compile(
    TEMPLATE_PATTERN + r'(?!\})'
    r'|(?<!{)' + TEMPLATE_PATTERN
)
# Parameters
TEMPLATE_PARAMETER_REGEX = re.compile(r'\{\{\{[^{}]*?\}\}\}')
# Parser functions
# According to https://www.mediawiki.org/wiki/Help:Magic_words
# See also :
# https://translatewiki.net/wiki/MediaWiki:Sp-translate-data-MagicWords/fa
PARSER_FUNCTION_REGEX = re.compile(
    r"""
    \{\{\s*
    (?:
      \#[^{}\s]*?|
      # Variables acting like parser functions
      # Technical metadata
      DISPLAYTITLE|
      DEFAULT
      (?:CATEGORYSORT|SORT|SORTKEY)|
      # Statistics
      # The following variables accept ":R" flag
      NUM
      (?:
        BER
        (?:
          OF
          (?:
            PAGES|
            ARTICLES|
            FILES|
            EDITS|
            VIEWS|
            USERS|
            ADMINS|
            ACTIVEUSERS
          )|
          INGROUP
        )|
        INGROUP
      )|
      PAGESIN
      (?:
        CATEGORY|
        CAT|
        NS|
        NAMESPACE
      )|
      # Page names
      # These can all take a parameter, allowing
      # specification of the page to be operated on
      (?:
        (?:FULL)?|
        BASE|
        SUB
        (?:JECT)?|
        ARTICLE|
        TALK|
        ROOT
      )
      PAGENAMEE?|
      # Namespaces
      # Can take a full-page-name parameter
      (?:
        NAME|
        SUBJECT|
        ARTICLE|
        TALK
      )
      SPACEE?|
      NAMESPACENUMBER|
      # Parser functions
      # Technical metadata of another page
      PAGE
      (?:ID|SIZE)|
      PROTECTION(?:LEVEL|EXPIRY)|
      CASCADINGSOURCES|
      REVISION
      (?:
        ID|
        DAY2?|
        MONTH1?|
        YEAR|
        TIMESTAMP|
        USER
      )|
      # URL data
      (?:local|full|canonical)
      url|
      filepath|
      (?:url|anchor)
      encode|
      # Namespaces
      nse?|
      # Formatting
      formatnum|
      [lu]c
      (?:first)?|
      pad
      (?:left|right)|
      # Localization
      plural|
      grammar|
      gender|
      int
    )
    :[^{}]*?\}\}
    """,
    re.VERBOSE
)
# External links
VALID_EXTLINK_CHARS_PATTERN = r'[^ \\^`#<>\[\]\"\t\n{|}]*'
# See DefaultSettings.php on MediaWiki and
# https://www.mediawiki.org/wiki/Help:Links#External_links
VALID_EXTLINK_SCHEMES_PATTERN = (
    r'('
    r'bitcoin:|ftp://|ftps://|geo:|git://|gopher://|http://|https://|'
    r'irc://|ircs://|magnet:|mailto:|mms://|news:|nntp://|redis://|'
    r'sftp://|sip:|sips:|sms:|ssh://|svn://|tel:|telnet://|urn:|'
    r'worldwind://|xmpp:|//'
    r')'
)
BARE_EXTERNALLINK_PATTERN = (
    VALID_EXTLINK_SCHEMES_PATTERN.replace(r'|//', r'') +
    VALID_EXTLINK_CHARS_PATTERN
)
# Wikilinks
# https://www.mediawiki.org/wiki/Help:Links#Internal_links
WIKILINK_REGEX = re.compile(
    r'\[\[(?!' + BARE_EXTERNALLINK_PATTERN + r')' +
    '[^' + INVALID_TITLE_CHARS_PATTERN.replace(r'\{\}', '') + ']*'
    r'(\]\]|\|(?:[\S\s](?!\[\[))*?\]\])',
    re.IGNORECASE,
)
# For a complete list of extension tags on your wiki, see the
# "Parser extension tags" section at the end of [[Special:Version]].
# <templatedata> and <includeonly> were manually added to the  following list.
# A simple trick to find out if a tag should be listed here or not is as
# follows:
# Create the {{text}} template in your wiki (You can copy the source code from
# English Wikipedia). Then save the following in a test page:
# {{text|0<tagname>1}}2</tagname>3}}4
# If the ending braces in the rendered result appear between 3 and 4, then
# `tagname` is not an extension tag (e.g. <small>). Otherwise, i.e. if those
# braces appear between 1 and 2 or completely don't show up, `tagname` is
# probably an extension tag (e.g.: <pre>).
TAG_EXTENSIONS = [
    'ref',
    'math',
    'source',
    'syntaxhighlight',
    'pre',
    'poem',
    'hiero',
    'score',
    'includeonly',
    'timeline',
    'nowiki',
    'categorytree',
    'charinsert',
    'references',
    'imagemap',
    'inputbox',
    'section',
    'templatedata',
    'gallery',
    'graph',
    'indicator',
]
# The idea of the following regex to detect innermost HTML tags is from
# http://blog.stevenlevithan.com/archives/match-innermost-html-element
# But probably not bullet proof:
# https://stackoverflow.com/questions/3076219/
EXTENSION_TAGS_REGEX = re.compile(
    r'<(' + '|'.join(TAG_EXTENSIONS) +
    r""")
    \b[^>]*
    (?<!/)
    > # content
    (?:
      # no tags are nested inside
      (?=
        ([^<]+)
      )
      \2|
      # the nested-tag is something else
      <
      (?!\1\b[^>]*>)|
      # the nested tag closes itself
      <\1\b[^>]*/>
    )*?
    # tag-end
    </\1\s*>""",
    re.IGNORECASE | re.VERBOSE,
)
# Contents of the some of the tags mentioned above can be parsed as wikitext.
# For example, templates are valid inside the poem tag:
#    <poem>{{text|Hi!}}</poem>
# But not within math or source or ...
# for more information about the <categorytree> tag see:
# https://www.mediawiki.org/wiki/Extension:CategoryTree#
#    The_.7B.7B.23categorytree.7D.7D_parser_function
PARSABLE_TAG_EXTENSIONS = [
    'ref',
    'poem',
    'includeonly',
    'categorytree',
    'references',
    'imagemap',
    'inputbox',
    'section',
    'gallery',
    'indicator',
]
COMMENT_REGEX = re.compile(
    r'<!--.*?-->',
    re.DOTALL,
)
SINGLE_BRACES_REGEX = re.compile(r'(?<!{){(?=[^{])|(?<!})}(?=[^}])')


def parse_to_spans(string: str) -> dict:
    """Calculate and set self._type_to_spans.

    The result is a dictionary containing lists of spans:
    {
        'parameters': parameter_spans,
        'functions': parser_function_spans,
        'templates': template_spans,
        'wikilinks': wikilink_spans,
        'comments': comment_spans,
        'exttags': extension_tag_spans,
    }

    """
    comment_spans = []
    extension_tag_spans = []
    wikilink_spans = []
    parameter_spans = []
    parser_function_spans = []
    template_spans = []
    # HTML <!-- comments -->
    for match in COMMENT_REGEX.finditer(string):
        comment_spans.append(match.span())
        group = match.group()
        string = string.replace(group, ' ' * len(group))
    # <extension tags>
    for match in EXTENSION_TAGS_REGEX.finditer(string):
        span = match.span()
        extension_tag_spans.append(span)
        group = match.group()
        string = string.replace(group, '_' * len(group))
        if any(
            (group.startswith('<' + pte) for pte in PARSABLE_TAG_EXTENSIONS)
        ):
            parse_substring_to_spans(
                group[3:-3],
                span[0] + 3,
                wikilink_spans,
                parameter_spans,
                parser_function_spans,
                template_spans,
            )
    # Remove the braces inside WikiLinks.
    # WikiLinks may contain braces that interfere with
    # detection of templates. For example when parsing `{{text |[[A|}}]] }}`,
    # the span of the template should be the whole string.
    loop = True
    while loop:
        loop = False
        for match in WIKILINK_REGEX.finditer(string):
            loop = True
            span = match.span()
            wikilink_spans.append(span)
            group = match.group()
            parse_to_spans_innerloop(
                group,
                span[0],
                parameter_spans,
                parser_function_spans,
                template_spans,
            )
            string = string.replace(
                group,
                '_[' + group[2:-2].replace('}', '_').replace('{', '_') + ']_'
            )
    parse_to_spans_innerloop(
        string,
        0,
        parameter_spans,
        parser_function_spans,
        template_spans,
    )
    return {
        'parameters': parameter_spans,
        'functions': parser_function_spans,
        'templates': template_spans,
        'wikilinks': wikilink_spans,
        'comments': comment_spans,
        'exttags': extension_tag_spans,
    }


def parse_substring_to_spans(
    substring: str,
    index: int,
    wikilink_spans: list,
    parameter_spans: list,
    parser_function_spans: list,
    template_spans: list,
) -> None:
    """Parse the substring to spans.

    This function is basically the same as `parse_to_spans`, but accepts an
    index that indicates the start of the substring. `substrings` are the
    contents of PARSABLE_TAG_EXTENSIONS.

    """
    # Todo: Do we need to parse for nested tag extensions?
    # Remove the braces inside WikiLinks.
    # WikiLinks may contain braces that interfere with
    # detection of templates. For example when parsing `{{text |[[A|}}]] }}`,
    # the span of the template should be the whole string.
    loop = True
    while loop:
        loop = False
        for match in WIKILINK_REGEX.finditer(substring):
            loop = True
            ss, se = match.span()
            wikilink_spans.append((index + ss, index + se))
            group = match.group()
            parse_to_spans_innerloop(
                group,
                index + ss,
                parameter_spans,
                parser_function_spans,
                template_spans,
            )
            substring = substring.replace(
                group,
                '_[' + group[2:-2].replace('}', '_').replace('{', '_') + ']_'
            )
    parse_to_spans_innerloop(
        substring,
        index,
        parameter_spans,
        parser_function_spans,
        template_spans,
    )


def parse_to_spans_innerloop(
    string: str,
    index: int,
    parameter_spans: list,
    parser_function_spans: list,
    template_spans: list,
) -> None:
    """Run the main loop for _get_spans.

    :string: The string or part of string that is being parsed.
    :index: Add to every returned index.

    This function was created because the _get_spans function needs to
    call it n + 1 time. One time for the whole string and n times for
    each of the n WikiLinks.

    """
    while True:
        # Single braces will interfere with detection of other elements and
        # should be removed beforehand.
        string = SINGLE_BRACES_REGEX.sub('_', string)
        # Also remove empty double braces
        loop = True
        while loop:
            loop = False
            for match in INVALID_NAME_TEMPLATE_REGEX.finditer(string):
                loop = True
                group = match.group()
                string = string.replace(group, len(group) * '_')
        # The following was much more faster than
        # string = re.sub(r'{(?=[^}]*$)', '_', string)
        head, sep, tail = string.rpartition('}')
        string = ''.join((head, sep, tail.replace('{', '_')))
        # Also Python does not support non-fixed-length lookbehinds
        head, sep, tail = string.partition('{')
        string = ''.join((head.replace('}', '_'), sep, tail))
        match = None
        # Template parameters
        loop = True
        while loop:
            loop = False
            for match in TEMPLATE_PARAMETER_REGEX.finditer(string):
                loop = True
                ss, se = match.span()
                parameter_spans.append((ss + index, se + index))
                group = match.group()
                string = string.replace(group, '___' + group[3:-3] + '___')
        # Templates
        loop = True
        while loop:
            # Parser functions
            while loop:
                loop = False
                for match in PARSER_FUNCTION_REGEX.finditer(string):
                    loop = True
                    ss, se = match.span()
                    parser_function_spans.append((ss + index, se + index))
                    group = match.group()
                    string = string.replace(
                        group, '__' + group[2:-2] + '__'
                    )
            # loop is False at this point
            for match in TEMPLATE_NOT_PARAM_REGEX.finditer(string):
                loop = True
                ss, se = match.span()
                template_spans.append((ss + index, se + index))
                group = match.group()
                string = string.replace(group, '__' + group[2:-2] + '__')
        if not match:
            break
