const app = Vue.createApp({
    data() {
        return {
            form: {
                email: '',
                message: ''
            },
            vidpovid: ''
        };
    },
    methods: {
        async handleMessage() {
            try {
                const response = await fetch('/help', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(
                        {email: this.form.email, message: this.form.message}
                    )
                });

                const result = await response.json();
                console.log(1)
                if (result.status) { // Песеліз на йбосінкт /account
                    this.vidpovid = "Повідомлення надіслано, чекайте на відповідь протягом двох діб";
                } else { // Уізорсащення помилки
                    this.vidpovid = "Спробйте ще раз";
                }
            } catch (err) {
                this.vidpovid = 'Сталася помилка. Спробуйте ще раз!';
                console.error(err);
            }
        }
    }
});

app.mount('#app');
