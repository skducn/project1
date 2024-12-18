
$(document).ready(function() {

    <!-- 3 规则集 - 查询 - 规则集（与规则名及联）-->

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

    <!-- 3 规则集 - 查询 - 规则名（与规则集及联） -->

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


    <!-- 4 调式 - 测试规则 - 规则集（与规则名及联）-->

    $('#queryRuleCollection2').change(function() {
    var selectedValue = $(this).val();
    $.ajax({
    url: '/get_queryRuleCollection',
    type: 'GET',
    data: {'value': selectedValue},
    success: function(data) {
    var textWithNewLines = data.text.replace(/\n/g, "<br>");
    // var textWithNewLines = data.text;
    $('#get_queryRuleCollection2').html(textWithNewLines);
    // {#alert(textWithNewLines);#}
    },
    error: function(error) {
    console.error('Error fetching data: ', error);
    }
    });
    });

    <!-- 4 调式 - 测试规则 - 规则名（与规则集及联）-->

    $('#queryRuleName2').change(function() {
    var selectedValue = $(this).val();
    $.ajax({
    url: "/get_queryRuleName",
    type: 'GET',
    data: {'value': selectedValue},
    success: function(response) {
    var queryRuleCollection2=document.getElementById("queryRuleCollection2");
    for (var i = 1; i < queryRuleCollection2.options.length;) {
    queryRuleCollection2.removeChild(queryRuleCollection2.options[i]);
    }
    for (var i = 0; i < response.length; i++) {
    $("#queryRuleCollection2").append("<option>" + response[i] + "</option>");
    }
    },
    error: function(xhr, status, error) {
    console.log(xhr.responseText);
    }
    });
    });

    <!-- 4 调试 - 查询sql -->

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


    <!--  5 辅助工具 - 查询表结构 -->

    $('#queryDesc2').change(function() {
    $('#mask').show(); // 显示遮罩层
    var selectedValue = $(this).val();
    $.ajax({
    url: '/get_queryDesc2',
    type: 'GET',
    data: {'value': selectedValue},
    success: function(response) {
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
            // divObj1.id = "test1"
        test.appendChild(divObj1);
        let divObj2 = document.createElement("div");
            divObj2.className = 'a5 md:a2u/2 af';
            // divObj1.id = "test2"
            divObj1.appendChild(divObj2);
        let divObj3 = document.createElement("div");
            divObj3.className = 'a3u';
            divObj3.id = "test3"
            divObj3.style = "line-height: 16px;"
            divObj2.appendChild(divObj3);

        for (let key in response){
            if (key != 'tblComment') {
                let trObj = document.createElement("tr");
                let tdObj = document.createElement("td");
                let tdObj2 = document.createElement("td");
                divObj3.appendChild(trObj)
                trObj.appendChild(tdObj)
                trObj.appendChild(tdObj2)
                let divObj = document.createElement("div");
                let divObj2 = document.createElement("div");
                let tblComment
                varComment = response['tblComment'][key]
                tblComment = key + "（" + varComment + "）"
                divObj.id = key;
                divObj.innerHTML = key;
                divObj2.innerHTML = varComment;
                tdObj.appendChild(divObj);
                tdObj2.appendChild(divObj2);

                //将文本内容格式化成表格
                let l_tr = response[key].split("<br>")
                let td_1 = '';
                let tr_1 = '';
                for (let i = 0; i < l_tr.length; i++) {
                    let l_td = l_tr[i].split(",")
                    for (let j = 0; j < l_td.length; j++) {
                        td_1 = td_1 + '<td><div style="line-height: 16px;">' + l_td[j] + '</div></td>'
                    }
                    tr_1 = tr_1 + '<tr>' + td_1 + '</tr>'
                    td_1 = ''
                }
                tr_1 = '<table class="tftable"><tbody>' + tr_1 + '</tbody></table>'

                $(document).ready(function () {
                    new jBox('Modal', {
                        attach: '#' + key,
                        height: 600,
                        title: tblComment,
                        content: tr_1
                            // '<tr><td><div style="line-height: 31px;">' + response[key] + '</div></td></tr>'
                    });
                })
            }
        }

    $('#mask').hide(); // 显示遮罩层
    },
    error: function(error) {
    console.error('Error fetching data: ', error);
    }
    });
    });


});