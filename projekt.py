import requests
import re
import os
import csv
import orodja


def save_sites():
    server = 'https://www.imo-official.org/year_individual_r.aspx'
    parameters = 'year'
    for year in range(2007, 2017):
        url = '{}?{}={}'.format(server, parameters, year)
        name ='podatki/{}'.format(year)
        orodja.shrani(url, name)

save_sites()

def get_cvs():
    regex_competitors = re.compile(r'<tr.*?><td><a href="participant_r\.aspx\?id=(?P<id>\d+?)">(?P<Name>.*?)</a>.*?'
                                   r'href="country_individual_r\.aspx\?code=(?P<Short_country_name>.*?)">(?P<Full_country_name>.*?)</a>.*?'
                                   r'align="center">(?P<P1>.*?)</td><td align="center">(?P<P2>.*?)</td><td align="center">(?P<P3>.*?)</td>'
                                   r'<td align="center">(?P<P4>.*?)</td><td align="center">(?P<P5>.*?)</td><td align="center">(?P<P6>.*?)</td>'
                                   r'<td align="right">(?P<Points>.*?)</td><td align="right">(?P<Rank>.*?)</td><td>(?P<Achievement>.*?)</td></tr>'
                                   ,
                                   flags=re.DOTALL
                                   )
    matchings = []

    for year in orodja.datoteke('podatki'):
        for cats in re.finditer(regex_competitors, orodja.vsebina_datoteke(year)):
            cat = cats.groupdict()
            cat['id'] = int(cat['id'])
            for i in range(1, 7):
                name = 'P{}'.format(i)
                cat[name] = int(cat[name])
            cat['Points'] = int(cat['Points'])
            cat['Rank'] = int(cat['Rank'])
            cat['Year'] = int(os.path.split(year)[1])
            matchings.append(cat)
    orodja.zapisi_tabelo(matchings, ['id', 'Name', 'Short_country_name', 'Full_country_name', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'Points', 'Rank','Year', 'Achievement'], 'data.csv')

get_cvs()





