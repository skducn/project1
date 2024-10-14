
$(document).ready(function() {

    <!-- 1 查询规则集 -->

    $('#queryRuleCollection').change(function() {
    var selectedValue = $(this).val();
    $.ajax({
    url: '/get_queryRuleCollection',
    type: 'GET',
    data: {'value': selectedValue},
    success: function(data) {
    var textWithNewLines = data.text.replace(/\n/g, "<br>");
    // var textWithNewLines = data.text;
    $('#get_queryRuleCollection').html(textWithNewLines);
    // {#alert(textWithNewLines);#}
    },
    error: function(error) {
    console.error('Error fetching data: ', error);
    }
    });
    });

    <!-- 1 查询规则集 - 规则名与规则集及联 -->

    $('#queryRuleName').change(function() {
    var selectedValue = $(this).val();
    $.ajax({
    url: "/get_queryRuleName",
    type: 'GET',
    data: {'value': selectedValue},
    success: function(response) {
    var queryRuleCollection=document.getElementById("queryRuleCollection");
    for (var i = 1; i < queryRuleCollection.options.length;) {
    queryRuleCollection.removeChild(queryRuleCollection.options[i]);
    }
    for (var i = 0; i < response.length; i++) {
    $("#queryRuleCollection").append("<option>" + response[i] + "</option>");
    }
    },
    error: function(xhr, status, error) {
    console.log(xhr.responseText);
    }
    });
    });

    <!-- edit123，查询sql -->

    $("#queryRecord").click(function() {
    // 获取输入框的内容
    var querySql = $("#querySql").val();
    $.ajax({
    url: "/get_queryRecord",
    type: "POST",
    data: {querySql: querySql},
    success: function(response) {
    alert(response);
    },
    error: function(xhr, status, error) {
    console.log(xhr.responseText);
    }
    });
    });

    <!-- 查询错误规则的记录 -->

    // $(document).ready(function() {
    // $('#queryErrorRuleId').change(function() {
    // var selectedValue = $(this).val();
    // $.ajax({
    // url: '/get_queryErrorRuleId',
    // type: 'GET',
    // data: {'value': selectedValue},
    // success: function(data) {
    // // {#alert(data)#}
    // // {#$('#data_container').text(data.tmp);#}
    // var textWithNewLines = data.text.replace(/\n/g, "<br/>");
    // $('#get_queryErrorRuleId').html(textWithNewLines);
    // },
    // error: function(error) {
    // console.error('Error fetching data: ', error);
    // }
    // });
    // });
    // });


    <!-- 查询规则结果 -->

    // $("#queryRuleResult").click(function() {
    // var ruleName = $("#ruleName").val();
    // var id = $("#id").val();
    // $.ajax({
    // url: "/get_queryRuleResult",
    // type: "POST",
    // data: {ruleName: ruleName, id:id},
    // success: function(response) {
    // alert(response);
    // },
    // error: function(xhr, status, error) {
    // console.log(xhr.responseText);
    // }
    // });
    // });


    <!--  index5 查询表结构 -->

    $('#queryDesc2').change(function() {
    $('#mask').show(); // 显示遮罩层
    var selectedValue = $(this).val();
    $.ajax({
    url: '/get_queryDesc2',
    type: 'GET',
    data: {'value': selectedValue},
    success: function(data) {
        var test = document.getElementById('test');
        var divObj33 = document.getElementById("test3");
        if (divObj33!=null){
            divObj33.remove();
        }
        var divObj22 = document.getElementById("test2");
        if (divObj22!=null){
            divObj22.remove();
        }
        var divObj11 = document.getElementById("test1");
        if (divObj11!=null){
            divObj11.remove();
        }

        let divObj1 = document.createElement("div");
            divObj1.className = 'a6 a1K ac';
            divObj1.id = "test1"
        test.appendChild(divObj1);
        let divObj2 = document.createElement("div");
            divObj2.className = 'a5 md:a2u/2 af';
            divObj1.id = "test2"
            divObj1.appendChild(divObj2);
        let divObj3 = document.createElement("div");
            divObj3.className = 'a3u';
            divObj1.id = "test3"
            divObj2.appendChild(divObj3);

        for (let key in data){
            let divObj = document.createElement("div");
            divObj.id = key;
            divObj.innerHTML = key;
            divObj3.appendChild(divObj);
            $(document).ready(function() {
                new jBox('Modal', {
                attach: '#' + key,
                height: 600,
                title: key,
                content: '<div style="line-height: 30px;">' +
                data[key] + '<br></div>'
                });
                })
        }

    $('#mask').hide(); // 显示遮罩层
    },
    error: function(error) {
    console.error('Error fetching data: ', error);
    }
    });
    });


});