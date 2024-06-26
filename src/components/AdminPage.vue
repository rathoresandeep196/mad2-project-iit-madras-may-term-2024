<template>
  <div>
    <nav class="navbar" v-if="isAuthenticated">
      <div class="nav-logo">Library Management System</div>
      <div class="nav-links">
        <router-link to="/stats">Stats</router-link>
        <button class="search-button" @click="goToSearch">Search Users</button>
        <button class="logout-button" @click="logout">Logout</button>
      </div>
    </nav>
    <h1 v-else>Please log in first!</h1>
    <div class="content" v-if="isAuthenticated">
      <h2>Add Sections to view</h2>
      <div class="add-section-container">
        <button class="add-section-button" @click="addSection">+</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashBoard',
  data() {
    return {
      isAuthenticated: false,
    };
  },
  mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      this.isAuthenticated = true;
    }
  },
  methods: {
    logout() {
      const accessToken = localStorage.getItem('token');
      this.$axios
        .post('/logout', null, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })
        .then(() => {
          localStorage.removeItem('token');
          localStorage.removeItem('role'); // Remove role if stored in localStorage
          this.isAuthenticated = false;
          this.$router.push('/');
        })
        .catch((error) => {
          console.log('Logout failed', error);
        });
    },
    goToSearch() {
      this.$router.push('/search/user');
    },
    addSection() {
      this.$router.push('/add/section');
    },
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #2c3e50;
  color: white;
}

.nav-logo {
  font-size: 24px;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 18px;
}

.nav-links a:hover {
  text-decoration: underline;
}

.search-button, .logout-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-button {
  background-color: #3498db;
  color: white;
}

.search-button:hover {
  background-color: #2980b9;
}

.logout-button {
  background-color: #e74c3c;
  color: white;
}

.logout-button:hover {
  background-color: #c0392b;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}

.add-section-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 50px;
}

.add-section-button {
  width: 50px;
  height: 50px;
  border: 2px solid #2c3e50;
  border-radius: 50%;
  background-color: white;
  font-size: 24px;
  cursor: pointer;
  outline: none;
}

.add-section-button:hover {
  background-color: #f0f0f0;
}
</style>
