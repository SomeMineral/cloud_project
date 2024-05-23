import pymysql
import db_data

# 회원정보 수정
def updateUserById(userId, userPw, userName, userEmail, userPhone, userAddress) :
    
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_update = 'UPDATE users SET user_pw = %s, user_name = %s, user_email = %s, user_phone = %s, user_address = %s WHERE user_id = %s'

    # 먼저 선언
    result_num1 = None
    result_num2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        result_num1 = cursor_aws.execute(sql_update, (userPw, userName, userEmail, userPhone, userAddress, userId))
        cursor_aws.close()
        con_aws.close()

    if con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        result_num2 = cursor_azure.execute(sql_update, (userPw, userName, userEmail, userPhone, userAddress, userId))
        cursor_azure.close()
        con_azure.close()

    return result_num1 if con_aws is not None else result_num2    

# 회원가입 시 ID 중복확인
def checkUserId(userId) :
    
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_select = 'SELECT user_id FROM users WHERE user_id = %s'

    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_aws.execute(sql_select, userId)
        result1 = cursor_aws.fetchone()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_azure.execute(sql_select, userId)
        result2 = cursor_azure.fetchone()
        cursor_azure.close()
        con_azure.close()

    else:
        pass

    return result1 if con_aws is not None else result2


# 회원가입 시 E-mail 중복확인
def checkUserEmail(userEmail) :
    
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_select = 'SELECT user_email FROM users WHERE user_email = %s'

    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_aws.execute(sql_select, userEmail)
        result1 = cursor_aws.fetchone()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_azure.execute(sql_select, userEmail)
        result2 = cursor_azure.fetchone()
        cursor_azure.close()
        con_azure.close()

    else:
        pass

    return result1 if con_aws is not None else result2


# 회원가입 시 PhoneNumber 중복확인
def checkUserPhoneNumber(userPhone) :
    
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_select = 'SELECT user_phone FROM users WHERE user_phone = %s'

    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_aws.execute(sql_select, userPhone)
        result1 = cursor_aws.fetchone()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_azure.execute(sql_select, userPhone)
        result2 = cursor_azure.fetchone()
        cursor_azure.close()
        con_azure.close()

    else:
        pass

    return result1 if con_aws is not None else result2

# 회원가입
def insertUser(userId, userPw, userName, userEmail, userPhone, userAddress) :

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure()
    sql_insert = 'INSERT INTO users (user_id, user_pw, user_name, user_email, user_phone, user_address) VALUES (%s, %s, %s, %s, %s, %s)'
      
    # 먼저 선언
    result_num1 = None
    result_num2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor()
        result_num1 = cursor_aws.execute(sql_insert, (userId, userPw, userName, userEmail, userPhone, userAddress))

        cursor_aws.close()
        con_aws.close()

    if con_azure is not None:
        cursor_azure = con_azure.cursor()
        result_num2 = cursor_azure.execute(sql_insert, (userId, userPw, userName, userEmail, userPhone, userAddress))

        cursor_azure.close()
        con_azure.close()

    return result_num1 if con_aws is not None else result_num2

# 상품 등록 페이지 SELECT
def selectProductAll():
        
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure()
    sql_select = "SELECT * FROM product ORDER BY product_date DESC"

    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_aws.execute(sql_select)
        result1 = cursor_aws.fetchall()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_azure.execute(sql_select)
        result2 = cursor_azure.fetchall()
        cursor_azure.close()
        con_azure.close()
    
    else:
        pass

    return result1 if con_aws is not None else result2   

# 상품 장바구니에 담기
def insertCartList(cartUserId, cartProductCode):
        
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure()
    sql_select = 'SELECT product_count FROM cart WHERE user_id = %s AND product_code = %s'

    # 먼저 선언
    result_num1 = None
    result_num2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_aws.execute(sql_select, (cartUserId, cartProductCode))
        existing_product = cursor_aws.fetchone()

        # 이미 장바구니에 있는 경우
        if existing_product:
            # 상품 수량 증가
            new_count = existing_product[0] + 1
            sql_update = 'UPDATE cart SET product_count = %s WHERE user_id = %s AND product_code = %s'
            cursor_aws.execute(sql_update, (new_count, cartUserId, cartProductCode))
            result_num1 = new_count

        # 장바구니에 없는 경우
        else:  
            # 장바구니에 새 상품 추가
            sql_insert = 'INSERT INTO cart (user_id, product_code, product_count) VALUES (%s, %s, 1)'
            cursor_aws.execute(sql_insert, (cartUserId, cartProductCode))
            result_num1 = 1

        con_aws.commit()
        cursor_aws.close()
        con_aws.close()

    if con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_azure.execute(sql_select, (cartUserId, cartProductCode))
        existing_product = cursor_azure.fetchone()
            
        # 이미 장바구니에 있는 경우
        if existing_product:
            # 상품 수량 증가
            new_count = existing_product[0] + 1
            sql_update = 'UPDATE cart SET product_count = %s WHERE user_id = %s AND product_code = %s'
            cursor_azure.execute(sql_update, (new_count, cartUserId, cartProductCode))
            result_num2 = new_count

        # 장바구니에 없는 경우
        else:  
            # 장바구니에 새 상품 추가
            sql_insert = 'INSERT INTO cart (user_id, product_code, product_count) VALUES (%s, %s, 1)'
            cursor_azure.execute(sql_insert, (cartUserId, cartProductCode))
            result_num2 = 1

        con_azure.commit()
        cursor_azure.close()
        con_azure.close()
    
    else:
        pass

    return result_num1 if con_aws is not None else result_num2

