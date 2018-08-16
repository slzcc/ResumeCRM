Dropzone.autoDiscover = false;
resume_id = "{{ uid }}"

// Get the template HTML and remove it from the doument
var previewNode = document.querySelector("#template");
previewNode.id = "";
var previewTemplate = previewNode.parentNode.innerHTML;
//开始先删除单个文件的布局
previewNode.parentNode.removeChild(previewNode);

var myDropzone = new Dropzone(document.body, { // 指定拖拽区为body
    url: "/source/upload/resume", // Set the url
    thumbnailWidth: 80,
    thumbnailHeight: 80,
    parallelUploads: 20,
    maxFiles: 10,
    maxFilesize: 5,
    acceptedFiles: ".pdf,.doc,.html,.txt,.docx",
    previewTemplate: previewTemplate,
    dictInvalidFileType: "文件类型错误，请重新选择! 支持格式为 pdf, doc, docx, txt.",
    dictMaxFilesExceeded: "您最多只能上传 10 个文件！",
    autoQueue: false, // 当队列有文件，是否立刻自动上传到服务器
    previewsContainer: "#previews", // 指定存放文件队列区
    clickable: ".fileinput-button", // 点击某个按钮或区域后出现选择电脑中本地图片，默认是previewsContainer指定的区域
    // init:function(){
    //     this.on("addedfile", function(file) { 
    //     //上传文件时触发的事件
    //     });
    //     this.on("queuecomplete",function(file) {
    //         //上传完成后触发的方法
    //     });
    //     this.on("removedfile",function(file){
    //         //删除文件时触发的方法
    //     });
    // }
});
myDropzone.on("addedfile", function(file) {
    // 让模版中的单个文件可以点击上传
    file.previewElement.querySelector(".start").onclick = function() { myDropzone.enqueueFile(file); };
});

// 显示所有文件整体上传进度1-100
myDropzone.on("totaluploadprogress", function(progress) {
    document.querySelector("#total-progress .progress-bar").style.width = progress + "%";
});

myDropzone.on("sending", function(file) {
    // 显示整体的上传的进度条，说明：原来是0，所以上面的style.width = progress + "%"即使是100%也看不到
     document.querySelector("#total-progress").style.opacity = "1";
    // 失效上传按钮
    file.previewElement.querySelector(".start").setAttribute("disabled", "disabled");
});

// 当没有文件上传时，隐藏进度条
myDropzone.on("queuecomplete", function(progress) {
    document.querySelector("#total-progress").style.opacity = "0";
});

// 发送自定义数据
myDropzone.on("sending", function(file, xhr, formData) {
    formData.append('resume_source', $('#resume_source option:selected').val());
    formData.append('update_file_type', "zh_filename");

});

// 上传所有
document.querySelector("#actions .start").onclick = function() {
    myDropzone.enqueueFiles(myDropzone.getAcceptedFiles());
//myDropzone.enqueueFiles(myDropzone.getFilesWithStatus(Dropzone.ADDED));与上面一样，可查看源码对比
};
//取消所有  
document.querySelector("#actions .cancel").onclick = function() {
    myDropzone.removeAllFiles(true);
};

    
