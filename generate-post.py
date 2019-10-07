
#!/usr/bin/python
#author='E-Tsai'

"""
This script converts post from ruanyf/weekly
To telegraph channel: https://t.me/scitech_fans
"""

from telegraph import Telegraph
import subprocess
import argparse
import sys
import os

post_dir    = './weekly/docs/' 
html_dir    = './tmp/'

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
    rtype: str (title)
    """
    try:
        f = open(post_dir + file_name, 'r')
        contents = f.readlines()
        #print(contents[-10:])
        f.close()
    except FileNotFoundError:
        print('File {} does not exist'.format(file_name), file=sys.stderr)
        sys.exit(1)
        
    title = contents[0][2:-1]
    index = contents.index('微信搜索“__阮一峰的网络日志__”或者扫描二维码，即可订阅。\n')
    contents.insert(index+1, '\nTelegram频道[科技爱好者周刊](https://t.me/scitech_fans)同步更新，欢迎关注。\n')


    with open(html_dir + file_name, 'w') as nf:
        nf.write(''.join(contents[2:]))
    nf.close()

    convert(file_name)

    return title




def generatePost(title, file_name):
    telegraph = Telegraph()

    telegraph.create_account(short_name='E-Tasi')


    with open(html_dir + file_name + '.html', 'r') as gf:
        html = gf.readlines()
    gf.close()

    cut = ''.join(html[10:-2])
    fixed = cut.replace('<div', '<p').\
                replace('</div', '</p').\
                replace('<h2', '<h3').\
                replace('</h2', '</h3').\
                replace('<span', '<p').\
                replace('</span', '</p')
                # replace('<blockquote>', '').\
                # replace('</blockquote>', '')

    # with open(html_dir + file_name + 'n.html', 'w') as nf:
    #     nf.write(fixed)
    # nf.close()

    response = telegraph.create_page(
        title = title,
        author_name ='ruanyf ( 阮一峰 ) 著 E-Tsai 搬运',
        html_content = fixed
    )
    print('https://telegra.ph/{}'.format(response['path']))

def main():
    parser = argparse.ArgumentParser(description='Range of markdown file index')
    parser.add_argument("start", action="store", type=int, help="starting index of markdown file")
    parser.add_argument("end", action="store", type=int, help="ending index of markdown file")
    args = parser.parse_args()

    start = args.start
    end = args.end + 1

    for i in range(start, end):
        file_name = 'issue-'+str(i)+'.md'
        
        generatePost(convertMD(file_name), file_name)

    return 0
    

if __name__ == '__main__':
    exit(main())