# 장바구니(Cart) 정보 SELECT
def selectCartListByUserId(userId):
    
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_select = """
        SELECT cart.*, product.*
        FROM cart
        INNER JOIN product ON cart.product_code = product.product_code
        WHERE cart.user_id = %s
        """

    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_aws.execute(sql_select, (userId))
        result1 = cursor_aws.fetchall()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_azure.execute(sql_select, (userId))
        result2 = cursor_azure.fetchall()
        cursor_azure.close()
        con_azure.close()

    else:
        pass

    return result1 if con_aws is not None else result2    

# 장바구니(Cart) 삭제
def deleteCartListByCode(num) :

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_delete = 'DELETE FROM cart WHERE product_code = %s'

    # 먼저 선언
    result_num1 = None
    result_num2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        result_num1 = cursor_aws.execute(sql_delete, num)
        cursor_aws.close()
        con_aws.close()

    if con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        result_num2 = cursor_azure.execute(sql_delete, num)
        cursor_azure.close()
        con_azure.close()

    return result_num1 if con_aws is not None else result_num2

# 상품 검색
def selectProductForSearch(searchQuery) :
    
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_select = 'SELECT * FROM product WHERE product_name LIKE %s;'

    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_aws.execute(sql_select, f'%{searchQuery}%')
        result1 = cursor_aws.fetchall()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_azure.execute(sql_select, f'%{searchQuery}%')
        result2 = cursor_azure.fetchall()
        cursor_azure.close()
        con_azure.close()

    else:
        pass

    return result1 if con_aws is not None else result2


# 장바구니(Cart) -> 주문(Orders) 테이블로 INSERT
def insertOrdersList(order_number, order_product_code, order_product_stock, 
                     order_product_price, order_user_id, order_user_name,
                     order_user_address, order_user_phone) :

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_insert = '''INSERT INTO orders (order_number, order_product_code, 
                    order_product_stock, order_product_price,
                    order_user_id, order_user_name,
                    order_user_address, order_user_phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''

    if con_aws is not None:
        cursor_aws = con_aws.cursor()
        cursor_aws.execute(sql_insert, (order_number, order_product_code, order_product_stock, 
                                order_product_price, order_user_id, order_user_name, 
                                order_user_address, order_user_phone))
        con_aws.commit()
        cursor_aws.close()
        con_aws.close()

    if con_azure is not None:
        cursor_azure = con_azure.cursor()
        cursor_azure.execute(sql_insert, (order_number, order_product_code, order_product_stock, 
                                order_product_price, order_user_id, order_user_name, 
                                order_user_address, order_user_phone))
        con_azure.commit()
        cursor_azure.close()
        con_azure.close()

# 결제 후 장바구니(Cart) 상품 전체 비우기
def deleteCartListAll(userId) :

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_delete = 'DELETE FROM cart WHERE user_id = %s'

    # 먼저 선언
    result_num1 = None
    result_num2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        result_num1 = cursor_aws.execute(sql_delete, userId)
        cursor_aws.close()
        con_aws.close()

    if con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        result_num2 = cursor_azure.execute(sql_delete, userId)
        cursor_azure.close()
        con_azure.close()

    return result_num1 if con_aws is not None else result_num2

# 장바구니 Cart List 상품수량 변경 시 UPDATE
def updateCartList(product_code, new_quantity, userId) :

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_update = 'UPDATE cart SET product_count = %s WHERE user_id = %s AND product_code = %s'
    
    # 먼저 선언
    result_num1 = None
    result_num2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        result_num1 = cursor_aws.execute(sql_update, (new_quantity, userId, product_code))
        cursor_aws.close()
        con_aws.close()

    if con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        result_num2 = cursor_azure.execute(sql_update, (new_quantity, userId, product_code))
        cursor_azure.close()
        con_azure.close()

    return result_num1 if con_aws is not None else result_num2

# 주문 내역 정보
def selectOrdersAll(userId):

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_select = """
    SELECT 
        o.order_number,
        o.order_product_code,
        p.product_name,
        o.order_product_stock,
        o.order_product_price,
        o.order_product_status,
        o.order_product_date,
        o.order_user_id,
        o.order_user_name,
        o.order_user_address,
        o.order_user_phone
    FROM 
        orders o
    INNER JOIN 
        product p
    ON 
        o.order_product_code = p.product_code
    WHERE
        o.order_user_id = %s
    """

    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_aws.execute(sql_select, userId)
        result1 = cursor_aws.fetchall()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_azure.execute(sql_select, userId)
        result2 = cursor_azure.fetchall()
        cursor_azure.close()
        con_azure.close()

    else:
        pass
    
    return result1 if con_aws is not None else result2