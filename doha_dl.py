from bs4 import BeautifulSoup
from urllib.request import urlopen
from dateutil import parser
from datetime import date


class Case:
    def __init__(self, case):
        self.case_number = self.set_case_number(case)
        self.guidelines = self.set_guidelines(case)
        self.date = self.set_date(case)
        self.text = self.set_text(case)
        self.link = self.set_case_link(case)

    @staticmethod
    def set_case_number(case) -> str:
        case_div = case.find('div', attrs={'class': 'casenum'})
        case_text = case_div.find('a').text
        return case_text.split('Case Number: ')[-1]

    @staticmethod
    def set_guidelines(case) -> list():
        case_guidelines = case.find('div', attrs={'class': 'keywords'}).text
        return [gl.replace(' ', '').replace('Guideline', '') for gl in case_guidelines.split(';')]

    @staticmethod
    def set_date(case) -> date:
        case_date = case.find('p', attrs={'class': 'date'}).text
        try:
            return parser.parse(case_date)
        except:
            print(case_date)

    @staticmethod
    def set_text(case) -> str:
        return case.find('p', attrs={'class': 'digest'}).text

    @staticmethod
    def set_case_link(case) -> str:
        return '{0}{1}'.format('http://ogc.osd.mil', case.find('a').get('href'))


case_list = list()
for year in range(1996, 2017 + 1, 1):
    html = urlopen("http://ogc.osd.mil/doha/industrial/{0}.html".format(year))
    soup = BeautifulSoup(html, "html5lib")
    for c in soup.findAll('div', attrs={'class': 'case'}):
        case_list.append(Case(c))


for c in case_list:
    print('Case Number:', c.case_number, '\n',
          'Guideline(s)', c.guidelines, '\n',
          'Date:', c.date, '\n',
          # 'Text:', c.text, '\n',
          'Link:', c.link)










