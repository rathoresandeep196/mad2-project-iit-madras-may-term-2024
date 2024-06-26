<template>
  <div class="login-container">
    <div class="login-form">
      <h2>Login</h2>
      <p>Welcome back! Please login to your account.</p>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <button type="submit">Login</button>
      </form>
      <p class="terms">
        By logging in, you agree to our 
        <a href="#">Terms and Conditions</a> and <a href="#">Privacy Policy</a>.
      </p>
      <p class="signup-link">
        Don't have an account? <a href="/signup">Sign up here</a>
      </p>
    </div>
  </div>
</template>

<script>

import { useToast } from 'vue-toastification';

export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  setup() {
    const toast = useToast();
    return { toast };
  },
  methods: {
    validateEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    login() {
      if (!this.validateEmail(this.email)) {
        this.toast.error('Please enter a valid email address', {
          position: 'top-right',
          timeout: 5000,
        });
        return;
      }

      const formData = {
        email: this.email,
        password: this.password,
      };

      this.$axios
        .post('/api/login', formData, { withCredentials: false,})
        .then((response) => {
          localStorage.setItem('token', response.data.access_token);
          localStorage.setItem('user', JSON.stringify(response.data.user_info));
          if (response.data.user_info.role === 'Admin') {
            this.$router.push('/admin');
          }else{
            this.$router.push('/dashboard');
          }

          // this.$router.push('/dashboard');
          this.$toast.success('Logged in successfully', {
            position: 'top-right',
            timeout: 5000,
          });
        })
        .catch((error) => {
          // console.log(error.response.data.message);
          const errorMsg = error.response?.data?.message;
          // console.log(errorMsg);
          // const errorMsg = error.response?.data?.message || 'An error occurred';
          this.$toast.error(errorMsg, {
            position: 'top-right',
            timeout: 5000,
          });
        });
    },
  },
};
</script>
<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
  padding-top: 60px; /* Adjust this if your navbar height is different */
}

.login-form {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  text-align: center;
}

.login-form h2 {
  margin-bottom: 10px;
  font-size: 24px;
  color: #333;
}

.login-form p {
  margin-bottom: 20px;
  color: #666;
}

.login-form .form-group {
  margin-bottom: 15px;
  text-align: left;
}

.login-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
}

.login-form input[type="email"],
.login-form input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

.login-form button {
  width: 100%;
  padding: 12px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

.login-form button:hover {
  background-color: #218838;
}

.login-form .terms {
  font-size: 14px;
  color: #666;
  margin-top: 20px;
}

.login-form .terms a {
  color: #007bff;
  text-decoration: none;
}

.login-form .terms a:hover {
  text-decoration: underline;
}

.login-form .signup-link {
  margin-top: 10px;
  font-size: 14px;
}

.login-form .signup-link a {
  color: #007bff;
  text-decoration: none;
}

.login-form .signup-link a:hover {
  text-decoration: underline;
}
</style>
