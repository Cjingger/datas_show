;layui.use('table', function(){
  var table = layui.table;
  table.render({
    elem: '#sysVolTable',
    page:  {limit:1},//指定分页
    data: [{
    "dataBase": "Scopus",
    "dataSum": "68560023",
    "dataClassify": "100000",
    "dataEmail": "100000",
    "startTime": "2017-12-25 9:31",
    "endTime": "2017-12-25 9:31",
    "remark":"测试数据"
},{
    "dataBase": "Wiley",
    "dataSum": "410015",
    "dataClassify": "20685",
    "dataEmail": "152030",
    "startTime": "2017-12-25 9:31",
    "endTime": "2017-12-25 9:31",
    "remark":"测试数据"
},
    {
    "dataBase": "EI",
    "dataSum": "410015",
    "dataClassify": "20685",
    "dataEmail": "152030",
    "startTime": "2017-12-25 9:31",
    "endTime": "2017-12-25 9:31",
    "remark":"测试数据"
}],
    cols: [[
          {title:'序号',templet:'#indexTp1', width:'6%'},
          {field:'dataBase', title:'数据源', width:'17%'},
          {field:'dataSum', title:'总数据量', width:'10%',sort:true},
          {field:'dataClassify', title:'总期刊数量', width:'17%'},
          {field:'dataEmail', title:'总邮箱数', width:'10%'},
          {field:'startTime', title:'开始时间', width:'11%'},
          {field:'endTime', title:'结束时间', width:'11%'},
          {field:'remark', title:'备注'}
        ]]
  });
});
