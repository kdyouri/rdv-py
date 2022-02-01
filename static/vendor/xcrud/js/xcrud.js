DIALOG = '<div class="modal fade xcrud-modal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1">' +
        '<div class="modal-dialog">' +
            '<div class="modal-content" style="position:relative">' +
                '<div class="modal-header">' +
                    '<h5 class="modal-title">Opération en cours...</h5>' +
                    '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>' +
                '</div>' +
                '<div class="modal-body">' +
                    '<div class="d-flex justify-content-center">' +
                        '<div class="spinner-border" role="status">' +
                            '<span class="visually-hidden">Téléchargement...</span>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="modal-footer">' +
                    '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Annuler</button>' +
                '</div>' +
            '</div>' +
        '</div>' +
    '</div>';

SPINER = '<div style="position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(255,255,255,.5)"></div>'+
    '<div class="spinner-border" style="position:absolute;top:50%;left:50%;margin:-20px"></div>';

$(document).on('click', '.xcrud-btn-edit,.xcrud-btn-add,.xcrud-btn-dialog', function(e){
    e.preventDefault();
    var $main = Xcrud.getMainContainer(this);
    var url = $(this).attr('href');
    var width = $(this).data('width') || '';
    var callback = $(this).data('callback') || '';
    Xcrud.showDialog($main, {'url' : url, 'width' : width, 'callback' : callback})
});

$(document).on('submit', '.xcrud-modal form', function(e) {
    e.preventDefault();

    var $dialog = $(this).closest('.modal');
    var $main = $dialog.data('xcrudmain');
    var updatecontent = $(this).data('updatecontent') || '';

    $.ajax({
        url: $(this).attr('action'),
        method: 'POST',
        data: new FormData(this),
        beforeSend: function(){
            $dialog.find('.modal-content').append(SPINER);
        },
        success: function(resp){
            if ($(resp).is('.modal-dialog:not(.xcrud-main)')){
                $dialog.html(resp);

                if ($dialog.find('.error-message').length) {
                    // Le temps de voir le Flash ".alert-danger":
                    window.setTimeout(function(){
                        // Défiler vers le premier élement contenant une erreur:
                        let $firstErrorInput = $dialog.find('.error-message').first().closest('.input');
                        let scrollY = $firstErrorInput.position().top;

                        $dialog.find('.modal-body').animate({scrollTop: scrollY}, 700);
                    }, 800);
                } else {
                    $dialog.find('input[type=text],input[type=number],input[type=email],textarea,select').not('[disabled]').not('[readonly]').first().focus();
                }
                $dialog.trigger('content.loaded');
            } else {
                $dialog.trigger('content.updated', [resp]);
                if(updatecontent){
                    $dialog.modal('hide');
                }else{
                    $dialog.modal('hide').on('hidden.bs.modal', function(){
                        Xcrud.updateMainContent($main, resp);
                    });
                }
            }
        },
        error: function(jqxhr){
            alert('Error has occurs!');
        },
        complete: function(){
            
        },
        contentType: false,
        processData: false
    });
});

$(document).on('click', '.xcrud-btn-delete,.xcrud-btn-action', function(e){
    e.preventDefault();

    var msg = $(this).data('msg');
    var url = $(this).attr('href');
    var $main = Xcrud.getMainContainer(this);

    var proceed = function(){
        $.ajax({
            url: url,
            beforeSend: function(){
                
            },
            success: function(resp){
                Xcrud.updateMainContent($main, resp);
            },
            error: function(jqxhr){
                alert('Error has occurs!');
            },
            complete: function(){
                
            }
        });
    };

    if (msg) {
        bootbox.confirm({
            message: msg,
            title: 'Confirmation',
            callback: function(result) {
                if (result)  proceed.call();
            }
        });
    } else {
        proceed();
    }
});

$(document).on('click', '.xcrud-paginate>li>a,.xcrud-sort>a', function(e){
    e.preventDefault();

    var $main = Xcrud.getMainContainer(this);

    $.ajax({
        url: $(this).attr('href'),
        beforeSend: function(){
            
        },
        success: function(resp){
            Xcrud.updateMainContent($main, resp);
            $('html,body').scrollTop(0);
        },
        error: function(jqxhr){
            alert('Error has occurs!');
        },
        complete: function(){
            
        }
    });
});

var Xcrud = {
    getMainContainer: function(child) {
        // If it's a dropdown menu:
        if ($(child).closest('.dropdown-menu').length) {
            let $dropdownMenu = $(child).closest('.dropdown-menu');

            // The menu item could be outside the main container:
            if ($dropdownMenu.parent().is('body')) {
                // So try to get it from data handler:
                let $dropdown = $dropdownMenu.data('dropdown');

                return $dropdown.closest('.xcrud-main');
            }
        }
        return $(child).closest('.xcrud-main');
    },
    showDialog: function($main, params){
        var $dialog = $(DIALOG);
        var url = params.url;
        var width = params.width != undefined ? params.width : '';

        $dialog.data('xcrudmain', $main);

        $dialog.modal('show').on('shown.bs.modal', function(e){
            $.get(url, function(resp){
                $dialog.html(resp);
                $dialog.find('.modal-dialog').addClass(width);
                $dialog.find('input[type=text],input[type=number],input[type=email],textarea,select').not('[disabled]').not('[readonly]').first().focus();
                $dialog.trigger('content.loaded');
                if(params.callback != undefined && params.callback != ''){
                    if(typeof params.callback == 'function'){
                        params.callback.call()
                    }else{
                        eval(params.callback);
                    }
                }
            }).fail(function(jqxhr){
                $dialog.find('.modal-dialog').removeClass('modal-sm');
                $dialog.find('.modal-title').text('Error');
                $dialog.find('.modal-body').html(jqxhr.responseText);
            });
            $(this).unbind('shown.bs.modal');

        }).on('hidden.bs.modal', function(){
            $(this).remove();
        });
    },
    updateMainContent: function($mainContainer, data) {
        if ($mainContainer.length) {
            var $parent = $mainContainer.parent();
            if ($parent.length > 0) {
                $parent.html(data);

                var $newMainContainer = $parent.children('.xcrud-main').first();
                $newMainContainer.trigger('content.updated');
            } else {
                $($mainContainer.context).trigger('content.updated', [data]);
            }
            $(document).trigger('xcrud.content.updated', [data]);
        }
    }
};
