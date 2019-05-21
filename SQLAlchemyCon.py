import sqlalchemy as sql

def getConnection():
    user_name="application"
    pwd="abc123!@#"
    host="1.22.137.204:3307"
    database="coffee"
    return sql.create_engine('mysql://'+user_name+':'+pwd+'@'+host+'/'+database)