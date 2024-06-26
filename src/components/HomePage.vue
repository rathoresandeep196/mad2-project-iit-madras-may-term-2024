<template>
    <div class="home-page">
      <!-- Navbar -->
      <div class="navbar">
        <div class="nav-logo">Library Management System</div>
        <div class="nav-links">
          <router-link to="/login">Login</router-link>
          <router-link to="/signup">Signup</router-link>
          <!-- <div class="dropdown">
            <button class="dropbtn">User</button>
            <div class="dropdown-content">
              <router-link to="/profile">Profile</router-link>
              <router-link to="/logout">Logout</router-link>
            </div>
          </div> -->
        </div>
      </div>
  
      <!-- Main Content: Welcome Message -->
      <div class="welcome-message">
        <h1>Welcome to our Library Management System!</h1>
        <p>Please log in to access the library features.</p>
      </div>
  
      <!-- Background Image -->
      <!-- <div class="background-image"></div> -->
  
      <!-- Footer -->
      <footer class="footer">
        <div class="social-media">
          <a href="#" class="social-link">Facebook</a>
          <a href="#" class="social-link">Twitter</a>
          <a href="#" class="social-link">Instagram</a>
        </div>
        <p>&copy; 2024 Library Management System. All rights reserved.</p>
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    // Add any necessary logic here, but for a simple home page, it may be minimal.
  };
  </script>
  
  <style scoped>
  /* Navbar Styles */
  .navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background-color: #333;
    color: white;
  }
  
  .nav-logo {
    font-size: 1.5rem;
  }
  
  .nav-links {
    display: flex;
    align-items: center;
  }
  
  .navbar a, .dropbtn {
    color: white;
    text-decoration: none;
    margin-left: 10px;
    cursor: pointer;
  }
  
  .navbar a:hover, .dropbtn:hover {
    text-decoration: underline;
  }
  
  .dropdown {
    position: relative;
    display: inline-block;
  }
  
  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 120px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
  }
  
  .dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
  }
  
  .dropdown-content a:hover {
    background-color: #f1f1f1;
  }
  
  .dropdown:hover .dropdown-content {
    display: block;
  }
  
  /* Welcome Message Styles */
  .welcome-message {
    padding: 50px 20px;
    text-align: center;
    color: #333;
  }
  
  .welcome-message h1 {
    font-size: 2.5rem;
    margin-bottom: 20px;
  }
  
  .welcome-message p {
    font-size: 1.2rem;
    color: #666;
  }
  
  /* Background Image Styles */
  
  /* Footer Styles */
  .footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding-left: 20px;
    position: fixed;
    margin-right: 0px;
    bottom: 0;
    width: 100%;
    height: 50px;
  }
  
  .social-media {
    margin-bottom: 10px;
  }
  
  .social-link {
    color: white;
    text-decoration: none;
    margin: 0 10px;
  }
  
  .social-link:hover {
    text-decoration: underline;
  }
  </style>
  