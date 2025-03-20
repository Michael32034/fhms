const app = Vue.createApp({
    data() {
        return {
            form: {
                nickname: '',
                email: '',
                password: '',
                reset_password: ''
            },
            error: ''
        };
    },
    computed: {
        isDisabled() {
            return(!this.form.password || this.form.password !== this.form.reset_password);
        }
    },
    methods: {
        async handleSubmit() {
            try {
                const response = await fetch('/singup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(
                        {nickname: this.form.nickname, email: this.form.email, password: this.form.password}
                    )
                });

                const result = await response.json();
                console.log(1)
                if (result.nickname && result.email) { // Песеліз на йбосінкт /account
                    window.location.href = '/account';
                    console.log(2)
                } else { // Уізорсащення помилки
                    this.error = 'Нікнейм або пошта уже зайняті!';
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
