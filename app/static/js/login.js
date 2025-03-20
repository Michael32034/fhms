const app = Vue.createApp({
    data() {
        return {
            form: {
                nickname: '',
                password: ''
            },
            error: ''
        };
    },
    methods: {
        async handleSubmit() {
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(
                        {nickname: this.form.nickname, password: this.form.password}
                    )
                });

                const result = await response.json();
                console.log(1)
                if (result.status) { // Песеліз на йбосінкт /account
                    window.location.href = '/account';
                    console.log(2)
                } else { // Уізорсащення помилки
                    this.error = 'Нікнейм або пароль невірні!';
                    console.log(3)
                }
            } catch (err) {
                this.error = 'Сталася помилка. Спробуйте ще раз!';
                console.error(err);
            }
        }
    }
});

app.mount('#app');
