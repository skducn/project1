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

var form2 = document.getElementById('mask3');
var loading = document.getElementById('loading');
form2.addEventListener('submit', function (event) {
    event.preventDefault(); // 阻止表单默认提交行为
    $('#mask').show(); // 显示遮罩层
    loading.style.display = 'block'; // 显示加载动画
    setTimeout(function () {
        form2.submit(); // 模拟提交表单
    }, 1000);
});

});