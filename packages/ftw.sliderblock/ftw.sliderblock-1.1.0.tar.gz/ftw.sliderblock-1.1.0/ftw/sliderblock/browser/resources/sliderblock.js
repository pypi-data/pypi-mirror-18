(function(global, $) {

  "use strict";

  $(function() {

    var sliders = {
      sliders: {},
      init: function() {
        var self = this;
        $(".sliderWrapper").each(function() {
          self.sliders[this.id] = new global.Slider($(".sliderPanes", this), $(this).data("settings"));
        });
      },
      update: function() {
        var self = this;
        $(".sliderWrapper > :not(.slick-initialized)").each(function() {

          var sliderPane = $(this);
          var sliderId = sliderPane.parent().attr("id");

          if (sliderId in self.sliders) {
            self.sliders[sliderId].update(sliderPane, sliderPane.parent().data("settings"));
          } else {
            self.sliders[sliderId] = new global.Slider(sliderPane, sliderPane.data("settings"));
          }

        });
      }
    };

    sliders.init();

    $(document).on("blockContentReplaced", function() { sliders.update(); });

    $(document).on("sortstop", ".sl-column", function() { sliders.update(); });

  });

}(window, jQuery));
