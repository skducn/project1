
$(document).ready(function() {


/* Tooltip */
new jBox('Mouse', {
  attach: '#Tooltip-1',
  position: {x: 'right', y: 'bottom'},
  content: '搜医院、获取医院数量、获取医院列表、获取医院详情'
});

new jBox('Mouse', {
  attach: '#Tooltip-2',
  position: {x: 'right', y: 'bottom'},
  content: '搜医院或医生(目标客户、非目标客户)、获取客户数量、获取客户列表、获取客户详情'
});

new jBox('Mouse', {
  attach: '#Tooltip-3',
  position: {x: 'right', y: 'bottom'},
  content: '拜访管理，创建拜访'
});

new jBox('Mouse', {
  attach: '#Tooltip-4',
  position: {x: 'right', y: 'bottom'},
  content: '协防管理，创建协防'
});

new jBox('Mouse', {
  attach: '#Tooltip-5',
  position: {x: 'right', y: 'bottom'},
  content: '搜索医院或申请人、获取会议数量，获取会议列表、获取会议详情'
});

new jBox('Mouse', {
  attach: '#Tooltip-6',
  position: {x: 'right', y: 'bottom'},
  content: '搜索医院或负责人、获取开发医院数量、获取产品开发详情'
});

new jBox('Mouse', {
  attach: '#Tooltip-7',
  position: {x: 'right', y: 'bottom'},
  content: '审批中心'
});

new jBox('Mouse', {
  attach: '#Tooltip-8',
  position: {x: 'right', y: 'bottom'},
  content: '工作计划'
});





/* Modal */


new jBox('Modal', {
  attach: '#Modal-1',
  height: 200,
  title: 'I\'m a basic jBox modal window',
  content: '<div style="line-height: 30px;">Try to scroll ...it\'s blocked.<br>Press [ESC] or click anywhere to close.</div>'
});


new jBox('Modal', {
  attach: '#Modal-2',
  width: 350,
  height: 200,
  blockScroll: false,
  animation: 'zoomIn',
  draggable: 'title',
  closeButton: true,
  content: 'You can move this modal window',
  title: 'Click here to drag me around',
  overlay: false,
  reposition: false,
  repositionOnOpen: false
});


new jBox('Modal', {
  attach: '#Modal-3',
  width: 450,
  height: 250,
  closeButton: 'title',
  animation: false,
  title: 'AJAX request',
  ajax: {
    url: 'https://ajaxresponse.com/2',
    data: {
      id: '1982',
      name: 'Stephan Wagner'
    },
    reload: 'strict',
    setContent: false,
    beforeSend: function() {
      this.setContent('');
      this.setTitle('<div class="ajax-sending">Sending AJAX request...</div>');
    },
    complete: function(response) {
      this.setTitle('<div class="ajax-complete">AJAX request complete</div>');
    },
    success: function(response) {
      this.setContent('<div class="ajax-success">Response:<tt>' + response + '</tt></div>');
    },
    error: function() {
      this.setContent('<div class="ajax-error">Oops, something went wrong</div>');
    }
  }
});


/* Confirm */


new jBox('Confirm', {
	content: 'Do you really want to do this?',
	cancelButton: 'Nope',
	confirmButton: 'Sure do!'
});


/* Notice */


$('#Notice-1').click(function() {
  
  new jBox('Notice', {
    content: 'Hello, I\'m a notice',
    color: 'black'
  });
  
});


$('#Notice-2').click(function() {
  
  new jBox('Notice', {
    animation: 'flip',
    color: getColor(),
    content: 'Oooh! They also come in colors'
  });
  
});


$('#Notice-3').click(function() {

  new jBox('Notice', {
    theme: 'NoticeFancy',
    attributes: {
      x: 'left',
      y: 'bottom'
    },
    color: getColor(),
    content: 'Hello, I\'m down here',
    audio: '../assets/audio/bling2',
    volume: 80,
    animation: {open: 'slide:bottom', close: 'slide:left'}
  });
  
});


$('#Notice-4').click(function() {
  
  new jBox('Notice', {
    attributes: {
      x: 'right',
      y: 'bottom'
    },
    stack: false,
    animation: {
      open: 'tada',
      close: 'zoomIn'
    },
    color: getColor(),
    title: 'Tadaaa! I\'m single',
    content: 'Open another notice, I won\'t stack'
  });
  
});

$('#Notice-5').click(function() {
  
  new jBox('Notice', {
    content: 'Hover me, I\'ll stick around',
    color: 'black',
    autoClose: Math.random() * 8000 + 2000,
    delayOnHover: true
  });
  
});


$('#Notice-6').click(function() {
  
  new jBox('Notice', {
    animation: 'flip',
    color: getColor(),
    autoClose: Math.random() * 8000 + 2000,
    content: 'Oooh! They also come in colors',
    delayOnHover: true,
    showCountdown: true,
    closeButton: true
  });
  
});


$('#Notice-7').click(function() {

  new jBox('Notice', {
    theme: 'NoticeFancy',
    attributes: {
      x: 'left',
      y: 'bottom'
    },
    color: getColor(),
    content: getString(),
    title: getTitle(),
    maxWidth: 600,
    audio: '../assets/audio/bling2',
    volume: 80,
    autoClose: Math.random() * 8000 + 2000,
    animation: {open: 'slide:bottom', close: 'slide:left'},
    delayOnHover: true,
    showCountdown: true,
    closeButton: true
  });
  
});


$('#Notice-8').click(function() {
  
  new jBox('Notice', {
    attributes: {
      x: 'right',
      y: 'bottom'
    },
    stack: false,
    animation: {
      open: 'tada',
      close: 'zoomIn'
    },
    autoClose: Math.random() * 8000 + 2000,
    color: getColor(),
    title: 'Tadaaa! I\'m single',
    content: 'Open another notice, I won\'t stack',
    delayOnHover: true,
    showCountdown: true,
    closeButton: true
  });
  
});


/* Image */


new jBox('Image', {
  imageCounter: true,
  imageCounterSeparator: ' of '
});


/* Additional JS for demo purposes  */

$('.target-notice').click(function() {
  $(this).addClass('active').html('Click me again');
}).mouseleave(function() {
  $(this).removeClass('active').html('Click me');
});

var colors = ['red', 'green', 'blue', 'yellow'], index = 0;
var getColor = function () {
  (index >= colors.length) && (index = 0);
  return colors[index++];
};

var strings = ['Short', 'You just switched the internet off', 'Please do not click too hard - next time we\'ll notify google.', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.'];
var getString = function () {
  return strings[Math.floor(Math.random()*strings.length)];
};

var titles = ['Congrats', 'Success', 'Thank you', false, false, false];
var getTitle = function () {
  return titles[Math.floor(Math.random()*strings.length)];
};


});

