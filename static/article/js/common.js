/**
 * Главная функция, которая вызывается сразу
 * после загрузки html - файла
 */
(function() {
    /**
     * Главный объект, которые обробатывает события
     *
     * @type {{object}}
     */
	var app = {
        /**
         * Вызывает функции при инициализации
         */
		initialize : function () {
            app.setUpListeners();
            app.autoresizeTextarea();
		},
        /**
         * Автоматическое изменение размера textarea
         */
        autoresizeTextarea: function () {
            jQuery.each(jQuery('textarea[data-autoresize]'), function() {
                var offset = this.offsetHeight - this.clientHeight;

                var resizeTextarea = function(el) {
                    jQuery(el).css('height', 'auto').css('height', el.scrollHeight + offset);
                };
                jQuery(this).on('keyup input', function() { resizeTextarea(this); }).removeAttr('data-autoresize');
            });
        },
        /**
         * Контроллер событий
         */
        setUpListeners: function () {
            $('.showForm').on('click', app.showAuthModal);
            $('.auth_form').on('submit', app.submitForm);
            $('.auth_form').on('keydown', 'input', app.removeError);
            $('#modalAuth').on('show.bs.modal', app.hideAuthModalClickOur);
            $('.closeForm').on('click', app.hideAuthModal);
            $('a.rate').on('click', app.rateControl);
            $('a.updComment').on('click', app.updComment);
            $('div.addcomment button[type=reset]').on('click', app.updResetComment);
        },
        /**
         * Отобразить модальное окно входа, регистрации
         *
         * @param e вызываемый объест
         */
        showAuthModal: function (e) {
            e.preventDefault();
            if ($(this).attr('href') === '#ModalAuthRegister')
                app.showModalRegister();
            else if($(this).attr('href') === '#ModalAuthLogin')
                app.showModalLogin();
        },
        /**
         * Модальное окно открыть в разделе регистрации
         */
        showModalRegister: function () {
            $('#liLogin').removeClass('active');
            $('#liRegister').addClass('active');
            $('#liLogin').find('a').attr('aria-expanded', 'false');
            $('#liRegister').find('a').attr('aria-expanded', 'true');
            $('#login').removeClass('fade in active');
            $('#register').addClass('fade in active');
            $('#modalAuth').modal();
		},
        /**
         * Модальное окно открыть в разделе вохда
         */
        showModalLogin: function () {
            $('#liRegister').removeClass('active');
            $('#liLogin').addClass('active');
            $('#liRegister').find('a').attr('aria-expanded', 'false');
            $('#liLogin').find('a').attr('aria-expanded', 'true');
            $('#register').removeClass('fade in active');
            $('#login').addClass('fade in active');
            $('#modalAuth').modal();
		},
        /**
         * Изменение модального окна входа, регситрации, в зависимости
         * от корректности введённых данных пользователем
         *
         * @param e вызываемый объест
         */
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
                    else if (msg == 'error_valid'){
                        var textError = 'Ошибка!';
                        h1.html(textError).css('color','#e63c3c');
                    }
                }
            }).always(function () {
                submitBtn.removeAttr('disabled');
            });

        },
        /**
         * Валидация формы
         *
         * @param form форма
         * @param inputs поля значения которых надо проверить
         * @param action определяет событе: регистрация или авторизация
         * @param h1 заголовок формы
         * @returns {boolean}
         */
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
        /**
         * Удаляет у объекта класс "error"
         */
        removeError: function () {
            $(this).tooltip('destroy').removeClass('error');
        },
        /**
         * Закрытие модального окна регистрации, авторизации
         * если пользователь нажал левой кнопкой мыши
         * за границами модального окна
         *
         * @param e e вызываемый объест
         */
        hideAuthModalClickOur: function (e) {
            $(document).click(function (e) {
                if( $.inArray("login-signup", e.target.classList) === 0)
                    $('#modalAuth').modal('hide');
            });

        },
        /**
         * Закрытие модального окна регистрации, авторизации
         *
         * @param e вызываемый объест
         */
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
        },
        /**
         * Обновление текста комментария после добавления
         * @param e вызываемый объект
         */
        updComment: function (e) {
            e.preventDefault();
            var parent_div = $(this).parents('div.comment'),
                addcomment_div = $(parent_div).next('div.addcomment'),
                text = $(parent_div).children('p.comment_text').html(),
                newtext = $(addcomment_div).find('textarea');
            parent_div.addClass('hidden');
            newtext.val(text);
            $(addcomment_div).removeClass('hidden');

        },
        /**
         * Отображение поля для изменения комментария
         */
        updResetComment: function () {
            var parent_div = $(this).parents('div.addcomment'),
                comment_div = $(parent_div).prev('div.comment');
            parent_div.addClass('hidden');
            $(comment_div).removeClass('hidden');
        }

	};

	app.initialize();
}());