<!-- mask -->

document.addEventListener('DOMContentLoaded', function() {

var form = document.querySelector('form');
var loading = document.getElementById('loading');
form.addEventListener('submit', function(event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function() {
    form.submit(); // 模拟提交表单
    }, 1000);
});

// 测试 遮罩

var form1 = document.getElementById('mask_testRule');
var loading = document.getElementById('loading');
form1.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        form1.submit(); // 模拟提交表单
    }, 1000);
});

// 检索记录 遮罩

var form2 = document.getElementById('mask_searchRecord');
var loading = document.getElementById('loading');
form2.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        form2.submit(); // 模拟提交表单
    }, 1000);
});

// 导入用例 遮罩

var form3 = document.getElementById('mask_importCase');
var loading = document.getElementById('loading');
form3.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        form3.submit(); // 模拟提交表单
    }, 1000);
});

// 创建xx规则表,步骤1/2 遮罩

var form4 = document.getElementById('mask_registerTbl1');
var loading = document.getElementById('loading');
form4.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        form4.submit(); // 模拟提交表单
    }, 1000);
});
// 创建xx规则表,步骤2/2 遮罩
var form42 = document.getElementById('mask_registerTbl2');
var loading = document.getElementById('loading');
form42.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        form42.submit(); // 模拟提交表单
    }, 1000);
});

// 查看日志 遮罩

var form5 = document.getElementById('mask_searchLog');
var loading = document.getElementById('loading');
form5.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        form5.submit(); // 模拟提交表单
    }, 1000);
});

});