## required:: pip install lxml and pip install requests.

import sys

def get_evaluation(UNI, password, instructorUNI):
    import requests
    from lxml import html

    payload = {
        '_username': UNI,
        '_password': password
        }

    c = requests.session()
    c.post('https://courseworks.columbia.edu/direct/session.json?', data=payload)
    response = c.get('https://courseworks.columbia.edu/direct/session.json')
    print(response.status_code)
    reply_json = response.json()
    userID = reply_json['session_collection'][0]['userEid']
    ## LOGIC FOR SIGN IN...
    ## if response.status_code == 200 && userID is not NULL...
    print('Logged in as: ' + userID)

    url = 'https://courseworks.columbia.edu/portal/tool/3b923cb5-ed21-4340-9273-67f4569a3c2d/report_search_archive?startSearch=&instructor=ob2178'

    results = c.get(url)
    tree = html.fromstring(results.content)
    all_reports = tree.xpath('//tr[@class="search-result-table-row"]//td//text()')
    for element in all_reports:
        print(element.rstrip('\n').rstrip('\r'))
    ## print(results.text)

    ## /html/body/div/div[4]/form/table/tbody
    ## /html/body/div/div[4]/form/table/tbody/tr[1]




    ## https://courseworks.columbia.edu/portal/tool/3b923cb5-ed21-4340-9273-67f4569a3c2d/report_search_archive?mergeReports=false&showSettingsDetail=false&canSelectGroups=true&returnTo=0&external=false&settingsByEvaluation=true&directView=false&command+link+parameters%26Submitting%2520control%3Dsearch-archive-button=Search+Reports+from+Old+CourseWorks
    ## https://courseworks.columbia.edu/portal/tool/3b923cb5-ed21-4340-9273-67f4569a3c2d/report_search_archive?mergeReports=false&startSearch=&canSelectGroups=true&instructor=ob2178&external=false&settingsByEvaluation=true&courseId=&schoolCode=&type=&showSettingsDetail=false&assistant=&returnTo=0&term=&directView=false&year=&departmentCode=&evaluationTitle=&sakai.tool.placement.id=3b923cb5-ed21-4340-9273-67f4569a3c2d
    ## https://courseworks.columbia.edu/portal/tool/3b923cb5-ed21-4340-9273-67f4569a3c2d/report_search_archive?mergeReports=false&startSearch=&canSelectGroups=true&instructor=ob2178&returnTo=0
    ## https://courseworks.columbia.edu/portal/tool/3b923cb5-ed21-4340-9273-67f4569a3c2d/report_search_archive?startSearch=&instructor=ob2178
