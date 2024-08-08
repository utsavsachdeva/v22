<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3>Login</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="login">
                <div class="form-group">
                  <label for="email">Email:</label>
                  <input type="email" id="email" v-model="email" class="form-control" required>
                </div>
                <div class="form-group">
                  <label for="password">Password:</label>
                  <input type="password" id="password" v-model="password" class="form-control" required>
                </div>
                <div v-if="error" class="alert alert-danger">{{ error }}</div>
                <button type="submit" class="btn btn-primary" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  Login
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex'
  
  export default {
    name: 'LoginForm',
    data() {
      return {
        email: '',
        password: '',
        error: null,
        isLoading: false // Add loading state
      }
    },
    methods: {
      ...mapActions('auth', ['login']),
      login() {
        this.error = null;
        this.isLoading = true; // Show loading indicator
  
        this.login({ 
          email: this.email,
          password: this.password
        })
          .then(() => {
            this.isLoading = false; // Hide loading indicator on success
            this.$router.push('/dashboard') 
          })
          .catch(error => {
            this.isLoading = false; // Hide loading indicator on error
            if (error.response && error.response.status === 401) {
              this.error = 'Invalid credentials. Please try again.';
            } else if (error.response && error.response.status === 403) {
              this.error = 'Your account is not yet approved or has been deactivated.';
            } else {
              this.error = 'An error occurred during login. Please try again later.';
            }
          })
      }
    }
  }
  </script>
  
  