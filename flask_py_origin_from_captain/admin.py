from flask import *
import admin_DAO
import boto3
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import requests
import os
import logging

import db_data
from st_data import *


# Blueprint 설정
bp = Blueprint("admin", __name__, url_prefix="/admin")

# Logging 설정
logging.basicConfig(filename='error.log', level=logging.ERROR)
logger = logging.getLogger()

# main 관리 페이지
@bp.route('/home')
def home() :
    # 관리자가 아닐 경우 user/home으로 redirect
    if 'loginSessionInfo' in session :
        userInfo = session.get('loginSessionInfo')
        if userInfo.get('user_role') != 'role_admin' :
            return redirect(url_for('user.product'))
        return redirect(url_for('admin.product'))
    else :
        return redirect(url_for('login'))

# 상품정보
@bp.route('/product', methods=['POST', 'GET'])
def product() :
    if 'loginSessionInfo' in session :
        userInfo = session.get('loginSessionInfo')
        # 관리자가 아닐 경우 user/home으로 redirect
        if userInfo.get('user_role') != 'role_admin' :
            return redirect(url_for('user.product'))

        products = admin_DAO.selectProductAll()
        
        is_active_aws = db_data.active_aws()
        is_active_azure = db_data.active_azure()

        for product in products :
            # AWS
            if is_active_aws:
                imageName = product['product_image_aws']
                newImageName = get_public_url(S3_BUCKET, imageName)
                product['product_image_aws'] = newImageName
                logger.error(f"Generated AWS URL: {newImageName}")  # 로그 기록
            # Azure
            elif is_active_azure:
                imageName = product['product_image_azure']
                newImageName = get_public_url_azure(CONTAINER_NAME, imageName)
                product['product_image_azure'] = newImageName
            else:
                pass                    

        return render_template('admin/product.html', products = products, is_active_aws = is_active_aws)

    else :
        return redirect(url_for('login'))

# 상품 등록
@bp.route('/register', methods=['POST', 'GET'])
def register() :
    if 'loginSessionInfo' in session :
        userInfo = session.get('loginSessionInfo')
        # 관리자가 아닐 경우 user/home으로 redirect
        if userInfo.get('user_role') != 'role_admin' :
            return redirect(url_for('user.home'))
        
        if request.method == 'GET' :
            return render_template('admin/register.html')
        
        elif request.method == 'POST' :
            # 상품명
            productName = request.form['productName']

            # 상품가격
            productPrice = request.form['productPrice']

            # 상품재고
            productStock = request.form['productStock']

            # 상품설명
            productDescription = request.form['productDescription']

            # 상품이미지
            today_datetime = datetime.now().strftime("%Y%m%d%H%M")
            s3_file = request.files['productImage']
            s3_filename = today_datetime + '_' + s3_file.filename
            azure_file = request.files['productImage']
            azure_file_read = request.files['productImage'].read()
            azure_filename = today_datetime + '_' + azure_file.filename
            

            admin_DAO.insertProduct(productName, productPrice, 
                                    productStock, productDescription, 
                                    s3_filename, azure_filename)
            is_active_aws = db_data.active_aws()
            is_active_azure = db_data.active_azure()

            # "AWS"일 때, S3에 업로드
            if is_active_aws:
                s3_file.seek(0)
                s3_client.upload_fileobj(s3_file, S3_BUCKET,'ssgproduct/' + s3_filename)

            # "AWS" / "AZURE"일 때, Azure Blob에 업로드
            if is_active_azure :
                blob_client = container_client.get_blob_client(azure_filename)
                blob_client.upload_blob(azure_file_read)
                print(f"{s3_filename} uploaded to Azure Blob Storage.")

            # 어느 때든 업로드하자. 
            result = admin_DAO.dbToJson()
            objects = []
            for item in result:
                obj = {
                    "product_name": item[0],
                    "product_price": item[1],
                    "product_stock": item[2],
                    "product_description": item[3],
                    "product_image_aws": item[4],
                    "product_image_azure": item[5],
                }
                objects.append(obj)

            # 생성할 JSON 파일 설정
            FILE_NAME = "./db_data.json"
            f = open(FILE_NAME, 'w', encoding='utf-8')
            f.write(json.dumps(objects, ensure_ascii=False))
            f.close()

            # GitHub Gist를 업데이트합니다.
            file_content = read_json(FILE_NAME)
            if uploadJsonToGist(GIST_ID, "db_data.json", str(file_content), GITHUB_TOKEN):
                print("Updated GitHub Gist successfully.")
            else:
                print("Failed to update GitHub Gist.")

            return redirect(url_for('admin.product'))

        else :
            return redirect(url_for('login'))
    else :
        return redirect(url_for('login'))
    
