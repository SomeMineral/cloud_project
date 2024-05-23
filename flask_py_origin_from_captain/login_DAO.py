import pymysql
import db_data

# 로그인 시 DB 확인
def selectUserById(userId) :  

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure()
    sql_select = 'SELECT * FROM users WHERE user_id = %s'
        
    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor()
        cursor_aws.execute(sql_select, userId)
        result1 = cursor_aws.fetchone()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor()
        cursor_azure.execute(sql_select, userId)
        result2 = cursor_azure.fetchone()
        cursor_azure.close()
        con_azure.close()

    else:
        pass

    return result1 if con_aws is not None else result2
