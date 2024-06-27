
// 上传图片后，显示预览图
document.getElementById('file-input').addEventListener('change', function(event) {
    const file = event.target.files[0]; // Get the file
    const reader = new FileReader();  // Create a file reader

    reader.onload = function(e) {  // Define what happens when reading completed
        const img = document.getElementById('previewImage');  // Get the image element

        img.onload = function() {
            const aspectRatio = img.width / img.height;

            // Get the previewImage and the container
            const previewImage = document.getElementById('previewImage');

            if (aspectRatio > 1) {  // Landscape
                previewImage.style.maxHeight = '400px';  // Limiting height for landscape
                previewImage.style.width = 'auto';
            } else {  // Portrait or square
                previewImage.style.maxWidth = '80%';  // Limiting width for portrait
                previewImage.style.height = 'auto';
            }
            previewImage.style.maxWidth = '80%';  // Limiting width for portrait
            previewImage.style.height = 'auto';
            // Set the image src and display the preview
            previewImage.src = e.target.result;
            document.getElementById('previewBox').style.display = 'block';
            document.getElementById('generateBtn').disabled = false;
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);  // Read the file as Data URL

});


document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.getElementById('generateBtn');
    const input = document.getElementById('file-input');

    input.addEventListener('change', function() {
        if (input.files.length > 0) {
            submitButton.disabled = false;
        }else {
            submitButton.disabled = true;
        }
    })

    // 检查是否存在 sessionid Cookie
            function getCookie(name){
                let cookieValue = null;
                if (document.cookie && document.cookie !=0) {
                    const cookies = document.cookie.split(';');
                    for (let i=0; i < cookies.length; i++) {
                         console.log(cookies[i])
                        const cookie = cookies[i].trim();
                        console.log(`Checking cookie: ${cookie}`);  // Debugging line
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            const sessionid = getCookie('sessionid');
            var userTitle = document.getElementById('userTitle')

            if (sessionid) {
                console.log('User is logged in');
                fetch('/api/user_info/',{
                   method:'GET',
                   headers:{
                       'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')  // 如果需要 CSRF token
                   } ,
                    credentials:'include'
                })
                    .then(response => response.json())
                    .then(data =>{
                        userTitle.textContent = data.username;

                    });
            }else {
                console.log('User is not logged in');
                window.location = "{%  url 'login' %}"
            }


            document.getElementById('generateBtn').addEventListener('click', function(event) {
                event.preventDefault(); // 阻止表单默认提交行为
                console.log('Button clicked');
                // 在这里执行您想要的操作，例如发送 AJAX 请求
                geterateBtnAction()
            });

            document.getElementById('downBtn').addEventListener('click', function(event) {
                downBtn()

            })

            document.getElementById('subtitleForm').addEventListener('submit', function(event) {
                event.preventDefault(); // 再次阻止表单默认提交行为
                console.log('Form submitted');
                // 在这里执行您想要的操作，例如发送 AJAX 请求

                 // 获取 CSRF token
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                fetch('api/get_user_count/',{
                        method: 'POST',
                        headers:{
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken
                        },
                })
                .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
                .then(data =>{
                    if (data['count'] > 1){
                        geterateBtnAction()
                    }

                })
                .catch(error => {
                    console.log(error)
                })
            });
});

function geterateBtnAction(){

        var errorText = document.getElementById('errorText')
        var loadingButton = document.getElementById('loadingButton');
        var generateBtn = document.getElementById('generateBtn');
        var fileInput = document.getElementById('file-input');

        var showTitle = document.getElementById('showTitle');
        var showDetail = document.getElementById('showDetail');

        var get_make_subtitle = document.getElementById('get_make_subtitle');
        var resource_box = document.getElementById('resource_box');


        const file = fileInput.files[0];
        const formData = new FormData();

        if (fileInput == null){
            errorText.textContent = '请先上传图片';
            return;
        }
        else {
            errorText.textContent = '';
            formData.append('file', file);

            loadingButton.style.display = 'block';
            generateBtn.style.display = 'none';
        }


        // 获取 CSRF token
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('api/get_matermark_subtitle/',{
                method: 'POST',
                headers:{
                    'X-CSRFToken': csrftoken
                },
                body:formData
            })
                .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                     loadingButton.style.display = 'none';
                    generateBtn.style.display = 'block';
                }
                return response.json();
            })
                .then(data =>{
                    console.log(data)
                    if (data['matermark_image_path']){

                        expend_user_count()

                        get_make_subtitle.src = data['matermark_image_path'];

                        showTitle.textContent = data['showTitle'];
                        showDetail.textContent = data['showDetail'];

                        loadingButton.style.display = 'none';
                        generateBtn.style.display = 'block';
                        resource_box.style.display = 'block';
                    }else{
                        errorText.textContent = 'Network abnormality, please try again'
                        loadingButton.style.display = 'none';
                        generateBtn.style.display = 'block';
                        resource_box.style.display = 'none';
                    }


                })
                .catch(error => {
                    console.log(error)
                    errorText.textContent = 'Network abnormality, please try again'
                    loadingButton.style.display = 'none';
                    generateBtn.style.display = 'block';
                    resource_box.style.display = 'none';
                })

}


function downBtn(){

    var down_loading_button = document.getElementById('down_loading_button');
    var downBtn = document.getElementById('downBtn');

    down_loading_button.style.display = 'block';
    downBtn.style.display = 'none';

    const get_make_subtitle = document.getElementById('get_make_subtitle').src;

    // 获取 CSRF token
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const data = {
            'get_make_subtitle':get_make_subtitle,
        }
        fetch('api/get_subtitle/',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body:JSON.stringify(data),
            })
                .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                    down_loading_button.style.display = 'none';
                    downBtn.style.display = 'block';
                }
                return response.json();
            })
                .then(data =>{

                    down_loading_button.style.display = 'none';
                    downBtn.style.display = 'block';

                    const a = document.createElement('a');
                    const imageName = '无水印照片.jpg'
                    a.href = data['data'];
                    a.download = imageName;
                    document.body.appendChild(a);

                    a.click();

                    document.body.removeChild(a);

                })
                .catch(error => {
                    console.log(error)
                    down_loading_button.style.display = 'none';
                    downBtn.style.display = 'block';
                })
}



function get_user_count(){

    var user_count = document.getElementById('resourceSpan');

    // 获取 CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch('api/get_user_count/',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
            })
                .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
                .then(data =>{
                    user_count.textContent = data['count'];

                })
                .catch(error => {
                    console.log(error)
                })
}


function expend_user_count(){
    // 获取 CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch('api/expend_user_count/',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
            })
                .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
                .then(data =>{
                    if (data['static'] ==1){
                        get_user_count()
                    }


                })
                .catch(error => {
                    console.log(error)
                })
}