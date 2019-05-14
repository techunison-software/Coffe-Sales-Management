import sqlalchemy as sql

def getConnection():
    user_name="application"
    pwd="abc123!@#"
    host="192.168.1.128:3307"
    database="coffee_sales"
    return sql.create_engine('mysql://'+user_name+':'+pwd+'@'+host+'/'+database)