(function($) {
  "use strict";
  $(document).ready(function() {
    var overlay_set = false;
    $('.calltoaction-portlet-wrapper').each( function() {
      var time_on_site;
      var cookie_value;
      var el;
      var cookiename;
      var start;
      var timeout;
      if (overlay_set) {
        return;
      }
      // Check if the user has already seen this overlay.
      cookiename = $(this).attr('data-cookiename');
      // Note: readCookie and createCookie are defined in
      // Products/CMFPlone/skins/plone_ecmascript/cookie_functions.js
      cookie_value = readCookie(cookiename);
      if (cookie_value === 'y') {
        // already seen
        return;
      }
      timeout = parseInt($(this).attr('data-timeout'));
      if (isNaN(timeout)) {
        timeout = 5000;
      }
      cookie_value = parseInt(cookie_value);
      start = cookie_value;
      if (isNaN(start)) {
        start = new Date().getTime();
      } else {
        /*
         Say start is 12:00 (but then in milliseconds).
         And current time is 12:02.
         And timeout is 3 minutes.
         Then the new timeout is 1 minute.
         */
        time_on_site = new Date().getTime() - start;
        if (time_on_site > 3600000) {
          // Reset time on site after an hour.
          start = new Date().getTime();
          time_on_site = 0;
        }
        timeout = timeout - time_on_site;
      }
      if (cookie_value !== start) {
        // Remember the session start time in a cookie.
        createCookie(cookiename, start, 365);
      }
      el = $(this);
      setTimeout(
        function(){
          // Overlay adapted from http://jquerytools.github.io/demos/overlay/trigger.html
          el.overlay({
            // custom top position
            top: "center",
            fixed: true,
            // Before the overlay is gone be active place it correctly
            onBeforeLoad: function() {

              if (el.hasClass("manager_right")){
                el.animate({right: -1000});
              }else{
                el.animate({left: -1000});
              }

            },
            // when the overlay is opened, animate our portlet
            onLoad: function() {

              if (el.hasClass("manager_right")){
                 el.animate({right: 15});
              }
              else {
                  el.animate({left: 15});
              }

            },
            // some mask tweaks suitable for facebox-looking dialogs
            mask: {
              // you might also consider a "transparent" color for the mask
              color: '#fff',
              // load mask a little faster
              loadSpeed: 200,
              // very transparent
              opacity: 0.5
            },
            // disable this for modal dialog-type of overlays
            closeOnClick: true,
            // load it immediately after the construction
            load: true

          });

          /*
           Set cookie to avoid showing overlay twice to the same
           user.  We could do this on certain events, but you have
           to catch them all: onClose of the overlay, clicking on
           a link in the overlay, etcetera.  Much easier to simply
           set the cookie at the moment we show the overlay.
           The 'y' value means: yes, the user has seen it.
           */
          createCookie(cookiename, 'y', 365);
        },
        timeout);
      // We setup only one overlay, otherwise it gets a bit crazy.
      overlay_set = true;
    });
  });
})(jQuery);
