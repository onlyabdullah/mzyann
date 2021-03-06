(function(document, window, $) {
  (function() {
    var defaults = Plugin.getDefaults("wizard");
    var options = $.extend(true, {}, defaults, {
      onInit: function() {
        $('#professionalCreationForm').formValidation({
          framework: 'bootstrap',
          fields: {
            first_name: {
              validators: {
                notEmpty: {
                  message: 'The first name is required'
                },
                min: 3,
                max: 30
              }
            },
            last_name: {
              validators: {
                notEmpty: {
                  message: 'The last name is required'
                },
                min: 3,
                max: 150
              }
            },
            birthday: {
              validators: {
                notEmpty: {
                  message: 'The birthday is required'
                },
                date: {
                  format: 'YYYY-MM-DD'
                }
              }
            },
            email: {
              validators: {
                notEmpty: {
                  message: 'The email is required'
                }
              }
            },
            password1: {
              validators: {
                min: 8,
                different: {
                  field: 'email',
                  message: 'The password cannot be the same as email'
                }
              }
            },
            password2: {
              validators: {
                identical: {
                  field: 'password1',
                  message: 'They are not identical'
                }
              }
            },
            profile_picture: {
              validators: {
                notEmpty: {
                  message: 'The Profile Picture is required'
                },
                file: {
                  extension: 'jpeg,jpg,png',
                  type: 'image/jpeg,image/png',
                  maxSize: 2097152,   // 2048 * 1024
                  message: 'The selected file is not valid'
                }
              }
            },
            job: {
              validators: {
                notEmpty: {
                  message: 'Job is required'
                }
              }
            },
            area: {
              validators: {
                notEmpty: {
                  message: 'Area is required'
                }
              }
            },
            phone: {
              validators: {
                notEmpty: {
                  message: 'Phone number is required'
                }
              }
            },
            about: {
              validators: {
                notEmpty: {
                  message: 'about is required'
                }
              }
            },
            image_0: {
              validators: {
                notEmpty: {
                  message: 'Job is required'
                }
              }
            },
            image_1: {
              validators: {
                notEmpty: {
                  message: 'Job is required'
                }
              }
            },
            image_3: {
              validators: {
                notEmpty: {
                  message: 'Job is required'
                }
              }
            },
            image_4: {
              validators: {
                notEmpty: {
                  message: 'Job is required'
                }
              }
            },
            image_5: {
              validators: {
                notEmpty: {
                  message: 'Job is required'
                }
              }
            }
          },
          err: {
            clazz: 'text-help'
          },
          row: {
            invalid: 'has-danger'
          }
        });
      },
      validator: function() {
        var fv = $('#professionalCreationForm').data('formValidation');


        var $this = $(this);

        // Validate the container
        fv.validateContainer($this);

        var isValidStep = fv.isValidContainer($this);
        if (isValidStep === false || isValidStep === null) {
          return false;
        }

        return true;
      },
      onFinish: function() {
        $('#professionalCreationForm').submit();
      },
      templates: {
        buttons: function() {
          var options = this.options;
          var html = '<div class="wizard-buttons">' +
            '<a class="btn btn-default bg-grey-700 btn-outline waves-effect pull-xs-left white" href="#' + this.id + '" data-wizard="back" role="button">Back</a>' +
            '<button type="submit" class="btn btn-success btn-outline pull-xs-right waves-effect white" data-wizard="finish" role="button">Finish</button>' +
            '<a class="btn btn-primary btn-outline pull-xs-right waves-effect white" href="#' + this.id + '" data-wizard="next" role="button">Next</a>' +
            '</div>';
          return html;
        }
      },
      buttonsAppendTo: '#professionalCreationForm'
    });

    $("#professionalCreationFormContainer").wizard(options);
  })();
})(document, window, jQuery);
