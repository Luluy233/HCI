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

# 根据id获取图片内容
# @app.route('/image', methods=['GET'])
# def get_img():
#     imageId = request.values.get('id')
#
#     # 将对应图片复制到static文件夹下
#     with open('database/dataset/im' + imageId + '.jpg', mode='rb') as f:
#         byte_data = f.read()
#
#     return Response(byte_data, mimetype='image/jpeg')
#
#
# # 获取用户全部收藏
# @app.route('/collect/all', methods=['GET'])
# def get_all_collect():
#     res = []
#     with open('database/favorites.txt', mode='r') as f:
#         for i in f.readlines():
#             res.append(i.strip())
#     return jsonify(res)
#
#
# # 改变图片收藏状态
# @app.route('/collect', methods=['GET'])
# def change_img_collect():
#     imageId = request.values.get('id')
#
#     # 获取collect文件夹内容
#     with open('database/favorites.txt', mode='r') as f:
#         s = f.readlines()
#
#     p = []
#     isCollected = False
#     for i in s:
#         # 已经收藏过了
#         if i.strip() == imageId:
#             isCollected = True
#         else:
#             p.append(i.strip())
#
#     if not isCollected:
#         p.append(imageId)
#
#     # 写文件
#     n = len(p)
#     with open('database/favorites.txt', mode='w') as f:
#         for index, item in enumerate(p):
#             if index != n - 1:
#                 f.write(item + '\n')
#             else:
#                 f.write(item)
#
#     return jsonify({
#         'status': True,
#     })
#
#
# @app.route("/tags", methods=['GET'])
# def get_tags():
#     res = []
#     for i in typeDict.keys():
#         res.append({
#             'label': i,
#             'size': len(typeDict[i]),
#         })
#     res.sort(key=lambda x: x['size'], reverse=True)
#     return jsonify(res)
#
#
# @app.route('/info', methods=['GET'])
# def get_img_info():
#     imageId = request.values.get('id')
#
#     # 查看favorites文件夹
#     with open('database/favorites.txt', mode='r') as f:
#         isCollected = False
#         for i in f.readlines():
#             if i.strip() == imageId:
#                 isCollected = True
#                 break
#
#     # 获取图片类型
#     tags = []
#     for i in typeDict.keys():
#         if imageId in typeDict[i]:
#             tags.append(i)
#
#     return jsonify({
#         'isCollected': isCollected,
#         'tags': tags,
#     })

# 用户上传文件对应的标签
upload_tag = []

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


            upload_dict={"images":images,"upload_tag":upload_tag}

            return jsonify(upload_dict)

 # 二元数组，下标对应图片名
img_tag = [[] for i in range(0, 3000)] # 创建一个包含3000个空列表的数组
# i：图片名
for i in range(0, 3000):
    # j：标签名
    for j in tags:
        # 若i图片拥有标签j，则将j加入数组
        if i in tagDict[j]:
            img_tag[i].append(j)

for i in range(0,3000):
    print(img_tag[i])


@app.route('/AllTags',methods=['POST','GET'])
def Tags():
    return jsonify(img_tag)


#==============================================================================================================================
#                                                                                                                              
#                                           Main function                                                        	            #						     									       
#  				                                                                                                
#==============================================================================================================================
@app.route("/")
def main():
    return render_template("main.html")
if __name__ == '__main__':
    app.run(debug = True, host= '0.0.0.0')
