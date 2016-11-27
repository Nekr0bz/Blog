(function() {

	var app = {

		initialize : function () {
            app.setUpListeners();
            app.autoresizeTextarea();
		},

        autoresizeTextarea: function () {
            jQuery.each(jQuery('textarea[data-autoresize]'), function() {
                var offset = this.offsetHeight - this.clientHeight;

                var resizeTextarea = function(el) {
                    jQuery(el).css('height', 'auto').css('height', el.scrollHeight + offset);
                };
                jQuery(this).on('keyup input', function() { resizeTextarea(this); }).removeAttr('data-autoresize');
            });
        },

        setUpListeners: function () {
            $('.showForm').on('click', app.showAuthModal);
            $('.auth_form').on('submit', app.submitForm);
            $('.auth_form').on('keydown', 'input', app.removeError);
            $('#modalAuth').on('show.bs.modal', app.hideAuthModalClickOur);
            $('.closeForm').on('click', app.hideAuthModal);
            $('a.rate').on('click', app.rateControl);
        },

        showAuthModal: function (e) {
            e.preventDefault();
            if ($(this).attr('href') === '#ModalAuthRegister')
                app.showModalRegister();
            else if($(this).attr('href') === '#ModalAuthLogin')
                app.showModalLogin();
        },

        showModalRegister: function () {
            $('#liLogin').removeClass('active');
            $('#liRegister').addClass('active');
            $('#liLogin').find('a').attr('aria-expanded', 'false');
            $('#liRegister').find('a').attr('aria-expanded', 'true');
            $('#login').removeClass('fade in active');
            $('#register').addClass('fade in active');
            $('#modalAuth').modal();
		},

        showModalLogin: function () {
            $('#liRegister').removeClass('active');
            $('#liLogin').addClass('active');
            $('#liRegister').find('a').attr('aria-expanded', 'false');
            $('#liLogin').find('a').attr('aria-expanded', 'true');
            $('#register').removeClass('fade in active');
            $('#login').addClass('fade in active');
            $('#modalAuth').modal();
		},

        submitForm: function (e) {
            e.preventDefault();

            var form = $(this),
                inputs = form.find('input'),
                submitBtn = form.find('button[type="submit"]'),
                action = form.attr('action') ;

            if(action === '/register/')
                var h1 = $('#h1_reg');
            else if(action === '/login/')
                var h1 = $('#h1_log');

            inputs = inputs.filter(function (i) {
               return $(inputs[i]).attr('name') !== 'csrfmiddlewaretoken';
            });

            /*TODO: Валидацию формы сделать польностью на серве*/
            if( app.validateForm(form, inputs, action, h1) === false) return false;

            submitBtn.attr('disabled', 'disabled');

            var data = {};

            $.each(inputs, function (index, obj) {
                var input = $(obj),
                    val = input.val(),
                    name = input.attr('name');
                data[name] = val;
            });

            $.ajax({
                'url': action,
                type: 'POST',
                'data':{
                    csrfmiddlewaretoken:form.find('input[name=csrfmiddlewaretoken]').val(),
                    dataAuth:JSON.stringify(data)
                }
            }).done(function (msg) {
                if(msg === 'OK')
                    location.reload();
                else{
                    if (msg === 'error_login'){
                        var textError = 'Неверный логин или пароль!';
                        h1.html(textError).css('color','#e63c3c');
                        $('input[name="username"]').addClass('error');
                        $('input[name="password"]').addClass('error');
                    }
                    else if (msg === 'error_name'){
                        var textError = 'Пользователь с таким логином уже существует!';
                        h1.html(textError).css('color','#e63c3c');
                        $('input[name="username"]').addClass('error');
                    }
                }
            }).always(function () {
                submitBtn.removeAttr('disabled');
            });

        },

        validateForm: function (form, inputs, action, h1) {
            var valid = true;

            // Проверка: заполнены ли поля
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
                    input.addClass('error');
                    valid = false;
                }else {
                    input.tooltip('hide');
                }
            });

            if (valid===false){
                h1.html('Все поля должны быть заполнены!').css('color','#e63c3c');
                return valid;
            }

            if(action === '/register/'){
                var pass1 = form.find($('input[name = password1]')),
                    pass2 = form.find($('input[name = password2]')),
                    username = form.find($('input[name = username]'));

                // Проверка: кол-во символов в пароле меньше 4
                if(pass1.val().length < 4){
                    h1.html('Пароль должен быть не короче 4 символов!').css('color','#e63c3c');
                    pass1.addClass('error').val('');
                    pass2.addClass('error').val('');
                    return false;
                }

                // Проверка: кол-во символов в логине меньше 4
                if(username.val().length < 4){
                    h1.html('Логин должен быть не короче 4 символов!').css('color','#e63c3c');
                    username.addClass('error').val('');
                    return false;
                }

                //Проверка: пароль и логин должен содержать символы латинского языка
                var regexp = /^[a-z0-9]+$/i,
                    newinputs = inputs.filter(function (i) {
                       return $(inputs[i]).attr('name') !== 'mail';
                    });

                $.each(newinputs, function(index, val) {
                    var input = $(val),
                        val = input.val();

                    if (!regexp.test(val)){
                        input.addClass('error').val('');
                        valid = false;
                    }
                });

                if (valid===false){
                    h1.html('Поля должны быть заполнены только латинскими буквами и цифрами').css('color','#e63c3c');
                    return valid;
                }

                // Проверка: равенство паролей
                if(pass1.val() !== pass2.val()){
                    h1.html('Пароли не совпадают!').css('color','#e63c3c');
                    pass1.addClass('error').val('');
                    pass2.addClass('error').val('');
                    return false;
                }
            }
            return valid;
        },

        removeError: function () {
            $(this).tooltip('destroy').removeClass('error');
        },

        hideAuthModalClickOur: function (e) {
            $(document).click(function (e) {
                if( $.inArray("login-signup", e.target.classList) === 0)
                    $('#modalAuth').modal('hide');
            });

        },

        hideAuthModal:function (e) {
            e.preventDefault();
            $('#modalAuth').modal('hide');
            /*TODO: вынести в объявление, не делать отдельную функци.*/
        },

        rateControl: function (e) {
            e.preventDefault();
            var ithis = $(this),
                vote = ithis[0].classList[1],
                p = ithis.parent()[0],
                table_type = p.classList[0],
                table_id = ithis.attr('href'),
                other_class= vote == 'dislike'? 'like' : 'dislike',
                other_rate = $(p).children('a.'+other_class);

            $(p).addClass('lock');

            $.ajax({
                'url':'/ratecontrol/',
                type: 'GET',
                'data':{
                    'vote':vote,
                    'table_type':table_type,
                    'table_id':table_id
                }
            }).done(function (msg) {
                msg = msg.split('/');
                $(ithis).children('span[class=rate]').html(msg[0]);
                $(ithis).toggleClass('active');
                $(other_rate).children('span[class=rate]').html(msg[1]);
                $(other_rate).removeClass('active');
            }).always(function () {
                $(p).removeClass('lock');
            });
        }

	};

	app.initialize();
}());