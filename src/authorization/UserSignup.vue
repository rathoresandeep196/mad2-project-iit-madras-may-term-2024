<template>
  <div class="signup-container">
    <div class="signup-form">
      <h2>Sign Up</h2>
      <p>It's free and only takes a minute</p>
      <form @submit.prevent="signup">
        <div class="form-group">
          <label for="firstName">First Name</label>
          <input type="text" id="firstName" v-model="firstName" required>
        </div>
        <div class="form-group">
          <label for="lastName">Last Name</label>
          <input type="text" id="lastName" v-model="lastName" required>
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword" required>
        </div>
        <div class="form-group">
          <label for="role">Role</label>
          <div class="role-options">
            <div>
              <input type="radio" id="librarian" value="Librarian" v-model="role">
              <label for="librarian">Librarian</label>
            </div>
            <div>
              <input type="radio" id="user" value="User" v-model="role">
              <label for="user">User</label>
            </div>
            <div>
              <input type="radio" id="admin" value="Admin" v-model="role">
              <label for="admin">Admin</label>
            </div>
          </div>
        </div>
        <button type="submit">Sign Up</button>
      </form>
      <p class="terms">
        By clicking the Sign Up button, you agree to our 
        <a href="#">Terms and Conditions</a> and <a href="#">Privacy Policy</a>.
      </p>
      <p class="login-link">
        Already have an account? <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      email: '',
      password: '',
      confirmPassword: '',
      role: '',
    };
  },
  methods: {
    validateEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    validatePassword(password) {
      const minLength = 8;
      return password.length >= minLength;
    },
    async signup() {
      if (this.password !== this.confirmPassword) {
        this.$toast.error('Passwords do not match', {
          position: 'top-right',
          timeout: 5000,
        });
        return;
      }
      if (!this.validateEmail(this.email)) {
        this.$toast.error('Please enter a valid email address', {
          position: 'top-right',
          timeout: 5000,
        });
        return;
      }
      if (!this.validatePassword(this.password)) {
        this.$toast.error('Password must be at least 8 characters long', {
          position: 'top-right',
          timeout: 5000,
        });
        return;
      }
      if (!this.role) {
        this.$toast.error('Please select a role', {
          position: 'top-right',
          timeout: 5000,
        });
        return;
      }

      const formData = {
        firstName: this.firstName,
        lastName: this.lastName,
        email: this.email,
        password: this.password,
        role: this.role,
      };

      this.$axios
        .post('/api/signup', formData)
        .then(() => {
          this.$toast.success('User created successfully', {
            position: 'top-right',
            timeout: 5000,
          });
          this.$router.push('/login');
        })
        .catch((error) => {
          const errorMsg = error.response?.data?.message || 'An error occurred';
          this.$toast.error(errorMsg, {
            position: 'top-right',
            timeout: 5000,
          });
        });

      try {

        // Optionally clear form fields after successful submission
        this.firstName = '';
        this.lastName = '';
        this.email = '';
        this.password = '';
        this.confirmPassword = '';
        this.role = '';

      } catch (error) {
        const errorMsg = error.response?.data?.message || 'An error occurred';
        // this.$toast.error(errorMsg, {
        //   position: 'top-right',
        //   timeout: 5000,
        // });
        console.log(errorMsg);
      }
    }
  }
};
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
  padding-top: 70px; /* Adjust this if your navbar height is different */
}

.signup-form {
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  text-align: center;
}

.signup-form h2 {
  margin-bottom: 10px;
  font-size: 24px;
  color: #333;
}

.signup-form p {
  margin-bottom: 20px;
  color: #666;
}

.signup-form .form-group {
  margin-bottom: 10px;
  text-align: left;
}

.signup-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: 300;
  color: #333;
}

.signup-form input[type="text"],
.signup-form input[type="email"],
.signup-form input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
}

.signup-form .role-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.signup-form .role-options div {
  display: flex;
  align-items: center;
}

.signup-form .role-options input {
  margin-right: 8px;
}

.signup-form button {
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

.signup-form button:hover {
  background-color: #218838;
}

.signup-form .terms {
  font-size: 14px;
  color: #666;
  margin-top: 20px;
}

.signup-form .terms a {
  color: #007bff;
  text-decoration: none;
}

.signup-form .terms a:hover {
  text-decoration: underline;
}

.signup-form .login-link {
  margin-top: 10px;
  font-size: 14px;
}

.signup-form .login-link a {
  color: #007bff;
  text-decoration: none;
}

.signup-form .login-link a:hover {
  text-decoration: underline;
}
</style>
