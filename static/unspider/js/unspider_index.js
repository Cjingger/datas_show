
// 获取表格内的高校抓取信息

function get_uninfo() {
    var set = [];
    $('.un-info').each(function() {
        var row = [];
        $(this).find('td').each(function() {
            row.push($(this).text());
        });
        set.push(row);
    });
    return set
}


//post提交表格数据到后端

function up_info(){
    $(document).ready(function(){
        info = get_uninfo()
        data = JSON.stringify({'data':info})
        var form_data = new FormData();
        form_data.append('csrfmiddlewaretoken', $('[name="csrfmiddlewaretoken"]').val());

        // 发送平台
        form_data.append('data', data);

        $.ajax({
            url: '/unspider',
            type: 'POST',
            data: form_data,
            processData: false,  // tell jquery not to process the data
            contentType: false, // tell jquery not to set contentType
            success: function (callback) {

            }
        });
    })

}


//点击确定提交信息抓取
function show_confirm(){
    var r=confirm("确认发送?");
    if (r==true){
        alert('正在抓取,稍后请前往首页查看数据')
        up_info()
    }
    else{
        alert("您已取消当前任务");
    }
}




function init_data() {
    var _init_tab = $('#show_un_history');
    _init_tab.bootstrapTable({
        url:'/unspider/show_un_history/',
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
                field: 'time',
                title: '时间',

            },
            {
                field: 'name',
                title: '姓名',


            },
            {
                field: 'data_from',
                title: '大学',

            },
            {
                field: 'subdiscipline',
                title: '专业',


            },
            {
                field: 'classify',
                title: '院系',

            },
            {
                field: 'statu',
                title: '状态',


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
    // $('#un_history').click(function () {
    init_data()
        // _init_tab.bootstrapTable('refresh'); //刷新表格

    // });
});


function responseHandler(res) {
    if (res) {
        return {
            "rows" : res.rows,
            "total" : res.total,
            // 'nums':$('#toolbar').html('总共搜索到' + '<a> ' + res.nums  + ' </a> '+ '条数据')
        };
    } else {
        return {
            "rows": [],
            "total": 0,
            // 'nums':$('#toolbar').html('总共搜索到<a> 0 </a>条数据')
        };
    }}











