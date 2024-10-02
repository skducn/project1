
$(document).ready(function() {

    <!-- 1，查询错误规则的记录 -->

$(document).ready(function() {
    $('#queryErrorRuleId').change(function() {
        var selectedValue = $(this).val();
        $.ajax({
            url: '/get_queryErrorRuleId',
            type: 'GET',
            data: {'value': selectedValue},
            success: function(data) {
                // {#alert(data)#}
                // {#$('#data_container').text(data.tmp);#}
                var textWithNewLines = data.text.replace(/\n/g, "<br/>");
                $('#get_queryErrorRuleId').html(textWithNewLines);
            },
            error: function(error) {
                console.error('Error fetching data: ', error);
            }
        });
    });
});


    <!-- 2，查询规则结果 -->

$("#queryRuleResult").click(function() {
    var ruleName = $("#ruleName").val();
    var id = $("#id").val();
    $.ajax({
        url: "/get_queryRuleResult",
        type: "POST",
        data: {ruleName: ruleName, id:id},
        success: function(response) {
            alert(response);
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});


    <!-- 4，查询sql -->

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


    <!-- 5 查询规则集 -->


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


});