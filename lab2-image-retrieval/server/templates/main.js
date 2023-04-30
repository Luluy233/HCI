    // <!-- 图片标签 -->
    tags = ['animals', 'baby', 'bird', 'car', 'clouds', 'dog', 'female',
    'flower', 'food', 'indoor', 'lake', 'male', 'night', 'people',
    'plant_life', 'portrait', 'river', 'sea', 'structures', 'sunset',
    'transport', 'tree', 'water'];

// // 显示上传的图片
// function xmTanUploadImg(obj) {
//     var file = obj.files[0];
//     var reader = new FileReader();
//     reader.readAsDataURL(file);
//     reader.onload = function (e) {    //成功读取文件
//         var img = document.getElementById("selectImg");
//         img.src = e.target.result;   //或 img.src = this.result / e.target == this
//     };
// }


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

            document.getElementById("img0").src = response.images.image0;
            // result.push(response.images.image0.replace(/[^\d]/g,' '));
            document.getElementById("img1").src = response.images.image1;
            // result.push(response.images.image1.replace(/[^\d]/g,' '));
            document.getElementById("img2").src = response.images.image2;
            // result.push(response.images.image2.replace(/[^\d]/g,' '));
            document.getElementById("img3").src = response.images.image3;
            // result.push(response.images.image3.replace(/[^\d]/g,' '));
            document.getElementById("img4").src = response.images.image4;
            // result.push(response.images.image4.replace(/[^\d]/g,' '));
            document.getElementById("img5").src = response.images.image5;
            // result.push(response.images.image5.replace(/[^\d]/g,' '));
            document.getElementById("img6").src = response.images.image6;
            // result.push(response.images.image6.replace(/[^\d]/g,' '));
            document.getElementById("img7").src = response.images.image7;
            // result.push(response.images.image7.replace(/[^\d]/g,' '));
            document.getElementById("img8").src = response.images.image8;
            // result.push(response.images.image8.replace(/[^\d]/g,' '));

            const labelsContainer = document.querySelector('.tag');

            // 动态创建并添加标签元素
            response.upload_tag.forEach(tag => {
                const span = document.createElement('span');
                span.textContent = tag;
                span.classList.add('label');
                // span.classList.add(`label-${tag}`);
                labelsContainer.appendChild(span);
            });

            // for (var i=0;i<response.upload_tag.length;i++){
            //     console.log(response.upload_tag[i])
            //         document.getElementById("tag"+i).innerHTML=response.upload_tag[i];
            // }

            // 为结果图片添加标签

            // var tags=new Array();
            // for(var i=0;i<9;i++){
            //     tags[i]=response.img_tag[result[i]];
            //     console.log(tags[i]);
            // }

            // for(var i=0;i<9;i++){
            //     // 获取当前图片的标签数组
            //     var imageTags=[];
            //     for(var k=0;k<tags.length;k++){
            //         imageTags[k]=tags[i][k];
            //         console.log(imageTags[k]);
            //     }
                

            //     // 获取当前图片的类名
            //     var className=".tag"+i;

            //     // 获取当前图片的jQuery对象
            //     var $image=$(className);

            //     // 循环遍历当前图片的标签数组，并将每个标签添加
            //     for(var j=0;j<imageTags[i].length;j++){
            //         $image.append("<span class='tag'>" + imageTags[j] + "</span>");
            //     }
            // }
            
            $('#table').show();
            $('#clear').show();
        }

    });
return false;
})};