# 상품 수정
@bp.route('/edit/<int:num>', methods=['GET', 'POST'])
def edit(num) :
    if 'loginSessionInfo' in session :
        userInfo = session.get('loginSessionInfo')
        # 관리자가 아닐 경우 user/home으로 redirect
        if userInfo.get('user_role') != 'role_admin' :
            return redirect(url_for('user.home'))
        
        if request.method == 'GET' :
            selectResult = admin_DAO.selectProductByCode(num)
            return render_template('admin/edit.html', selectResult = selectResult)
        
        elif request.method == 'POST' :
            # 상품명
            productName = request.form['productName']

            # 상품가격
            productPrice = request.form['productPrice']

            # 상품재고
            productStock = request.form['productStock']

            # 상품설명
            productDescription = request.form['productDescription']

            # 상품이미지
            today_datetime = datetime.now().strftime("%Y%m%d%H%M")
            s3_file = request.files['productImage']
            s3_filename = today_datetime + '_' + s3_file.filename
            azure_file = request.files['productImage']
            azure_file_read = request.files['productImage'].read()
            azure_filename = today_datetime + '_' + azure_file.filename

            admin_DAO.updateProductByCode(productName, productPrice, 
                                        productStock, productDescription, 
                                        s3_filename, azure_filename, num)

            is_active_aws = db_data.active_aws()
            is_active_azure = db_data.active_azure()

            # "AWS"일 때, S3에 업로드
            if is_active_aws :
                s3_file.seek(0)
                s3_client.upload_fileobj(s3_file, S3_BUCKET,'ssgproduct/'+ s3_filename)

            # "AWS" / "AZURE"일 때, Azure Blob에 업로드
            if is_active_azure :
                blob_client = container_client.get_blob_client(azure_filename)
                blob_client.upload_blob(azure_file_read)
                print(f"{s3_filename} uploaded to Azure Blob Storage.")

            # 언제든지 json 저장
            result = admin_DAO.dbToJson()
            objects = []
            for item in result:
                obj = {
                    "product_name": item[0],
                    "product_price": item[1],
                    "product_stock": item[2],
                    "product_description": item[3],
                    "product_image_aws": item[4],
                    "product_image_azure": item[5]
                }
                objects.append(obj)

            # 생성할 JSON 파일 설정
            FILE_NAME = "./db_data.json"
            f = open(FILE_NAME, 'w', encoding='utf-8')
            f.write(json.dumps(objects, ensure_ascii=False))
            f.close()

            # GitHub Gist를 업데이트합니다.
            file_content = read_json(FILE_NAME)
            if uploadJsonToGist(GIST_ID, "db_data.json", str(file_content), GITHUB_TOKEN):
                print("Updated GitHub Gist successfully.")
            else:
                print("Failed to update GitHub Gist.")

            return redirect(url_for('admin.product'))

        else :
            return redirect(url_for('login'))
    else :
        return redirect(url_for('login'))
    
# 상품 삭제
@bp.route('/delete/<int:num>', methods=['POST'])
def delete(num) :
    if 'loginSessionInfo' not in session:
        return redirect(url_for('login'))
    
    # 관리자일 경우에만 상품 삭제 가능
    userInfo = session.get('loginSessionInfo')
    if userInfo.get('user_role') != 'role_admin':
        return redirect(url_for('login'))
    
    is_active_aws = db_data.active_aws()
    is_active_azure = db_data.active_azure()

    result = admin_DAO.deleteProductByCode(num)
    # result : type -> tuple
    
    # json은 항상 관리
    results = admin_DAO.dbToJson()
    objects = []
    for item in results:
        obj = {
            "product_name": item[0],
            "product_price": item[1],
            "product_stock": item[2],
            "product_description": item[3],
            "product_image_aws": item[4],
            "product_image_azure": item[5]
        }
        objects.append(obj)

    # 생성할 JSON 파일 설정
    FILE_NAME = "./db_data.json"
    f = open(FILE_NAME, 'w', encoding='utf-8')
    f.write(json.dumps(objects, ensure_ascii=False))
    f.close()

    # JSON 파일을 읽어옵니다.
    file_content = read_json(FILE_NAME)

    # GitHub Gist를 업데이트합니다.
    if uploadJsonToGist(GIST_ID, "db_data.json", str(file_content), GITHUB_TOKEN):
        print("Updated GitHub Gist successfully.")
    else:
        print("Failed to update GitHub Gist.")

    if result[0] and result[1]:
        return jsonify({'message': '상품이 성공적으로 삭제되었습니다.'}), 200
    else:
        return jsonify({'message': '상품 삭제에 실패했습니다.'}), 500
    
    
# JSON -> Github GIST 자동 업로드
def uploadJsonToGist(gist_id, file_name, file_content, github_token):
    # 업데이트할 Gist의 URL을 생성합니다.
    gist_url = f"https://api.github.com/gists/{gist_id}"

    # GitHub API를 사용하여 Gist를 업데이트합니다.
    data = {
        "files": {
            file_name: {
                "content": file_content
            }
        }
    }

    # GitHub API를 사용하여 Gist를 업데이트합니다.
    response = requests.patch(
        gist_url,
        headers={"Authorization": f"token {github_token}"},
        json=data
    )

    # 요청이 성공하면 True를 반환합니다.
    if response.status_code == 200:
        return True
    else:
        # 요청이 실패하면 False를 반환합니다.
        print("Failed to update GitHub Gist.")
        error_message = f"Failed to update GitHub Gist. Status code: {response.status_code}, Response body: {response.text}"
        print(error_message)
        return False


# 고객 관리
@bp.route('/userInfo', methods=['GET'])
def userInfo() :
    if 'loginSessionInfo' in session :
        userInfo = session.get('loginSessionInfo')
        # 관리자가 아닐 경우 user/home으로 redirect
        if userInfo.get('user_role') != 'role_admin' :
            return redirect(url_for('user.home'))
        
        if request.method == 'GET' :
            users = []
            users = admin_DAO.selectUsersAll()

            return render_template('admin/userInfo.html', users = users)

        else :
            return redirect(url_for('login'))
    else :
        return redirect(url_for('login'))
    

# 주문 관리
@bp.route('/orderInfo', methods=['GET'])
def orderInfo() :
    if 'loginSessionInfo' in session :
        userInfo = session.get('loginSessionInfo')
        # 관리자가 아닐 경우 user/home으로 redirect
        if userInfo.get('user_role') != 'role_admin' :
            return redirect(url_for('user.home'))
        
        if request.method == 'GET' :
            orders = []
            orders = admin_DAO.selectOrdersAll()

            return render_template('admin/orderInfo.html', orders = orders)

        else :
            return redirect(url_for('login'))
    else :
        return redirect(url_for('login'))
