# required:: lxml, requests, pdfkit (has dep: wkhtmltopdf)


def get_evaluation(login_uni, password, instructors_uni):
    import requests
    import pdfkit
    from lxml import etree

    payload = {
        '_username': login_uni,
        '_password': password
    }

    c = requests.session()
    c.post('https://courseworks.columbia.edu/direct/session.json?', data=payload)
    response = c.get('https://courseworks.columbia.edu/direct/session.json')
    print(response.status_code)
    reply_json = response.json()
    user_eid = reply_json['session_collection'][0]['userEid']
    # LOGIC FOR SIGN IN...
    # if response.status_code == 200 && user_eid is not NULL...
    print('Logged in as: ' + user_eid)

    eval_url = 'https://courseworks.columbia.edu/portal/tool/3b923cb5-ed21-4340-9273-67f4569a3c2d' \
               '/report_search_archive?startSearch=&instructor='
    
    url = ''.join([eval_url, instructors_uni])
    results = c.get(url)

    evaluations_xml = etree.HTML(results.text)

    # Get our evaluation xpaths - we need to know the data about the row and the URL to fetch the evaluation.
    evaluation_xpaths = evaluations_xml.xpath('//tr[contains(@class,"search-result-table-row")]/td//text() | '
                                              '//tr[contains(@class,"search-result-table-row")]/td//a/@href')

    # Now we need to parse our the unnecessary line return and tab characters.
    # and build a composite list that has each evaluation in its own list, within our master list.
    junk_values = '\n\t\t\t\t\t\t'
    filtered_list = [cell for cell in evaluation_xpaths if cell not in junk_values]
    master_eval_list = [filtered_list[x:x + 7] for x in range(0, len(filtered_list), 7)]

    # We purposefully left some unnecessary characters in our master list which will help us set the course title
    # of courses with multiple evaluations. We need this so we know how to name the file!
    last_title = ''
    for evaluation_row in master_eval_list:
        if evaluation_row[0] != '\n\t\t\t\t\t\t\n\t\t\t\t\t':
            last_title = evaluation_row[0]
        else:
            evaluation_row[0] = last_title

        # Finally we kick our row to the fetcher and saver function for -this- evaluation row.
        fetch_and_save_evaluations(evaluation_row, c)
    print('All done...')


def fetch_and_save_evaluations(evaluation_row, c):
    sep_char = '-'
    instructor_eval = ''.join([sep_char, evaluation_row[4]]) if evaluation_row[4] != ' ' else ''
    filename = ''.join([evaluation_row[0], sep_char, evaluation_row[3], sep_char, evaluation_row[2], instructor_eval])
    fetch_url = evaluation_row[5]
    evaluation = c.get(fetch_url)

    print(filename)
    print(evaluation)

