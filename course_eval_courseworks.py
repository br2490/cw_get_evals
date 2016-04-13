# required:: lxml, requests, pdfkit (has dep: wkhtmltopdf)
import os
import sys
import getpass
import requests
from lxml import etree
import pdfkit


def get_job():
    user = input("Enter your UNI (you must be an admin): ")

    password = getpass.getpass(prompt='Password: ', stream=None)

    instructor_uni = input("Instructor UNI: ")

    get_evaluation(user, password, instructor_uni)


def get_evaluation(login_uni, password, instructors_uni):
    payload = {
        '_username': login_uni,
        '_password': password
    }
    # Configure our session
    webworker = requests.session()
    # Login to CourseWorks.
    webworker.post('https://courseworks.columbia.edu/direct/session.json?', data=payload)
    # Get our SESSION info.
    response = webworker.get('https://courseworks.columbia.edu/direct/session.json')
    if response.status_code != 200:
        print('Error: Received a non-200 response during login.')
        sys.exit(1)

    # Set reply to JSON and parse.
    reply_json = response.json()
    user_eid = reply_json['session_collection'][0]['userEid']
    if user_eid != login_uni:
        print('Error: Could not login as user ' + login_uni)
        sys.exit(1)

    print('Logged in as: ' + user_eid)

    eval_url = 'https://courseworks.columbia.edu/portal/tool/3b923cb5-ed21-4340-9273-67f4569a3c2d' \
               '/report_search_archive?startSearch=&instructor='

    url = ''.join([eval_url, instructors_uni])
    results = webworker.get(url)

    evaluations_xml = etree.HTML(results.text)

    # Get our evaluation xpaths - we need to know the data about the row and the URL to fetch the evaluation.
    evaluation_xpaths = evaluations_xml.xpath('//tr[contains(@class,"search-result-table-row")]/td//text() | '
                                              '//tr[contains(@class,"search-result-table-row")]/td//a/@href')

    # Now we need to parse our the unnecessary line return and tab characters.
    # and build a composite list that has each evaluation in its own list, within our master list.
    junk_values = '\n\t\t\t\t\t\t'
    filtered_list = [cell for cell in evaluation_xpaths if cell not in junk_values]
    master_eval_list = [filtered_list[x:x + 7] for x in range(0, len(filtered_list), 7)]

    # Make a directory to throw up in.
    try:
        os.stat(instructors_uni)
    except:
        os.mkdir(instructors_uni)
    print('Created a directory for these reports named: ' + instructors_uni)

    # We purposefully left some unnecessary characters in our master list which will help us set the course title
    # of courses with multiple evaluations. We need this so we know how to name the file!
    last_title = ''

    for evaluation_row in master_eval_list:
        if evaluation_row[0] != '\n\t\t\t\t\t\t\n\t\t\t\t\t':
            last_title = evaluation_row[0]
        else:
            evaluation_row[0] = last_title

    # Finally we kick our row to the fetcher and saver function for -this- evaluation row.
    fetch_and_save_evaluations(evaluation_row, webworker, instructors_uni)

    print('All reports have been saved.')


def fetch_and_save_evaluations(evaluation_row, webworker, instructors_uni):
    sep_char = '-'
    ext_char = '.pdf'
    instructor_eval = ''.join([sep_char, evaluation_row[4]]) if evaluation_row[4] != ' ' else ''
    filename = ''.join([evaluation_row[0], sep_char, evaluation_row[3], sep_char,
                        evaluation_row[2], instructor_eval, ext_char])
    fetch_url = evaluation_row[5]

    print('Getting evaluation: ' + filename)
    evaluation = webworker.get(fetch_url)
    if evaluation.status_code != 200:
        print('Error: Failed to fetch: ' + filename)
        return

    options = {
        'page-size': 'Letter',
        'margin-top': '0.25in',
        'margin-right': '0.25in',
        'margin-bottom': '0.25in',
        'margin-left': '0.25in',
        'encoding': "UTF-8",
        'quiet': ''
    }

    pdfkit.from_string(evaluation.text, instructors_uni + '/' + filename, options=options, css='eval.css')


if __name__ == "__main__":
    get_job()
else:
    print('Cannot be run non-interactively (yet)')
    sys.exit(1)
