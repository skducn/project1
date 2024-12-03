//<!-- 返回首页 -->

function goBack() {
window.history.back(); // 或者使用 window.history.go(-1)
return false; // 阻止表单提交
}
function goHome() {window.location.href = '/';}

//<!-- 重构alert -->

function alert(e){
$("body").append('<div id="msg">' +
    '<div class="box" >' +
    '<div id="msg_top">信息<span class="msg_close">×</span></div>' +
    '<div id="msg_cont">'+e+'</div>' +
    '<div class="msg_close" id="msg_clear">关闭</div>' +
    '</div>'+
    '</div>');
$(".msg_close").click(function (){
    $("#msg").remove();
});
};

//<!-- loading加载中 -->

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
});