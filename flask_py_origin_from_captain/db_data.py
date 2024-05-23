import pymysql

# DB 연결 - AWS
def db_connect() :
    try:
        db = pymysql.connect(
            user = 'root',
            password = 'admin12345',
            host = 'db-svc',
            db = 'ssgpang',
            charset = 'utf8',
            autocommit = True
        )
    except Exception as e:
        db = None
    finally:
        return db
# 연결 실패한 경우 return 으로 None

# DB 연결 - Azure
def db_connect_azure() :
    try:
        db = pymysql.connect(
            user = 'azureroot',
            password = 'admin12345!!',
            host = '10.1.2.101',
            db = 'ssgpang',
            charset = 'utf8',
            autocommit = True
        )
    except Exception as e:
        db = None
    finally:
        return db
# 연결 실패한 경우 return 으로 None


def active_aws():
    con_aws = db_connect()
    if con_aws is not None:
        con_aws.close()
        return True
    else:
        con_aws.close()
        return False

def active_azure():
    con_azure = db_connect_azure()
    if con_azure is not None:
        con_azure.close()
        return True
    else:
        con_azure.close()
        return False