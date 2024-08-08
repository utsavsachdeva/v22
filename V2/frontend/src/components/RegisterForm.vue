<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3>Register</h3>
            </div>
            <div class="card-body">
              <div v-if="isLoading">
                <p>Registering...</p> 
              </div>
              <div v-else-if="successMessage" class="alert alert-success">{{ successMessage }}</div> 
              <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
              <form v-else @submit.prevent="register">
                <div class="form-group">
                  <label for="username">Username:</label>
                  <input type="text" id="username" v-model="username" class="form-control" required>
                </div>
                <div class="form-group">
                  <label for="email">Email:</label>
                  <input type="email" id="email" v-model="email" class="form-control" required>
                </div>
                <div class="form-group">
                  <label for="password">Password:</label>
                  <input type="password" id="password" v-model="password" class="form-control" required>
                </div>
                <div class="form-group">
                  <label for="role">Role:</label>
                  <select id="role" v-model="role" class="form-control" required>
                    <option value="sponsor">Sponsor</option>
                    <option value="influencer">Influencer</option>
                  </select>
                </div>
                <button type="submit" class="btn btn-primary" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  Register
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'RegisterForm',
    data() {
      return {
        username: '',
        email: '',
        password: '',
        role: 'sponsor', 
        error: null,
        isLoading: false, 
        successMessage: null 
      }
    },
    methods: {
      register() {
        this.error = null;
        this.isLoading = true; 
  
        axios.post('/api/register', {
          username: this.username,
          email: this.email,
          password: this.password,
          role: this.role
        })
        .then(() => {
          this.isLoading = false;
          this.successMessage = 'Registration successful! You can now log in.'; 
          setTimeout(() => {
            this.$emit('registrationSuccessful'); 
            this.$router.push('/login'); 
          }, 3000); 
        })
        .catch(error => {
          this.isLoading = false;
          if (error.response && error.response.status === 409) {
            this.error = 'Username or email already exists.';
          } else {
            this.error = 'An error occurred during registration.';
          }
        });
      }
    }
  }
  </script>
  