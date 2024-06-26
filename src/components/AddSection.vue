<template>
    <div>
      <nav class="navbar" v-if="isAuthenticated">
        <div class="nav-logo">Library Management System</div>
        <div class="nav-links">
          <router-link to="/stats">Stats</router-link>
          <router-link to="/books">Books</router-link>
          <router-link to="/Create/book">CreateBook</router-link>

          <button class="logout-button" @click="logout">Logout</button>
        </div>
      </nav>
      <h1 v-else>Please log in first!</h1>
      <div class="content" v-if="isAuthenticated">
        <div class="add-section-container">
          <button class="add-section-button" @click="showForm = true">+</button>
        </div>
        <div v-if="showForm" class="form-container">
          <h2>Add New Section</h2>
          <form @submit.prevent="submitForm">
            <div class="form-group">
              <label for="title">Title:</label>
              <input type="text" id="title" v-model="title" required />
            </div>
            <div class="form-group">
              <label for="dateCreated">Date Created:</label>
              <input type="date" id="dateCreated" v-model="dateCreated" required />
            </div>
            <div class="form-group">
              <label for="description">Description:</label>
              <textarea id="description" v-model="description" required></textarea>
            </div>
            <div class="form-group">
              <label for="file">Upload Book:</label>
              <input type="file" id="file" @change="handleFileUpload" required />
            </div>
            <button type="submit">Add</button>
            <button type="button" @click="cancelForm">Cancel</button>
          </form>
        </div>
        <div class="sections-container">
          <h2>Existing Sections</h2>
          <div v-for="section in sections" :key="section.id" class="section">
            <h3>{{ section.title }}</h3>
            <p>{{ section.description }}</p>
            <button @click="readSection(section.id)">View Section</button>
            <button @click="editSection(section.id)">Edit</button>
            <button @click="deleteSection(section.id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AddSection',
    data() {
      return {
        isAuthenticated: false,
        showForm: false,
        title: '',
        dateCreated: '',
        description: '',
        file: null,
        sections: [],
      };
    },
    mounted() {
      const token = localStorage.getItem('token');
      if (token) {
        this.isAuthenticated = true;
        this.fetchSections();
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
            localStorage.removeItem('role');
            this.isAuthenticated = false;
            this.$router.push('/');
          })
          .catch((error) => {
            console.log('Logout failed', error);
          });
      },
      handleFileUpload(event) {
        this.file = event.target.files[0];
      },
      submitForm() {
        const formData = new FormData();
        formData.append('title', this.title);
        formData.append('dateCreated', this.dateCreated);
        formData.append('description', this.description);
        formData.append('file', this.file);
  
        this.$axios
          .post('/add-section', formData, {
            headers: {  
              'Content-Type': 'multipart/form-data',
              Authorization: `Bearer ${localStorage.getItem('token')}`,
              'Access-Control-Allow-Origin': '*',
            },
          })
          .then((response) => {
            console.log('Section added successfully:', response.data);
            this.showForm = false;
            this.title = '';
            this.dateCreated = '';
            this.description = '';
            this.file = null;
            this.fetchSections(); // Fetch sections to update the list
          })
          .catch((error) => {
            console.error('Error adding section:', error);
          });
      },
      cancelForm() {
        this.showForm = false;
      },
      fetchSections() {
        this.$axios
          .get('/sections', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
              // ContentType : `multipart/form-data`,
            },
          })
          .then((response) => {
            this.sections = response.data;
          })
          .catch((error) => {
            console.error('Error fetching sections:', error);
          });
      },
      readSection(id) {
        this.$router.push(`/section/${id}`);
      },
      editSection(id) {
        this.$router.push(`/edit-section/${id}`);
      },
      deleteSection(id) {
        this.$axios
          .delete(`/section/${id}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          })
          .then((response) => {
            console.log('Section deleted successfully:', response.data);
            this.fetchSections();
          })
          .catch((error) => {
            console.error('Error deleting section:', error);
          });
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
  
  .logout-button {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
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
  
  .form-container {
    margin-top: 20px;
    width: 400px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
  }
  
  .form-group input, .form-group textarea {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  
  form button {
    padding: 10px 20px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  form button:hover {
    background-color: #2980b9;
  }
  
  .sections-container {
    margin-top: 30px;
  }
  
  .section {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
    width: 400px;
  }
  </style>
  