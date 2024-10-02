/* -------------------------------------------------------------------
 * Plugin Name           : Laus - Dropdown & Hamburger Menu
 * Author Name           : Yucel Yilmaz
 * Author URI            : https://codecanyon.net/user/aip_theme3434
 * Created Date          : 18 January 2020
 * Version               : 1.0.1
 * File Name             : main.js
------------------------------------------------------------------- */

/* -------------------------------------------------------------------
 [Table of contents]
 * 01.Navbar
 * 02.Copyright
 * 03.ScrollIt
 * 04.Contact Form
 * 05.Sign Up & Login Popup
*/

(function ($) {
  "use strict";

    // Call all ready functions
    laus_navbar(),
    laus_copyright(),
    laus_scrollIt(),
    laus_contactForm(),
    laus_formPopup();
    
})(window.jQuery);

/* ------------------------------------------------------------------- */
/* 01.Navbar
/* ------------------------------------------------------------------- */
function laus_navbar() {
    "use-strict";

    // Variables
    var header              = $('.header'),
        navbarLink          = $('.menu-link'),
        logoTransparent     = $(".logo-transparent"),
        logoNormal          = $(".logo-normal");

    // When Window On Scroll
    $(window).on('scroll',function(){
        let scrollTop       = $(this).scrollTop();

        if(scrollTop > 100 ) {
            header.addClass('header-shrink');
            logoTransparent.hide();
            logoNormal.show();
        }else {
            header.removeClass('header-shrink');
            logoTransparent.show();
            logoNormal.hide();
        }
    });
    navbarLink.on('click', function(){
        $('.navbar-collapse').collapse('hide');
        $("#signup-form, #login-form").fadeOut();
    }); 

    $(".navbar-toggler").on("click",function(){
        $("#signup-form, #login-form").fadeOut();
    });

    // Scroll Spy
    $('body').scrollspy({
        target: '#fixedNavbar',
        offset: 95
    });
    
    // DropDown
    var $dropdown = $(".dropdown");
    var $dropdownToggle = $(".dropdown-toggle");
    var $dropdownMenu = $(".dropdown-menu");
    var  showClass = "show";
     
    $(window).on("load resize", function() {
      if (this.matchMedia("(min-width: 992px)").matches) {
        $dropdown.hover(
          function() {
            const $this = $(this);
            $this.addClass(showClass);
            $this.find($dropdownToggle).attr("aria-expanded", "true");
            $this.find($dropdownMenu).addClass(showClass);
          },
          function() {
            const $this = $(this);
            $this.removeClass(showClass);
            $this.find($dropdownToggle).attr("aria-expanded", "false");
            $this.find($dropdownMenu).removeClass(showClass);
          }
        );
      } else {
        $dropdown.off("mouseenter mouseleave");
      }
    });
}
/* ------------------------------------------------------------------- */
/* 02.Copyright
/* ------------------------------------------------------------------- */
function laus_copyright() {
    "use-strict";

    // Variables
    var fullYearCopyright       = $('#fullYearCopyright'),
        getFullYearDate         = new Date().getFullYear();

    fullYearCopyright.text(getFullYearDate);
}   
/* ------------------------------------------------------------------- */
/* 03.ScrollIt
/* ------------------------------------------------------------------- */
function laus_scrollIt() {
    "use-strict";
        
    $.scrollIt({
        upKey: 38,
        downKey: 40,
        easing: "swing",
        scrollTime: 600,
        activeClass: "active",
        onPageChange: null,
        topOffset: -15
    });
}

/* ------------------------------------------------------------------- */
/* 04.Contact Form
/* ------------------------------------------------------------------- */
function laus_contactForm(){
  "use-scrict";

 
  $("#contactBtn").on("click",function(event) {
      event.preventDefault();

      // E-Mail Validation Function 
      function validateEmail(email) {
          var regexp = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return regexp.test(String(email).toLowerCase());
      }

      // Contact Form Input Value 
      var name            = $("#contactName").val().trim(),
          email           = $("#contactEmail").val().trim(),
          subject         = $("#contactSubject").val().trim(),
          message         = $("#contactMessage").val().trim(),
          validateEmail   = validateEmail(email);

      // Check empty fields
      if(name===''||email===''||message===''||subject===''){
          $('div.empty-form').stop().slideDown(500).delay(2000).slideUp(500);
      }else if (!validateEmail===true) {
          $('div.email-invalid').stop().slideDown(500).delay(2000).slideUp(500);
      }else {
          // Once the information entered is verified, the mail form is sent. 
          $.post("send_mail.php",
              {
                  contact_name:name,
                  contact_email:email,
                  contact_subject:subject,
                  contact_message:message
              },
              function(response) {
                  $("#contactForm")[0].reset();   
                  $(".success-form").stop().html(response).slideDown(500).delay(5000).slideUp(500);  
              }
          );
      }
  });
}

/* ------------------------------------------------------------------- */
/* 05.Sign Up & Login Popup
/* ------------------------------------------------------------------- */
function laus_formPopup(){
    "use-scrict";

    $('#sign-up-close-btn').on("click",function(event){
        event.preventDefault();
        $("#signup-form").fadeOut();
    });

    $('#login-close-btn').on("click",function(event){
        event.preventDefault();
        $("#login-form").fadeOut();
    });

    $(".signup-btn-toggle").on("click",function(event){
        event.preventDefault();
        $("#signup-form").fadeIn();
        $("#login-form").fadeOut();
    });

    $(".login-btn-toggle").on("click",function(event){
        event.preventDefault();
        $("#login-form").fadeIn();
        $("#signup-form").fadeOut();
    });
}


