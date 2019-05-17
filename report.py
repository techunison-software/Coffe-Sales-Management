import pandas as pd
import os
import mysql.connector
import MySQLdb
import sqlalchemy as sql
import SQLAlchemyCon as conn
from sqlalchemy import create_engine
from reportlab.lib import styles
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from xlsxwriter.workbook import Workbook
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer,Table, TableStyle
engine = None
user_name="application"
pwd="abc123!@#"
host="192.168.1.128:3307"
database="coffee"
sql_engine = conn.getConnection()
engine = create_engine('mysql://'+user_name+':'+pwd+'@'+host+'/'+database)


pdfname = 'mydoc.pdf'
doc = SimpleDocTemplate(
        pdfname
    )
style = ParagraphStyle(
        name='Normal',
        fontSize=8,
    )
story = []   
result1 = engine.execute('select * from users')

sampleData = result1.fetchall()
print(sampleData) 
query = 'select * from users'
result=pd.read_sql_query(query, sql_engine) 
results.to_csv("output.csv", index=False)
#sample1 = result1.fetchall()
print(result)
for row in result:
    story.append(Paragraph(row, style))
    print('row',row)


doc.build(
    story
)
workbook = Workbook('outfile.xlsx')
sheet = workbook.add_worksheet()
for r, row in enumerate(result):
    for c, col in enumerate(row):
        sheet.write(r, c, col)       




