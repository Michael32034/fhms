const { createApp } = Vue;

createApp({
  data() {
    return {
      utilities: []
    };
  },
  created() {
    this.fetchUtilities();
  },
  methods: {
    async fetchUtilities() {
      try {
        const response = await fetch("/api/utilities/home", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });
        if (!response.ok) throw new Error("Failed to fetch utilities");
      const data = await response.json();
      this.utilities = data.utilities
    } catch(error) {
      console.error("Error fetching utilities list:", error);
    }
  }
},
  }).mount("#app");
