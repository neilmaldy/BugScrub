import sso
from bs4 import BeautifulSoup
import getpass
import time
import string
import sys
import os
import queue

printable = set(string.printable)
printable.remove('"')
printable.remove('\n')

print("Get Bugs v2")

bug_file = 'bugs.txt'
if os.path.exists(bug_file):
    print("\nFound burt id list in bugs.txt")
else:
    temp = input("\nPlease create bugs.txt with one burt id per line and try again")
    sys.exit('\nPlease create bugs.txt with one burt id per line and try again')


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
s = None
fail_count = 0

while s is None:
    user = input('\nSSO user: ')
    pw = getpass.getpass('SSO password: ')
    s = sso.get_authenticated_session(user, pw)
    if s is None:
        fail_count += 1
        if fail_count > 2:
            sys.exit("\nSorry, too many login failures")
        else:
            print("Login failed, please try again")


with open(bug_file) as f:
    bug_list = f.read().splitlines()

output_filename = "bug_report_" + time.strftime("%Y%m%d%H%M%S") + ".csv"

with open(output_filename, mode="w") as f:
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
        print(' '.join([output_string.split(',')[0], output_string.split(',')[1]]))
s.close()

temp = input('\nReport complete\n\nOutput written to ' + output_filename + '\n\nPlease hit Enter to exit')