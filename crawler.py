import sys
import os
import requests
import json
import time
import random


def get_chapter(book_id: str):
    url = "https://read.douban.com/j/column_v2/" + book_id + "/chapters?all=1"
    respond = requests.get(url)

    # save respond
    with open('chapters.dat', 'w', encoding='utf-8') as f:
        f.write(respond.text)

    r_data = json.loads(respond.text)
    aids = []
    for chapter in r_data['list']:
        aids.append(chapter['id'])

    return aids


def get_article(aid: str):
    api = "https://read.douban.com/j/article_v2/get_reader_data"
    reader_data_version = "v15"
    response = requests.post(api, data={'aid': aid, 'reader_data_version': reader_data_version})
    r_data = json.loads(response.text)
    en_article = r_data['data']

    # # decrypt respond data
    # node = execjs.get("Node")
    # # Compile javascript
    # file = 'decrypt_article.js'
    # ctx = node.compile(open(file).read())
    # # error raise when en_article was passed overall
    # decrypted_data = ''
    # en_article = en_article[320:]
    # while len(en_article):
    #     res = ctx.eval(f'decrypt_data("{en_article[:80]}", "{aid}")')
    #     res = res.encode('GBK').decode('utf-8')
    #     decrypted_data += res
    #     print(res)
    #     en_article = en_article[80:]
    #
    # return decrypted_data

    return en_article


def analyse_article(file_name: str):
    with open('de_articles.dat', 'r', encoding='utf-8') as fin:
        log = ''
        text_type = set([])
        content_type = set([])
        for line in fin.readlines():
            a_data = json.loads(line)
            if len(a_data['posts']) > 1:
                print('error')
            title = a_data['posts'][0]['title']
            chapter = a_data['posts'][0]['contents']
            log += f'\n{title}\n\n'
            for se in chapter:
                content_type.add(se['type'])
                if 'text' in se['data']:
                    text_segments = se['data']['text']
                    for ts in text_segments:
                        text_type.add(ts['kind'])
                else:
                    log += '(非文字段落)\n\n'

    print(content_type)
    print(text_type)
    with open(file_name, 'w', encoding='utf-8') as fout:
        fout.write(log)


class ArticleComposerTXT(object):
    def __init__(self, data_file):
        self.data_file = data_file

    def parse_text(self, text: dict) -> str:
        if text['kind'] == 'plaintext':
            return text['content']
        elif text['kind'] == 'link':
            return text['url']
        elif text['kind'] == 'regular_script':
            re_str = ''
            for content in text['content']:
                re_str += self.parse_text(content)
            return f'「{re_str}」'
        elif text['kind'] == 'emphasize':
            re_str = ''
            for content in text['content']:
                re_str += self.parse_text(content)
            return f'[{re_str}]'
        elif text['kind'] == 'footnote':
            return ' ({})'.format(text['content'])

    def parse_segment(self, segment: dict) -> str:
        if segment['type'] == 'paragraph':
            re_str = ''
            for text in segment['data']['text']:
                re_str += self.parse_text(text)
            return re_str
        elif segment['type'] == 'headline':
            re_str = ''
            for text in segment['data']['text']:
                re_str += self.parse_text(text)
            return re_str
        elif segment['type'] == 'illus':
            pic_url = segment['data']['size']['orig']['src']
            legend = segment['data']['legend']
            return '![{}]({})'.format(legend, pic_url)

    def compose(self):
        book = ''
        for line in self.data_file.readlines():
            a_data = json.loads(line)
            for post in a_data['posts']:
                title = post['title']
                chapter = post['contents']
                book += f'\n\n{title}\n\n'
                for se in chapter:
                    se_str = self.parse_segment(se)
                    if len(se_str):
                        book += se_str + '\n\n'
        return book


