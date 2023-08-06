#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, json, sys
from datetime import datetime
from bs4 import BeautifulSoup as bs

class tucao:
    api = 'http://daily.zhihu.com/api/1.2/news/before/{0}'

    def __init__(self, date):
        self.transfer(date)

    def transfer(self, date):
        if date == '':
            date = int(datetime.now().strftime("%Y%m%d")) + 1
        else:
            if int(date) > int(datetime.now().strftime("%Y%m%d")):
                raise Exception("Invalid Date!")
        self.api = self.api.format(date)
        self.parse()

    def parse(self):
        try:
            res = urllib.urlopen(self.api)
            data = json.loads(res.read())
            tucao_url = data['news'][-1]['url']
        except:
            raise Exception("Invalid Date!")

        res2 = urllib.urlopen(tucao_url)
        data2 = json.loads(res2.read())
        content = data2['body']

        soup = bs(content,'lxml')
        questions = soup.findAll('div',{'class':'question'})

        for i, question in enumerate(questions):
            print('===============================================================\n')
            title = question.find('h2').get_text()
            print 'Q{0}: '. format(i+1) + title.encode('utf-8').strip()

            authors = question.findAll('div',{'class':'meta'})
            answers = question.findAll('div',{'class':'content'})
            for author, answer in zip(authors, answers):
                print('\n---------------------------------------------------------------\n')
                print '作者: ' + author.get_text().encode('utf-8').strip()
                print('\n---------------------------------------------------------------\n')
                print answer.get_text().encode('utf-8').strip()
                pics = answer.findAll('img')
                if len(pics) > 0:
                    for pic in pics:
                        print pic['src']
            print '\n\n\n'


def main():
    try :
        argv = sys.argv[1:]
        if len(argv) > 1:
            print 'ERROR'
        elif len(argv) == 0:
            tucao('')
        elif int(argv[0]) and len(argv[0]) == 8:
            tucao(argv[0])
        else:
            raise ValueError
    except ValueError:
        print '格式错误!'
    except Exception:
        print '日期错误'


if __name__ == '__main__':
    main()
