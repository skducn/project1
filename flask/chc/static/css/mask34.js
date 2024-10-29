<!-- mask  遮罩 -->

document.addEventListener('DOMContentLoaded', function() {
var loading = document.getElementById('loading');

// 规则集 - 新建/修改
var mask32 = document.getElementById('mask32');
// var loading = document.getElementById('loading');
mask32.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        mask32.submit(); // 模拟提交表单
    }, 1000);
});

// 调式 - 测试规则 - 执行
var mask41 = document.getElementById('mask41');
// var loading = document.getElementById('loading');
mask41.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        mask41.submit(); // 模拟提交表单
    }, 1000);
});

// 调式 - 测试规则 - 编辑
var mask42 = document.getElementById('mask42');
// var loading = document.getElementById('loading');
mask42.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        mask42.submit(); // 模拟提交表单
    }, 1000);
});













});