#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author='E-Tsai'

"""
This script converts post from ruanyf/weekly
To telegraph channel: https://t.me/scitech_fans
"""

from telegraph import Telegraph
from colorama import Fore, Style
import subprocess
import argparse
import sys
import os

from md2html import * 

post_dir    = './weekly/docs/' 
html_dir    = './tmp/'


# def make():
#     ret = os.system( "cd resume&&GRAVATAR_OPTION=--no-gravatar make" )

def save(content, file_name):
    """
    Convert markdown file to html
    """
    os.system('mkdir -p ' + html_dir)
    try:
        f = open(file_name, 'w')
        f.write(content)
        f.close()
    except FileNotFoundError:
        print('Cant open file {}'.format(file_name))
        sys.exit(1)

def convertMD(file_name):
    """
    Read markdown file from git submodule dir: weekly/docs
    Extract title from post, add tg channel link to the end of the post
    Convert content from md to html
    type: str (filename)
    rtype: str (title), str (html content)
    """
    try:
        f = open(post_dir + file_name, 'r')
        contents = f.readlines()
        f.close()
    except FileNotFoundError:
        print('File {} does not exist'.format(file_name))
        sys.exit(1)
    title = contents[0][2:-1]
    # Add telegram channel promt
    index = contents.index('微信搜索“阮一峰的网络日志”或者扫描二维码，即可订阅。\n')
    contents.insert(index+1, '\nTelegram频道[科技爱好者周刊](https://t.me/scitech_fans)同步更新，欢迎关注。\n')

    generated_html = html(''.join(contents[2:]).rstrip('\n'))
    
    save(generated_html, html_dir + file_name)
    return (generated_html, title)




def generatePost(content_tuple):
    """
    Create telegraph page
    Using telegraph API: https://telegra.ph/api
    """
    telegraph = Telegraph()
    telegraph.create_account(short_name='E-Tasi')

    html_content = content_tuple[0]
    title = content_tuple[1]

    response = telegraph.create_page(
        title = title,
        author_name ='ruanyf ( 阮一峰 ) 著 E-Tsai 搬运',
        html_content = html_content
    )

    url = 'https://telegra.ph/{}'.format(response['path'])
    print(Fore.GREEN + url + Fore.WHITE)
    # os.system('google-chrome '+ url)

def main():
    """
    Read starting and ending index from args
    Convert post and generate telegraph page 
    """
    parser = argparse.ArgumentParser(description='Range of markdown file index')
    parser.add_argument("start", action="store", type=int, help="starting index of markdown file")
    parser.add_argument("end", action="store", type=int, help="ending index of markdown file")
    args = parser.parse_args()

    start = args.start
    end = args.end + 1

    for i in range(start, end):
        file_name = 'issue-'+str(i)+'.md'
        generatePost(convertMD(file_name))

    return 0
    

if __name__ == '__main__':
    exit(main())
