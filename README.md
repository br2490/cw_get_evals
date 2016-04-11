# Get CourseWorks Evaluation from CourseArchives
A script that will grab archived CourseWorks evaluation reports and save them as PDFs

Requirements
--
Python 3.x

Modules: lxml, requests, pdfkit

`pip install <module name>` should work for each required module.

PDFKit requires [wkhtmltopdf](http://wkhtmltopdf.org/) which has downloads available for Windows, Mac, and Linux.


What's it do?
--
This will grab an instructors evaluatiosn from the CourseArchives which are not available except for superusers.


How to use cw_get_evals
--
Enter: 
 `python3 course_eval_courseworks.py`
 at the command line. The script will guide you through.
