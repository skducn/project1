<!-- mask  遮罩 -->

document.addEventListener('DOMContentLoaded', function() {
var loading = document.getElementById('loading');


// erp - 今日团队排名
var mask51 = document.getElementById('mask71');
// var loading = document.getElementById('loading');
mask51.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        mask51.submit(); // 模拟提交表单
    }, 1000);
});


//
var mask62 = document.getElementById('mask72');
// var loading = document.getElementById('loading');
mask62.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        mask62.submit(); // 模拟提交表单
    }, 1000);
});

});