class ArticleComposerMD(object):
    def __init__(self, data_file, path):
        self.data_file = data_file
        self.path = path

    def parse_text(self, text: dict) -> str:
        if text['kind'] == 'plaintext':
            return text['content']
        elif text['kind'] == 'link':
            content_str = ''
            for content in text['content']:
                content_str += self.parse_text(content)
            return '[{0}]({1})'.format(content_str, text['url'])
        elif text['kind'] == 'regular_script':
            re_str = ''
            for content in text['content']:
                re_str += self.parse_text(content)
            return f'「{re_str}」'
        elif text['kind'] == 'emphasize':
            re_str = ''
            for content in text['content']:
                re_str += self.parse_text(content)
            return f'**{re_str}**'
        elif text['kind'] == 'footnote':
            return ' ({})'.format(text['content'])

    def parse_segment(self, segment: dict) -> str:
        if segment['type'] == 'paragraph':
            re_str = ''
            for text in segment['data']['text']:
                re_str += self.parse_text(text)
            return re_str
        elif segment['type'] == 'headline':
            re_str = ''
            for text in segment['data']['text']:
                re_str += self.parse_text(text)
            return re_str
        elif segment['type'] == 'illus':
            # pic_url = segment['data']['size']['orig']['src']
            # legend = segment['data']['legend']
            # pic_name = download_pic(self.path + '/pic', pic_url)
            # return '![]({1})  \n[{0}]'.format(legend, './pic/' + pic_name)
            pic_url = segment['data']['size']['orig']['src']
            legend = segment['data']['legend']
            return '![]({1})  \n[{0}]'.format(legend, pic_url)

    def compose(self):
        book = '# 十恶胡作 - 暴力仓鼠  \n\n[TOC]'   # [TOC] indicates where to put table of content
        for line in self.data_file.readlines():
            a_data = json.loads(line)
            for post in a_data['posts']:
                title = post['title'].strip()   # remove spaces and control characters
                chapter = post['contents']
                book += f'\n\n## {title}\n\n'
                for se in chapter:
                    se_str = self.parse_segment(se)
                    if len(se_str):
                        book += se_str + '\n\n'
        return book


def download_pic(path, url):
    if not os.path.exists(path):
        os.makedirs(path)
    # get file_name from url
    file_name = url.split('/')[-1]
    if path[-1] != '/':
        path += '/' + file_name
    else:
        path += file_name
    # request pic and save
    respond = requests.get(url)
    with open(path, 'wb') as f:
        f.write(respond.content)
    return file_name


def compose_article_txt(file_name: str):
    path = './out/'
    if not os.path.exists(path):
        os.makedirs(path)
		
    with open('out/de_articles.dat', 'r', encoding='utf-8') as f_in:
        ac = ArticleComposerTXT(f_in)
        book = ac.compose()

    with open(path + '/' + file_name, 'w', encoding='utf-8') as f_out:
        f_out.write(book)


def compose_article_md(file_name: str):
    path = './out/' + file_name[:file_name.rindex('.')]
    if not os.path.exists(path):
        os.makedirs(path)

    with open('out/de_articles.dat', 'r', encoding='utf-8') as f_in:
        ac = ArticleComposerMD(f_in, path)
        book = ac.compose()

    with open(path + '/' + file_name, 'w', encoding='utf-8') as f_out:
        f_out.write(book)


def main():
    if len(sys.argv) == 2:
        book_id = sys.argv[1]
    else:
        print('argv error.')
        return

    aids = get_chapter(book_id)

    with open('out/en_articles.dat', 'w', encoding='utf-8') as f:
        count = 0
        for aid in aids:
            data = get_article(aid)
            f.write(json.dumps({'aid': aid, 'data': data}) + '\n')
            print(f'{count:3}: {aid} succeeded.')
            count += 1
            # time.sleep(random.gauss(1*60, 0.1))


if __name__ == '__main__':
    # analyse_article('log.txt')
    # compose_article_txt('十恶胡作 - 暴力仓鼠.txt')
    # compose_article_md('十恶胡作 - 暴力仓鼠.md')
    main()
