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
                <button type="submit" class="btn btn-primary">Login</button>
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
    name: 'Login',
    data() {
      return {
        email: '',
        password: '',
        error: null
      }
    },
    methods: {
      ...mapActions('auth', ['login']), 
      login() {
        this.error = null; 
  
        this.$store.dispatch('auth/login', { 
          email: this.email,
          password: this.password
        })
        .then(() => {
          this.$router.push('/dashboard') 
        })
        .catch(error => {
          this.error = (error.response && error.response.data && error.response.data.message) || 'An error occurred during login.'
        })
      }
    }
  }
  </script>
  