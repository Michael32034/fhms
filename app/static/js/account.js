const app = Vue.createApp({
    data() {
        return {
            account: {
                nickname: "",
                email: "",
                comments_count: null
            }
        };
    },
    mounted() {
        this.fetchAccountData();
    },
    methods: {
        async fetchAccountData() {
            try {
                const response = await fetch("/api/account", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });

                if (! response.ok) {
                    throw new Error("Failed to fetch account data");
                }

                const data = await response.json();
                this.account.nickname = data.nickname;
                this.account.email = data.email;
                this.account.comments_count = data.comments_count || 0;
            } catch (error) {
                console.error("Error fetching account data:", error);
                alert("Failed to load account data. Please try again later.");
            }
        },
        logout() {
            window.location.href = "/logout";
        }
    }
}).mount("#app");
