// 上传文件
function send_test() {

    $(document).ready(function () {
        var form_data = new FormData();
        var file_info = $('#file_upload')[0].files;
        for (var i = 0; i < file_info.length; i++) {
            form_data.append("file", file_info[i]);
        }
        form_data.append('csrfmiddlewaretoken', $('[name="csrfmiddlewaretoken"]').val());
        form_data.append('subject',$('#subject').val());

        $.ajax({
            url: '/scispider/',
            type: 'POST',
            mimeType: "multipart/form-data",
            data: form_data,
            processData: false,  // tell jquery not to process the data
            contentType: false, // tell jquery not to set contentType
            success: function (data) {
                console.log(data)
            }
        }).alert(()=>{
            console.log("success!")
        });
    })
}



//点击确认后执行上传文件方法
function show_confirm(){
    var r=confirm("确认?");
    if (r==true){
        alert('后台正在解析,请耐心等待')
        send_test()
    }
    else{
        alert("您已取消当前任务");
    }
}




// 展示sci解析记录

function init_data() {
    var _init_tab = $('#show_sci_history');
    _init_tab.bootstrapTable({
        url:'/scispider/show_sci_history/',
        method: 'GET',
        dataType: "json",
        uniqueId: 'id',
        striped: true,
        cache: false,
        sortName: 'id',
        sortable: false,
        sortOrder: 'desc',
        sidePagination: "server",
        undefinedText: '--',
        singleSelect: false,
        search: false,
        strictSearch: true,
        clickToSelect: true,
        pagination: true,
        pageNumber: 1,
        pageSize: 10,
        paginationPreText: "<",
        paginationNextText: ">",
        queryParamsType: "",
        showRefresh: true,
        responseHandler: responseHandler,

        queryParams: function (params) {
            var temp = {
                'offset': this.pageNumber, // SQL语句起始索引
                'pagesize': this.pageSize
            };
            return temp;
        },


        columns: [{
                field: 'id',
                title: 'id',


            },
            {
                field: 'user',
                title: '用户',
            },
            {
                field: 'subject',
                title: '专业/关键词',

            },
            {
                field: 'mark',
                title: '标记',

            },
            {
                field: 'time',
                title: '时间',


            },
            {
                field: 'status',
                title: '状态',

            },
            {
                field: 'num',
                title: '数量',
            },
            {
                field: 'button',
                title: '操作',
                events: operateEvents1,
                formatter: operateFormatter

            },

        ],

        onLoadError: function () {
            alert("数据加载失败！", "错误提示");
        },
        //onClickRow: function (row, $element) {
        //    EditViewById(id, 'view');
        //}
    });

}
$(function () {
    init_data()

});


function responseHandler(res) {
    if (res) {
        return {
            "rows" : res.rows,
            "total" : res.total,

        };
    } else {
        return {
            "rows": [],
            "total": 0,
        };
    }
}


//对应点击事件
window.operateEvents1 = {
		'click .RoleOfA': function(e, value, row, index) {
		    var status = row['status']
            if (status == '解析成功'){
                var form_data = new FormData();
                form_data.append('mark',row['mark']);
                form_data.append('csrfmiddlewaretoken', $('[name="csrfmiddlewaretoken"]').val());

                $.ajax({
                    url: '/scispider/expro_sci/',
                    type: 'POST',
                    data: form_data,
                    processData: false,  // tell jquery not to process the data
                    contentType: false, // tell jquery not to set contentType
                    success: function (data) {
                        obj = JSON. parse(data)["data"]
                        if(obj){
                            exportExcel(obj)
                        }else{
                            alert('导出失败,请联系管理员查看原因')
                        }
                    }
                });
            }else{
                alert('当前解析状态显示不成功,请稍后再试')
            }

		}
	};

	function operateFormatter(value, row, index) {
        return [
            '<button id="btn_detail" type="button" class="RoleOfA btn-default bt-select">导出</button>',
        ].join('');
}





// 导出查询数据
function exportExcel(obj) {
    var option={};
    option.fileName = 'excel'  //文件名称
    option.datas=[
      {
        sheetData:obj,
        sheetName:'sheet',  //sheet名称
        sheetFilter:['create_date','time','data_from','keyword','is_qikan','article','area','is_ch','name','email','classify','url','discipline','subdiscipline'],    //用于过滤json中的数据进行导出数据筛选
        sheetHeader:['create_date','time','data_from','keyword','is_qikan','article','area','is_ch','name','email','classify','url','discipline','subdiscipline'],    //用于过滤json中的数据进行导出数据筛选,  //第一行的标题
      }
    ];
    var toExcel=new ExportJsonExcel(option);
    toExcel.saveExcel();
}

 // 转化json
function strToJson(str){
    var res = (new Function("return " + str))();
    return res;
}









