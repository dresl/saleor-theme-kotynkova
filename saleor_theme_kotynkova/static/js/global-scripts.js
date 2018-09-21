jQuery(function($) {
  $(function() {
    $(document).on("click", "a.open-modal", function () {
      var url = $(this).attr('href');
      var modal = $('#modal-container');
      $.ajax({
        url: url,
      }).done(function(response) {
        modal.html(response);
        modal.modal('show');
      });
      event.preventDefault();
    });
  });
});
jQuery(function($) {
    setTimeout(function(){
      $(".carousel").swipe({
        swipe: function(event, direction, distance, duration, fingerCount, fingerData) {
          if (direction == 'left') $(this).carousel('next');
          if (direction == 'right') $(this).carousel('prev');
        },
      });
    }, 1000);
  
  $(function(){
    $('.main-menu li.dropdown a.dropdown-toggle').click(function() {
      $("#nav-icon1").toggleClass('open');
    });
    $(".main-menu ul.dropdown-menu").append("<div class='dropdown-divider show-on-mobile'></div>");
    $(".main-menu > .language-menu").clone().appendTo($(".main-menu ul.dropdown-menu")).addClass("show-on-mobile");
    $(".main-menu #nav-icon1").click(function(){
      setTimeout(function(){
      if ($(".main-menu #nav-icon1").hasClass("open")) {
          $(".menu-burger > .dropdown-menu").addClass("show");
          } else {
      $(".menu-burger > .dropdown-menu").removeClass("show");
      }
      }, 5);
          });
      $(".main-menu .language-menu > div > a").click(function(){
        $(this).toggleClass("open");
        setTimeout(function(){
        if ($(".main-menu .language-menu > div > a").hasClass("open")) {
            $(".main-menu .language-menu .language-picker > .dropdown-menu").addClass("show");
            } else {
        $(".main-menu .language-menu .language-picker > .dropdown-menu").removeClass("show");
        }
        }, 5);
      });
  });
  $(document).mouseup(function(e){
    var container = $(".main-menu li.dropdown");
    if (!container.is(e.target) && container.has(e.target).length === 0) 
    {
        $(".main-menu #nav-icon1").removeClass('open');
        $(".menu-burger > .dropdown-menu").removeClass("show");
        $(".main-menu .language-menu .language-picker > .dropdown-menu").removeClass("show");
    }
  });
});
