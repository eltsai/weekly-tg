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
title = ''


# def make():
#     ret = os.system( "cd resume&&GRAVATAR_OPTION=--no-gravatar make" )

def convert(file_name):
    """
    Convert markdown file to html
    """
    os.system('cd '+ html_dir + '&&' + 'pandoc ' + file_name +  ' -f markdown -t html -s -o ' + file_name + '.html && cd ..')

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
        #print(contents[-10:])
        f.close()
    except FileNotFoundError:
        print('File {} does not exist'.format(file_name))
        sys.exit(1)
    global title
    title = contents[0][2:-1]
    # Add telegram channel promt
    index = contents.index('微信搜索“**阮一峰的网络日志**”或者扫描二维码，即可订阅。\n')
    contents.insert(index+1, '\nTelegram频道[科技爱好者周刊](https://t.me/scitech_fans)同步更新，欢迎关注。\n')

    return html(''.join(contents[2:]).rstrip('\n'))




def generatePost(html_content):
    """
    Create telegraph page
    Using telegraph API: https://telegra.ph/api
    """
    telegraph = Telegraph()
    telegraph.create_account(short_name='E-Tasi')

    global title

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
