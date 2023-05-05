# Lab2: Image Retrieval

> @author 2154298 Ying Wang

## Installation

- To run the code, you should also download and unzip [database.zip](https://anjt.oss-cn-shanghai.aliyuncs.com/database.zip) in `server`.

    1. You can easily download the dataset from the provided link and extract it. Then, place the extracted folder in the "server/database"  directory.
    2. Alternatively, you can use the command line to download and install it.

    - navigate to the directory where you want to download and extract the file. Then, enter the following command:

      ```
      wget https://anjt.oss-cn-shanghai.aliyuncs.com/database.zip
      ```

    - use the following command to extract the file:

      ```
      unzip database.zip
      ```

    -  Note that before running these commands, make sure you have installed the `wget` and `unzip` tools.

- After installing the essential package, you can run the code as follows:

    ```shell
    cd server
    python image_vectorizer.py
    ```

- Start the server as follows:

  ```shell
  python rest-server.py
  ```
  
  Then you can visit the website: http://127.0.0.1:5000/
  

## Project Structure

```
root folder
│  neighbor_list_recom.pickle
│  requirements.txt
│  __init__.py
│          
└─server
    │  image_vectorizer.py
    │  neighbor_list_recom.pickle
    │  rest-server.py
    │  saved_features_recom.txt
    │  search.py
    │  
    ├─database
    │  │  
    │  ├─dataset
    │  │      
    │  └─tags
    │          
    │              
    ├─imagenet
    │      classify_image_graph_def.pb
    │      
    ├─static
    |  |   main.js
    |  |   style.css
    |  |
    │  ├─collection
    |  |
    │  ├─images
    │  │      
    │  └─result
    │          
    ├─templates
    |  		collection.html
    │  		main.html 
    │          
    └─uploads
```

## Functionality

- ### Formulation

  - It contains an input box to upload an image:

    ![](D:\学习\TongjiTerm\大二下\用户交互技术\首页.png)

  - Users can preview the query image in the searching window:

    ![](D:\学习\TongjiTerm\大二下\用户交互技术\上传图片.png)

- ### Initiation of action

  - It has a search button, click the button for results:

    ![image-20230504205957253](C:\Users\shade\AppData\Roaming\Typora\typora-user-images\image-20230504205957253.png)

- ### Review of results

  - Provide an overview of the results, the overview displays the number of search results

    ![](D:\学习\TongjiTerm\大二下\用户交互技术\搜索结果.png)

- ### Refinement

  - Allow changing search parameters（select certain tag when reviewing results）

    for example: The user selects the  tag `structures`  and filters out the images that contain the tag in the results.

    ![](D:\学习\TongjiTerm\大二下\用户交互技术\筛选结果3.png)

- ### Use

  - Users can add selected images to a collection list

    - Users can click the stars to add a picture into collection list, and click it again to

      delete the picture from the collection list.

    ​	![](D:\学习\TongjiTerm\大二下\用户交互技术\点击收藏.png)

    - Users can click on the favorite icon located in the top left corner to view their

      collection of saved images.

      ![image-20230504210901859](C:\Users\shade\AppData\Roaming\Typora\typora-user-images\image-20230504210901859.png)

    