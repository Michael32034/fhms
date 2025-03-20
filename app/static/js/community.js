const { createApp } = Vue;

createApp({
  data() {
    return {
      userNickname: "", // Можете змінити на актуальний нік користувача
      messages: [],
      newMessage: "",
    };
  },
  created() {
    this.fetchUserNickname();
    this.fetchMessages();
  },
  methods: {
    async fetchUserNickname() {
      try {
        const response = await fetch("/api/account", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });
        if (!response.ok) throw new Error("Failed to fetch user nickname");
      const data = await response.json();
      this.userNickname = data.nickname;
      this.fetchMessages(); // Після отримання імені завантажуємо повідомлення
      setInterval(this.fetchMessages, 10000); // Перевіряємо нові повідомлення
    } catch(error) {
      console.error("Error fetching user nickname:", error);
    }
  },
  async fetchMessages() {
    try {
      const response = await fetch("/api/commentaries/community", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      if (!response.ok) throw new Error("Failed to fetch messages");

      const data = await response.json();
      this.messages = data; // Ксєілуч вщі повідоємеллн, сюо додсьи перевірку
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  },
  async sendMessage() {
    if (!this.newMessage.trim()) return;

    try {
      const response = await fetch("/api/comentate/community", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: this.newMessage.trim() }),
      });
      if (!response.ok) throw new Error("Failed to send message");

      this.newMessage = ""; // Очищуємо поле вводу
      await this.fetchMessages(); // Оновлюємо список повідомлень
    } catch (error) {
      console.error("Error sending message:", error);
    }
  },
},
  }).mount("#app");
