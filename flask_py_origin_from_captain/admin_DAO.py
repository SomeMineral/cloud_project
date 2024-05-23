import pymysql
import db_data

# 상품정보 등록 - AWS
def insertProduct(productName, productPrice,
                  productStock, productDescription,
                  s3_filename, azure_filename) :

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure()
    sql_insert = "INSERT INTO product (product_name, product_price, product_stock, product_description, product_image_aws, product_image_azure) VALUES (%s, %s, %s, %s, %s, %s)"
        
    # 먼저 선언
    result_num1 = None
    result_num2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor()
        result_num1 = cursor_aws.execute(sql_insert, (productName, productPrice, productStock, productDescription, 'ssgproduct/'+ s3_filename, azure_filename))
        con_aws.commit()
        cursor_aws.close()
        con_aws.close()

    if con_azure is not None:
        cursor_azure = con_azure.cursor()
        result_num2 = cursor_azure.execute(sql_insert, (productName, productPrice, productStock, productDescription, 'ssgproduct/'+ s3_filename, azure_filename))
        con_azure.commit()
        cursor_azure.close()
        con_azure.close()


# DB to JSON
def dbToJson() :
    
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure()
    sql_select = "SELECT product_name, product_price, product_stock, product_description, product_image_aws, product_image_azure FROM product"
    
    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor()
        cursor_aws.execute(sql_select)
        result1 = cursor_aws.fetchall()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor()
        cursor_azure.execute(sql_select)
        result2 = cursor_azure.fetchall()
        cursor_azure.close()
        con_azure.close()
    
    else:
        pass

    return result1 if con_aws is not None else result2

# 상품 페이지
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

# 상품정보 수정을 위한 SELECT
def selectProductByCode(num) :
    
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_select = 'SELECT * FROM product WHERE product_code = %s'

    # 먼저 선언
    result1 = None
    result2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_aws.execute(sql_select, num)
        result1 = cursor_aws.fetchone()
        cursor_aws.close()
        con_aws.close()

    elif con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        cursor_azure.execute(sql_select, num)
        result2 = cursor_azure.fetchone()
        cursor_azure.close()
        con_azure.close()

    else:
        pass

    return result1 if con_aws is not None else result2

# 상품정보 수정 - AWS
def updateProductByCode(productName, productPrice, 
                        productStock, productDescription, 
                        s3_filename, azure_filename, num) :

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_update = "UPDATE product SET product_name = %s, product_price = %s, product_stock = %s, product_description = %s, product_image_aws = %s, product_image_azure = %s WHERE product_code = %s"

    # 먼저 선언
    result_num1 = None
    result_num2 = None

    if con_aws is not None:
        cursor_aws = con_aws.cursor(cursor=pymysql.cursors.DictCursor)
        result_num1 = cursor_aws.execute(sql_update, (productName, productPrice, productStock, productDescription, 'ssgproduct/'+ s3_filename, azure_filename, num))
        
        cursor_aws.close()
        con_aws.close()

    if con_azure is not None:
        cursor_azure = con_azure.cursor(cursor=pymysql.cursors.DictCursor)
        result_num2 = cursor_azure.execute(sql_update, (productName, productPrice, productStock, productDescription, 'ssgproduct/'+ s3_filename, azure_filename, num))

        cursor_azure.close()
        con_azure.close()

    return result_num1 if con_aws is not None else result_num2

# 상품정보 삭제 - AWS
def deleteProductByCode(num):

    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_delete = 'DELETE FROM product WHERE product_code = %s'

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

    return (result_num1, result_num2)

# 유저 정보
def selectUsersAll():
    
    con_aws = db_data.db_connect()
    con_azure = db_data.db_connect_azure() 
    sql_select = "SELECT * FROM users WHERE user_role = 'role_user' ORDER BY user_idx ASC"

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

# 주문 정보
def selectOrdersAll():
    
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
    """

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