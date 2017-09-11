import sso
from bs4 import BeautifulSoup
import getpass
import time
import string
import queue

printable = set(string.printable)
printable.remove('"')
printable.remove('\n')


user = input('SSO user: ')
pw = getpass.getpass('SSO password: ')

bug_file = 'bugs.txt'
headings = ['Bug ID',
            'Title',
            'Duplicate of',
            'Bug Severity',
            'Bug Status',
            'Product',
            'Bug Type',
            'DescriptionFormatted',
            'WorkaroundFormatted',
            'NotesFormatted',
            'Fixed-In Version',
            'Related Bugs',
            'Burt TitleInternal Only',
            'Burt Target ReleaseInternal Only',
            'Burt Patch ReleaseInternal Only',
            'Burt Fix ReleaseInternal Only',
            'Version Found(may exist in earlier versions)Internal Only',
            'Likely ExistsInternal Only']

s = sso.get_authenticated_session(user, pw)

with open(bug_file) as f:
    bug_list = f.read().splitlines()

with open("bug_report_" + time.strftime("%Y%m%d%H%M%S") + ".csv", mode="w") as f:
    print(','.join(headings), file=f)

    for bug in bug_list:
        bug_page = s.get('https://mysupport.netapp.com/NOW/cgi-bin/bol?Type=Detail&Display=' + bug.strip())
        soup = BeautifulSoup(bug_page.text, "html.parser")
        table1 = soup.find('table')
        table2 = table1.find('table')
        rows = table2.findAll('tr')
        bug = {}
        for tr in rows:
            child = tr.findAll(['th', 'td'])
            bug[child[0].text] = child[1].text
        output_string = ''
        for heading in headings:
            if heading in bug and bug[heading] and str(bug[heading]) != 'nan':
                output_string += '"' + ''.join(filter(lambda x: x in printable, str(bug[heading]))) + '",'
            else:
                output_string += ','
        print(output_string, file=f)
        print(output_string)
s.close()

temp = input('Please hit Enter to quit')