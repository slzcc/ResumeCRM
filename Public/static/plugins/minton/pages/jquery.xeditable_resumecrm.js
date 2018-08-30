
/**
* Theme: Minton Admin Template
* Author: Coderthemes
* Demo: Editable (Inline editing)
* 
*/

$(function(){

    //modify buttons style
    $.fn.editableform.buttons =
        '<button type="submit" class="btn btn-primary editable-submit btn-sm waves-effect waves-light" id="xeditable_submit" ><i class="mdi mdi-check"></i></button>' +
        '<button type="button" class="btn btn-light editable-cancel btn-sm waves-effect" id="xeditable_cancel" ><i class="mdi mdi-close"></i></button>';

    //Inline editables
    $('#inline-DownloadRN').editable({
        type: 'text',
        pk: 1,
        name: 'download-resume-number',
        title: 'Enter download-resume-number',
        mode: 'inline',
        inputclass: 'form-control-sm'
    });

    $('#inline-AutoUnlockResume').editable({
        type: 'text',
        pk: 1,
        name: 'upload-resume-unlock-time',
        title: 'Enter Unlock Time',
        mode: 'inline',
        inputclass: 'form-control-sm'
    });

    $('#inline-firstname').editable({
        validate: function(value) {
            if($.trim(value) == '') return 'This field is required';
        },
        mode: 'inline',
        inputclass: 'form-control-sm'
    });


    $('#inline-dob').editable({
        mode: 'inline',
        inputclass: 'form-control-sm'
    });

    $('#inline-event').editable({
        placement: 'right',
        mode: 'inline',
        combodate: {
            firstItem: 'name'
        },
        inputclass: 'form-control-sm'
    });

    $('#inline-comments').editable({
        showbuttons: 'bottom',
        mode: 'inline',
        inputclass: 'form-control-sm'
    });

    $('#inline-fruits').editable({
        pk: 1,
        limit: 3,
        mode: 'inline',
        inputclass: 'form-control-sm',
        source: [
            {value: 1, text: 'Banana'},
            {value: 2, text: 'Peach'},
            {value: 3, text: 'Apple'},
            {value: 4, text: 'Watermelon'},
            {value: 5, text: 'Orange'}
        ]
    });


});

function SubmitData(){
    var postData = {}
    $('#xeditable_table').find('a[edit-enable="true"]').each(function () {
        var n = $(this).attr("name")
        var v = $(this).text()

        if ($(this).attr("old-data") != v){
            postData[n] = v;
        }
        
    })
    if (!jQuery.isEmptyObject(postData)){
        $.ajax({
            url: "",
            type: "POST",
            dataType: "JSON",
            data: postData,
            success: function(arg){
                if(arg.status_code == "200"){
                    $('#xeditable_table').find('a[edit-enable="true"]').each(function () {
                        var n = $(this).attr("name")
                        var v = $(this).text()
                        var _self = $(this)
                        $.each(postData, function (k, row) {
                            if (n == k){
                                _self.attr("old-data", row);
                            }
                        });
                    })
                }else{
                    swal({
                        title: '错误',
                        text: "输入的格式有误请重新输入!",
                        type: 'error',
                        confirmButtonClass: 'btn btn-confirm mt-2'
                    }).then(function () {
                        // window.location.href="/resume/template/list";
                    });
                }
            }
        })
        
    };
}
var t2 = window.setInterval("SubmitData()",1000);