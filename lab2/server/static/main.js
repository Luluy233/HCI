function myFunction(){
    document.getElementById("predictedResult").innerHTML= "";
    $('#clear').hide();
}

// 显示上传的图片
function FileUpload()
{
    var fileInput = document.getElementById('file_input');
    var uploadedImage = document.getElementById('selectImg');

    fileInput.addEventListener('change', (event) => {
        var file = event.target.files[0];
        var reader = new FileReader();


        reader.readAsDataURL(file);

        reader.onload = () => {
            uploadedImage.src = reader.result;
            uploadedImage.style.display = 'block';
        }
    });
}

// 获取所有class为collect的button元素
var btnList = document.getElementsByClassName("collect");
// 遍历每个button元素并为其添加点击事件监听器
for (var i = 0; i < btnList.length; i++) {
    //判断是否已收藏         
    var btn=btnList[i];
    // 图片链接 
    var imgSrc = btn.previousElementSibling.src;
    // 图片名
    var imgName = imgSrc.substring(imgSrc.lastIndexOf('/') + 1);
    // $.ajax({
    //         url:"is_collected",
    //         type:"POST",
    //         data:{
    //             imgSrc:imgSrc
    //         },
    //         success: function(response) {
    //             //点击button前已收藏
    //             if(response.img_collect){     
    //                 btn.style.backgroundImage="url(images/collected-icon.png)"; 
    //             }
    //             else{  //点击button前未收藏
    //                 btn.style.backgroundImage="url(images/collect-icon.png)";  
    //             }
    //         },
    // });          

    //添加监听器          
    btnList[i].addEventListener("click", function(event){
         // event.target获取触发事件的按钮
        var button=event.target;
        // 图片链接 
        var imgSrc = button.previousElementSibling.src;
        // 图片名
        // var imgName = imgSrc.substring(imgSrc.lastIndexOf('/') + 1);
        $.ajax({
            url:"collect",
            type:"POST",
            data:{
                imgSrc:imgSrc
                // imgName:imgName
                // collected:button.dataset.collected
            },
            success: function(response) {
                //点击button前已收藏
                if(response.img_collect){     
                    button.style.backgroundImage="url(images/collect-icon.png)"; 
                }
                else{  //点击button前未收藏
                    button.style.backgroundImage="url(images/collected-icon.png)";  
                }
            },
            error: function(xhr) {
                console.log(xhr);
            }  
        });     
    });
}


function fun(){
    
    $('#load').show();
    $("form").submit(function(evt){	 
    //$('#loader-icon').show(); 
                
    evt.preventDefault();
    
            //$('#loader-icon').show();
        var formData = new FormData($(this)[0]);
    
    $.ajax({
        // 发出请求的路由
        url: 'imgUpload',
        type: 'POST',
        data: formData,
        //async: false,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
    
        success: function (response) {
            $('#load').hide();
            $('#row1').show();
            //$('#clear').show();
            //console.log(response[1]);
            //document.getElementById("predictedResult").innerHTML= response; 
            // 记录结果图片数组的编号

            // var result=[];


                                // 遍历reponse中的图片数量
            for(i=0;i<9;i++){
                $('#img' + i).parent().show();
            }
            document.getElementById("img0").src = response.images.image0;
            document.getElementById("img1").src = response.images.image1;
            document.getElementById("img2").src = response.images.image2;
            document.getElementById("img3").src = response.images.image3;
            document.getElementById("img4").src = response.images.image4;
            document.getElementById("img5").src = response.images.image5;
            document.getElementById("img6").src = response.images.image6;
            document.getElementById("img7").src = response.images.image7;
            document.getElementById("img8").src = response.images.image8;
            document.getElementById('result_count').innerHTML = "为您找到结果共9条"


            const labelsContainer = document.querySelector('.tag');

            $('.tag').empty();//删除所有子元素
            // 动态创建并添加标签元素
            response.upload_tag.forEach(tag => {
                const span = document.createElement('span');
                span.textContent = tag;
                span.classList.add('label');
                // span.classList.add(`label-${tag}`);
                labelsContainer.appendChild(span);
            });
       
            // 获取所有类名为label的元素
            var checkboxes = document.querySelectorAll('span.label');
            //为标签元素添加监听器
            for(var i=0;i<checkboxes.length;i++){
                checkboxes[i].addEventListener("click",function(event){
                    var selected=event.target;
                    for(var j=0;j<checkboxes.length;j++){
                        checkboxes[j].style.backgroundColor='rgb(154, 171, 219)';
                    }
                    selected.style.backgroundColor='#caa4e2';
                    select_tag=selected.textContent;
                    $.ajax({
                        url: 'filter',
                        type: 'POST',
                        data:{
                            select_tag:select_tag
                        },
                        //async: false,
                        // cache: false,
                        // contentType: false,
                        // enctype: 'multipart/form-data',
                        // processData: false,

                        success: function (response) {
                            console.log("filting success!");
                            console.log(response);

                            // 遍历reponse中的图片数量
                             for(i=0;i<9;i++){
                                $('#img' + i).parent().show();
                            }
                            // 显示过滤结果
                            for (i = 0; i < response.num; i++) {
                                document.getElementById('img' + i).src = response.result[i];
                            }
                            //不显示过滤结果
                            for (j = response.num; j < 9; j++) {
                                // document.getElementById('img' + j).parentNode.style.display = 'none';
                                $('#img' + j).parent().hide();
                            }
                            document.getElementById('result_count').innerHTML = "为您找到结果共"+response.num+"条"
                        }
                })
                })
            }

            // var btnList = document.getElementsByClassName("collect");
            // for (var i = 0; i < btnList.length; i++) {
            //     //判断是否已收藏         
            //     var btn=btnList[i];
            //     // 图片链接 
            //     var imgSrc = btn.previousElementSibling.src;
            //     $.ajax({
            //             url:"is_collected",
            //             type:"POST",
            //             data:{
            //                 imgSrc:imgSrc
            //             },
            //             success: function(response) {
            //                 //点击button前已收藏
            //                 if(response.img_collect){     
            //                     btn.style.backgroundImage="url(images/collected-icon.png)"; 
            //                 }
            //                 else{  //点击button前未收藏
            //                     btn.style.backgroundImage="url(images/collect-icon.png)";  
            //                 }
            //             },
            //     });        
            // }
            $('#table').show();
            $('#clear').show();
        }

    });
return false;
})};
