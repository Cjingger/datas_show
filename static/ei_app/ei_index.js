
// 展示ei数据

function init_data() {
    var _init_tab = $('#ei_tab');
    _init_tab.bootstrapTable({
        url:'/ei/get_ei/',
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
                'pagesize': this.pageSize,
                'time': $('#time').val(),
                'clss_code': $('#clss_code').val(),
                'control_term': $('#control_term').val(),
            };
            return temp;
        },

        columns: [
            {
                field: 'article',
                title: '标题',
                cellStyle: formatTableUnit,
                formatter: paramsMatter


            },
            {
                field: 'name',
                title: '姓名',
                cellStyle: formatTableUnit,
                formatter: paramsMatter
            },
            {
                field: 'email',
                title: '邮箱',
                cellStyle: formatTableUnit,
                formatter: paramsMatter


            },
            {
                field: 'is_ch',
                title: '国籍',
                cellStyle: formatTableUnit,
                formatter: paramsMatter

            },
            {
                field: 'time',
                title: '时间',
                cellStyle: formatTableUnit,
                formatter: paramsMatter


            },

            {
                field: 'clss_code',
                title: '归类',
                cellStyle: formatTableUnit,
                formatter: paramsMatter
            },
            {
                field: 'control_term',
                title: '受控词',
                cellStyle: formatTableUnit,
                formatter: paramsMatter
            },

        ],

        onLoadError: function () {
            alert("数据加载失败！", "错误提示");
        },
    });


}



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


//表格超出宽度鼠标悬停显示td内容
function paramsMatter(value, row, index, field) {

    var span = document.createElement('span');
    span.setAttribute('title', value);
    span.innerHTML = value;
    return span.outerHTML;
}
//td宽度以及内容超过宽度隐藏
function formatTableUnit(value, row, index) {
    return {
        css: {
            "white-space": 'nowrap',
            "text-overflow": 'ellipsis',
            "overflow": 'hidden',
            "max-width": "300px"
        }
    }
}
//初始化
$(function () {
    init_data()

});


//点击查询刷新
$(document).ready(function (){
    $('#select_ei').click(function (){
        var _init_tab = $('#ei_tab')
        _init_tab.bootstrapTable('refresh');
    })
})


//导出数据
$(document).ready(function () {
    $('#movement').click(function () {
        var start_num = parseInt($('#start_num').val());
        var end_num = parseInt($('#end_num').val());
        if(end_num-start_num>5000 || Boolean(start_num) ===false || Boolean(end_num) === false || end_num<start_num){
            alert('输入有误,请重新输入')
        }
        else {
            document.getElementById('exampleModal').style.display='none';
            $(".modal-backdrop").hide();

            $.post('/ei/exportion',{
                'start_num':start_num,
                'end_num':end_num,
                'time': $('#time').val(),
                'clss_code': $('#clss_code').val(),
                'control_term': $('#control_term').val(),
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
                },function (data) {
                    obj = JSON.parse(data)["data"]
                    if(obj){
                        exportExcel(obj)
                    }else{
                        alert('导出失败,请联系管理员查看原因')
                    }
            })

        }
    })
})


// 导出查询数据
function exportExcel(obj) {
    var option={};
    option.fileName = 'excel'  //文件名称
    option.datas=[
      {
        sheetData:obj,
        sheetName:'sheet',  //sheet名称
        sheetFilter:['article','name','email','is_ch','time','affils','abstracty','clss_code','control_term'],    //用于过滤json中的数据进行导出数据筛选
        sheetHeader:['article','name','email','is_ch','time','affils','abstracty','clss_code','control_term'],    //用于过滤json中的数据进行导出数据筛选,  //第一行的标题
      }
    ];
    var toExcel=new ExportJsonExcel(option);
    toExcel.saveExcel();
}









