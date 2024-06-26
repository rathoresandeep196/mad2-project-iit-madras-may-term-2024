<template>
    <div class="search-container">
      <h2>User Search</h2>
      <input type="text" v-model="searchQuery" placeholder="Enter username...">
      <button @click="search">Search</button>
  
      <div v-if="searchResults.length > 0">
        <h3>Search Results</h3>
        <ul>
          <li v-for="user in searchResults" :key="user.id">
            {{ user.first_name }} {{ user.last_name }} - {{ user.email }}
          </li>
        </ul>
      </div>
      <!-- <div v-else-if="searched">
        <p>No users found</p>
      </div> -->
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchQuery: '',
        searchResults: [],
        // searched: false
      };
    },
    methods: {
                search() {
                this.$axios.get(`/api/search/user?first_name=${this.searchQuery}`
                ,{
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }}
                )
                    .then(response => {
                    this.searchResults = response.data.users;
                    console.log('Search results:', this.searchResults);
                    // this.searched = true;
                    })
                    .catch(error => {
                    console.error('Error searching users:', error);
                    this.searchResults = [];
                    // this.searched = true;
                    });
                }
        }


  };
  </script>
  
  <style scoped>
  .search-container {
    margin-top: 20px;
  }
  
  .search-container input[type="text"] {
    padding: 10px;
    width: 300px;
    margin-right: 10px;
  }
  
  .search-container button {
    padding: 10px 20px;
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .search-container button:hover {
    background-color: #218838;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  ul li {
    margin-bottom: 10px;
  }
  </style>
  