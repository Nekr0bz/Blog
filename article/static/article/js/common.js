(function() {

	var app = {

        MODAL_LOGIN : 1,
        MODAL_REGISTER : 2,

		initialize : function () {
			app.setUpListeners();

            if ($.cookie('MODAL') == app.MODAL_LOGIN) app.showModalLogin();
            if ($.cookie('MODAL') == app.MODAL_REGISTER) app.showModalRegister();
		},

		setUpListeners: function () {
            $('form').on('submit', app.submitForm);
            $('form').on('keydown', 'input', app.removeError);
            $('#modalAuth').on('hidden.bs.modal', app.delCookieModal);
            $('#modalAuth').on('show.bs.modal', app.hideAuthModalClickOur);
            $('.closeForm').on('click', app.hideAuthModal);
		},
        
        submitForm: function (e) {
            e.preventDefault();

            var form = $(this);

            if( app.validateForm(form) === false) return false;

            console.log('ajax');
        },

        validateForm: function (form) {
            var inputs = form.find('input'),
                valid = true;

            $.each(inputs, function (index, val) {
                var input = $(val),
                    val = input.val(),
                    textError = 'Заполните поле';

                if(val.length === 0){
                    input.tooltip({
                    trigger : 'manual',
                    placement : 'right',
                    title : textError
                    }).tooltip('show');
                    valid = false;
                }else {
                    input.tooltip('hide');
                }

            });
            return valid;
        },

        removeError: function () {
            $(this).tooltip('destroy')
        },

		showModalRegister: function (e) {
            if (this != app) e.preventDefault();

            $('#liLogin').removeClass('active');
            $('#liRegister').addClass('active');
            $('#liLogin').find('a').attr('aria-expanded', 'false');
            $('#liRegister').find('a').attr('aria-expanded', 'true');
            $('#login').removeClass('fade in active');
            $('#register').addClass('fade in active');
            $('#modalAuth').modal();
		},

        showModalLogin: function (e) {
            if (this != app) e.preventDefault();

            $('#liRegister').removeClass('active');
            $('#liLogin').addClass('active');
            $('#liRegister').find('a').attr('aria-expanded', 'false');
            $('#liLogin').find('a').attr('aria-expanded', 'true');
            $('#register').removeClass('fade in active');
            $('#login').addClass('fade in active');
            $('#modalAuth').modal();
		},

        delCookieModal: function (e) {
            $.removeCookie('MODAL');
        },

		hideAuthModalClickOur: function (e) {
            $(document).click(function (e) {
                if( $.inArray("login-signup", e.target.classList) === 0){
                    $('#modalAuth').modal('hide');
                }
            });
        },

        hideAuthModal:function (e) {
            e.preventDefault();
            $('#modalAuth').modal('hide');
        }

	};

	app.initialize();
}());