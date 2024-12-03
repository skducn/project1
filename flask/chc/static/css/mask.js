<!-- mask  遮罩 -->

document.addEventListener('DOMContentLoaded', function() {
var loading = document.getElementById('loading');


// 数据源 - 创建库表 步骤1/2
var mask21 = document.getElementById('mask21');
// var loading = document.getElementById('loading');
mask21.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        mask21.submit(); // 模拟提交表单
    }, 1000);
});


// 数据源 - 创建库表 步骤2/2
var mask211 = document.getElementById('mask211');
// var loading = document.getElementById('loading');
mask211.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        mask211.submit(); // 模拟提交表单
    }, 1000);
});


// 数据源 - 导入规则
var mask22 = document.getElementById('mask22');
// var loading = document.getElementById('loading');
mask22.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        mask22.submit(); // 模拟提交表单
    }, 1000);
});








});