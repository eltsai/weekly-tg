# weekly-tg

*自动生成[科技爱好者周刊](https://github.com/ruanyf/weekly) [telegram channel](https://t.me/scitech_fans)推送*， see [issue #885](https://github.com/ruanyf/weekly/issues/885).

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) (注：这个Licence继承自[这个仓库](https://github.com/linheimx/Husky)，只针对代码内容，不针对weekly博文)。

## 依赖

* [telegraph](https://telegra.ph/api)
* [colorama](https://github.com/tartley/colorama)

安装依赖:

```shell
pip/pip3 install -r requirements.txt
```

如果想尝试替换markdown => html 模块，可以安装:

```shell
# optional: pandoc - markdown => html
apt-get install pandoc

# optional: python markdown module
apt-get install python3-markdown
```

下载博客文本内容:

```shell
git pull --recurse-submodules
```

## 功能

- [x] 文本处理：将博文成批转处理，获得标题+修改过后的内容(在末尾加上tg channel promt).
- [x] 文本转换：将markdown格式转换成html ([issue1](#问题))，以适应[telegraph api](https://telegra.ph/api).
- [ ] 使用telegram bot自动推送

## 使用说明

```shell
├── generate-post.py	# python script to generate posts in batch
├── md2html.py			# convert md to html, following principles of tg API
├── LICENSE
├── README.md
├── requirements.txt
├── run.sh				# run python script with proxychains: needed under GFW
├── TODO
├── venv
└── weekly				# original posts
```

使用:

```shell
python generate-post.py [starting-index] [ending-index]
```

来成批生成telegraph博文。

使用: 

```shell
./run.sh [starting-index] [ending-index]
```

使用proxychains运行此python脚本。

## 合作

这个仓库的代码的目的是让tg channel管理员能够相对轻松地搬运博文，但是它也可以成为从markdown源文件部署tg channel推送的一个项目。非常欢迎有意贡献代码的小伙伴们参与！

## 问题


### 1. Markdown => html

我尝试了[这个仓库](https://github.com/mwhite/resume) (即[pandoc](https://pandoc.org/getting-started.html)) 和[python模块markdown](https://www.drupal.org/project/markdown) ([命令行](http://tuxdiary.com/2016/06/30/markdown-to-html-terminal/))，但是它们对引用的处理都有问题，左侧没有横杠出现/横岗出现得一点都不美观，缩进也有点问题，我觉得这个小问题 ~~可以忍受~~ 有点不能忍受。可能我们需要寄希望于[typora](https://github.com/typora)开发出[高级命令行功能](https://github.com/typora/typora-issues/issues/1999)了。

我决定尝试一下使用re模块，就像[这个repo](https://github.com/linheimx/Husky)一样。
