(function(document, window, $) {
  'use strict';

  // Images Upload
  // -------------------
  $('a.select').on('click', function() {
    $(this).prev('input.img-input').click();
    $.uploadPreview({
      input_field: $(this).prev('input.img-input'),
      preview_box: $(this).find('.preview-panel'),
      no_label: true
    });
  }).mouseover(function() {
    $(this).find('.md-edit').removeClass('white');    
    $(this).find('.md-edit').addClass('indigo-500');
  }).mouseout(function() {
    $(this).find('.md-edit').removeClass('indigo-500');    
    $(this).find('.md-edit').addClass('white');
  });

  $('input.img-input').on('change', function() {
    const previewPanel = $(this).next('.select').find('.preview-panel');
    const profilePicPreview = $(this).next('.select').find('.profile-pic');

    if ($(this).val()){
      previewPanel.css('border-style', 'none');
      previewPanel.find('.md-plus').css('display', 'none');
      previewPanel.find('.md-edit').css('display', '');
    } else {
      previewPanel.css('background-image', 'none');
      previewPanel.css('border-style', 'solid');
      previewPanel.find('.md-plus').css('display', '');
      previewPanel.find('.md-edit').css('display', 'none');
      profilePicPreview.removeAttr('style');
    }
  });

})(document, window, jQuery);