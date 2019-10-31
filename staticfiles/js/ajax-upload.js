$(function () {
    $(".js-upload-photos").click(function () {
      $("#id_image").click();
    });

    $("#id_image").fileupload({
      dataType: 'json',
      sequentialUploads: true,
      start: function (e) {
        $("#uploadProgressBar").modal("show");
      },
      stop: function (e) {
        $("#uploadProgressBar").modal("hide");
      },
      progressall: function (e, data) {
        var progress = parseInt(data.loaded / data.total * 100, 10);
        var strProgress = progress + "%";
        $(".progress-bar").css({"width": strProgress});
        $(".progress-bar").text(strProgress);
      },
      done: function (e, data) {
        if (data.result.is_valid) {
          $('tbody.images').prepend(
            "<tr><td>"+ data.result.url +"</td></tr>"
          )
        } else {
            if (data.result.limit_exceeded) {
              $("#error-alert").click();
            }
            $('tbody.images').prepend(
              "<tr><td class='red-500'>Invalid data</td></tr>"
            )
        }
      }
    });
});