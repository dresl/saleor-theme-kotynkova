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
  });
  $(document).mouseup(function(e){
    var container = $(".main-menu li.dropdown");
    if (!container.is(e.target) && container.has(e.target).length === 0) 
    {
        $("#nav-icon1").removeClass('open');
    }
  });
});
