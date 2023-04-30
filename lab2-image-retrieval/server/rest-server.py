#!flask/bin/python
################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------                                                                                                                             
# This file implements the REST layer. It uses flask micro framework for server implementation. Calls from front end reaches 
# here as json and being branched out to each projects. Basic level of validation is also being done in this file. #                                                                                                                                  	       
#-------------------------------------------------------------------------------------------------------------------------------                                                                                                                              
################################################################################################################################
from flask import Flask, jsonify, abort, request, make_response, url_for,redirect, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os
import shutil 
import numpy as np
from search import recommend
import re #正则
import urllib.request
import tarfile
from datetime import datetime
from scipy import ndimage
#from scipy.misc import imsave

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
from tensorflow.python.platform import gfile
app = Flask(__name__, static_url_path = "")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()

#==============================================================================================================================
#                                                                                                                              
#    Loading the extracted feature vectors for image retrieval                                                                 
#                                                                          						        
#                                                                                                                              
#==============================================================================================================================
extracted_features=np.zeros((2955,2048),dtype=np.float32)
#读取特征值文件
with open('saved_features_recom.txt') as f:
    for i, line in enumerate(f):
        extracted_features[i, :] = line.split()
print("loaded extracted_features")


# 所有标签
tags = ['animals', 'baby', 'bird', 'car', 'clouds', 'dog', 'female',
            'flower', 'food', 'indoor', 'lake', 'male', 'night', 'people',
            'plant_life', 'portrait', 'river', 'sea', 'structures', 'sunset',
            'transport', 'tree', 'water']

def image_tags():
    # 标签字典,key是标签名，value是对应的图片编号
    tagDict = dict()
    for i in tags:
        tagDict[i] = []
        # 逐行读取每个标签对应的文件
        with open('database/tags/' + i + '.txt', 'r') as f:
            #文件中每一行内容作为一个string存储到list中
            list = f.readlines()
            for j in list:
                tagDict[i].append(j.strip()) #j去除首尾空格
    return tagDict


# 存储图片标签
tagDict = image_tags()

# 用户上传文件对应的标签
upload_tag = []


# 收藏图片
@app.route('/collect',methods=['POST','GET'])
def add_collection():
    # 获取上传图片的图片名和图片路径\
    imgSrc = request.form.get('imgSrc')
    img_src=imgSrc.encode()
    img_name = re.findall(r'[^\\/:*?"<>|\r\n]+$', imgSrc)[0]
    #被选择的图片文件名是否在收藏夹collection中,若在，则img_collect=true,
    file_path = os.path.join('static/collection', img_name)
    img_collect=os.path.exists(file_path);
    print(img_collect)

    # 图片已收藏
    if(img_collect):
        os.remove(file_path) # 删除文件
    # 图片未收藏
    else:
        # 创建 collection 文件夹
        collection = 'static/collection'
        if not gfile.Exists(collection):
            os.mkdir(collection)
        # 将图像保存到指定路径
        with open('static/collection/' + img_name, 'wb') as f:
            f.write(img_src)

    return jsonify({'img_collect':img_collect})

@app.route('/mycollection')
def mycollection():
    return render_template('collection.html')

@app.route('/show_collection',methods=['POST','GET'])
def show_collection():
    collection_path = 'static/collection'
    # img_paths = [os.path.join(collection_path, img_name) for img_name in os.listdir(collection_path)]

    collection = "/collection"
    img_paths = [os.path.join(collection, file) for file in os.listdir(collection_path)
                  if not file.startswith('.')]
    # for i in img_paths:
    #     i= i.replace('/collection\\', 'http://127.0.0.1:5000/')
    #     print(i)

    return jsonify({'img_paths':img_paths})


# 判断选中的图片是否已收藏
# @app.route('/is_collected',methods=['POST'])
# def is_collected():
#     imgSrc = request.form.get('imgSrc')
#     img_name = re.findall(r'[^\\/:*?"<>|\r\n]+$', imgSrc)[0]
#     print(imgSrc)
#     print(img_name)
#
#     # 被选择的图片文件名是否在收藏夹collection中,若在，则img_collect=true,
#     file_path = os.path.join('static', 'collection', img_name)
#     img_collect = os.path.exists(file_path);
#
#     return jsonify({'img_collect':img_collect})

@app.route('/filter', methods=['POST'])
def filter_images():
    # 解析POST请求的参数
    select_tag = request.form.get('select_tag')
    # 这里可以根据接收到的参数来处理相应的业务逻辑，比如过滤图片
    #response：最终返回的过滤结果
    response = {}
    count=0  #过滤出的图片数量
    # print("select_tag",select_tag)
    # for i in tagDict[select_tag]:
    #     result_path='http://127.0.0.1:5000/result/im' + i + '.jpg'  # 返回过滤后的图片URL
    #     if os.path.exists(result_path):
    #         response['image'+count]=result_path
    #         count=count+1

    response['num']=count;#过滤出的图片数量

    return jsonify(response)

#==============================================================================================================================
#                                                                                                                              
#  This function is used to do the image search/image retrieval
#                                                                                                                              
#==============================================================================================================================
@app.route('/imgUpload', methods=['GET', 'POST'])
#def allowed_file(filename):
#    return '.' in filename and \
#           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def upload_img():
    print("image upload")
    result = 'static/result'
    if not gfile.Exists(result):
          os.mkdir(result)
    shutil.rmtree(result)
 
    if request.method == 'POST' or request.method == 'GET':
        print(request.method)
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        print(file)
        print(file.filename)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        if file:# and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            inputloc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            recommend(inputloc, extracted_features)
            os.remove(inputloc)
            image_path = "/result"
            image_list =[os.path.join(image_path, file) for file in os.listdir(result)
                              if not file.startswith('.')]
            images = {
			'image0':image_list[0],
            'image1':image_list[1],	
			'image2':image_list[2],	
			'image3':image_list[3],	
			'image4':image_list[4],	
			'image5':image_list[5],	
			'image6':image_list[6],	
			'image7':image_list[7],	
			'image8':image_list[8]
		      }
            print(images['image0'])

            #tagDict:tagname+num
            # 获取上传文件的文件名
            uploadfile = file.filename
            # 提取文件名中的数字
            upload_num = uploadfile.split('.')[0][-1]
            #清空upload_tag数组
            upload_tag=[]

            # 检查数字是否在标签列表中出现过
            for i in tags:
                # 若在该标签中出现
                if upload_num in tagDict[i]:
                    upload_tag.append(i)
            print(upload_tag)

            # 二元数组，下标对应图片名
            img_tag = [[] for i in range(0, 3000)]  # 创建一个包含3000个空列表的数组
            # i：图片名
            for i in range(0, 3000):
                # j：标签名
                for j in tags:
                    # 若i图片拥有标签j，则将j加入数组
                    if str(i) in tagDict[j]:
                        img_tag[i].append(j)

            for i in range(0,10):
                print(img_tag[i])


            upload_dict={"images":images,"upload_tag":upload_tag,"img_tag":img_tag}

            return jsonify(upload_dict)




#返回一个二维数组，第一个下标对应图片名数字，数组元素为一个字符串数组，对应该图片的标签
# @app.route('/AllTags',methods=['POST','GET'])
# def Tags():
#     return jsonify(img_tag)


#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/",methods=['GET', 'POST'])
def main():
    return render_template("main.html")
if __name__ == '__main__':
    app.run(debug = True, host= '0.0.0.0')
