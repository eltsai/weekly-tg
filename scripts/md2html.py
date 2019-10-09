#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author='nvander1, E-Tsai'
#Kudos to Nik Vanderhoof! https://github.com/nvander1

"""
Convert Markdown into HTML.
This script is modified to suite requirements
of telegra.ph API: https://telegra.ph/api#Node
"""

import re


def paragraphs(corpus):
    """
    >>> text = 'P1\n\nP2\nP2\n    \t   \n\n\n  \t\nP3'
    >>> paragraphs(text)
    '<p>P1</p>\n<p>P2\nP2</p>\n<p>P3</p>'
    """
    inner_paras_added = re.sub(r'\n\s*\n', '</p>\n<p>', corpus)
    all_paras_added = f'<p>{inner_paras_added}</p>'
    return all_paras_added


def inline_links(corpus):
    """
    >>> simple = 'This is an [example link](http://example.com/).'
    >>> inline_links(simple)
    'This is an <a href="http://example.com/">example link</a>.'
    >>> titled = 'This is an [example link](http://example.com/ "With a Title").'
    >>> inline_links(titled)
    'This is an <a href="http://example.com/" title="With a Title">example link</a>.'
    """
    with_titles = re.sub(r'\[(.*)\]\((\S*?)[ \t]*?(".*?")\)', r'<a href="\g<2>" title=\g<3>>\g<1></a>', corpus)
    all_inline_links = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\g<2>">\g<1></a>', with_titles)
    return all_inline_links


def images(corpus):
    """
    >>> simple = 'This is an ![image](http://example.com/).'
    >>> inline_links(simple)
    'This is an <img src="http://example.com/" alt="image">.'
    """
    with_titles = re.sub(r'\!\[(.*)\]\((\S*)[ \t]*(".*")\)', r'<a href="\g<2>" title=\g<3>>\g<1></a>', corpus)
    all_inline_links = re.sub(r'\!\[(.*)\]\((.*)\)', r'<img src="\g<2>" alt="\g<1>">', with_titles)
    return all_inline_links


def lists(corpus):
    """
    >>> ul_test = '- i1\n+ i2\n* i3'
    >>> lists(ul_test)
    '<ul><li>i1</li>\n<li>i2</li>\n<li>i3</li></ul>'
    >>> ul_test = '2. i1\n69. i2\n1337. i3'
    >>> lists(ul_test)
    '<ol><li>i1</li>\n<li>i2</li>\n<li>i3</li></ol>'
    >>> mixed_test = '- P1\n78. P2\n* P3'
    >>> lists(mixed_test)
    '<ul><li>P1</li></ul>\n\n<ol><li>P2</li></ol>\n\n<ul><li>P3</li></ul>'
    """
    # wrap each unordered item in its own list
    # ul_wrapped = re.sub(r'(-|\+|\*) (.*)', r'<ul><li>\g<2></li></ul>', corpus)
    # wrap each ordered item in its own list
    # ol_ul_wrapped = re.sub(r'(\d+\.) (.*)', r'<ol><li>\g<2></li></ol>', ul_wrapped)

    # separate unordered and ordered lists
    separated = re.sub(r'</ul>\n(.*)<ol>', r'</ul>\n\n\g<1><ol>', corpus)
    separated = re.sub(r'</ol>\n(.*)<ul>', r'</ol>\n\n\g<1><ul>', separated)

    # remove back-to-back </ul><ul>
    ul_finished = re.sub(r'</ul>\n(.*)<ul>', '\n', separated)
    # remove back-to-back </ul><ul>
    ol_ul_finished = re.sub(r'</ol>\n(.*)<ol>', '\n', ul_finished)
    return ol_ul_finished


def italics(corpus):
    """
    >>> text = '*italic*'
    >>> italics(text)
    '<em>italic</em>'
    """
    return re.sub(r'\*([^\n]+)\*', r'<em>\g<1></em>', corpus)


def bold(corpus):
    """
    >>> text = '**bold**' / '__bold__'
    >>> bold(text)
    '<strong>bold</strong>'
    """
    underscore = re.sub(r'\_\_([^\n]+)\_\_', r'<strong>\g<1></strong>', corpus)
    return re.sub(r'\*\*([^\n]+)\*\*', r'<strong>\g<1></strong>', underscore)


def headers(corpus):
    """
    Places headers up to h6 into the corpus.
    """
    for i in range(3, 1, -1):
        corpus = re.sub(r'(^|\n)'+f'({"#"*i})'+'[ \t]+([^\n]+)',
                        fr'\g<1><h{i+1}>\g<3></h{i+1}>', corpus)
    return corpus

def quotes(text):
    pat = re.compile(r"""
            (
                ^(>[\s\t]?)    
                (.+\n (.+[\n])*)
                (?=\n)*      
            )   
            """, re.M | re.X)

    def rep(match):
        content = match.group(3)
        return "<{qtag}><{ptag}>{content}</{ptag}></{qtag}>".format(qtag='blockquote',content=content, ptag='p')

    return pat.sub(repl=rep, string=text)

def code(text):
    return re.sub(r'```([^\n]+)```', r'<code>\g<1></code>', text)

def html(corpus):
    """
    Converts raw Markdown into HTML.
    >>> text = 'P1\n\nP2\n- 1\n- 2\nP2\n\nP3'
    >>> html(text)
    '<p>P1</p>\n<p>P2\n<ul><li>1</li>\n<li>2</li></ul>\nP2</p>\n<p>P3</p>'
    >>> bolditalic = '***hello***'
    >>> html(bolditalic)
    '<p><strong><em>hello</em></strong></p>'
    """
    return paragraphs(quotes(lists(italics(bold(headers(inline_links(images(code(corpus))))))))).replace('<head>', '').replace('</head>', '')


def run():
    """
    Command line tool to convert Markdown file into HTML.
    """
    # import argparse
    # parser = argparse.ArgumentParser(description='Convert Markdown into HTML.')
    # parser.add_argument('FILE')
    # args = parser.parse_args()
    # with open(args.FILE, 'r') as file_obj:
    #     text = file_obj.read()
    text = """
    ``` FILE * test_file = fopen("/tmp/test.txt", "w+"); ```
    """
    markdown = text.rstrip('\n')
    print(html(markdown))


if __name__ == '__main__':
    import doctest
    run()
