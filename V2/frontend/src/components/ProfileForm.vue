<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3>Edit Profile</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="updateProfile">
                <div class="form-group">
                  <label for="username">Username:</label>
                  <input type="text" id="username" v-model="form.username" class="form-control" required>
                </div>
                <div class="form-group">
                  <label for="email">Email:</label>
                  <input type="email" id="email" v-model="form.email" class="form-control" required>
                </div>
  
                <div v-if="error" class="alert alert-danger">{{ error }}</div>
                <button type="submit" class="btn btn-primary">Update Profile</button>
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
    name: 'ProfileForm',
    data() {
      return {
        form: {
          username: '',
          email: ''
          // ... other profile fields
        },
        error: null
      }
    },
    mounted() {
      this.fetchProfileData()
    },
    methods: {
      fetchProfileData() {
        axios.get('/api/profile')
          .then(response => {
            this.form = response.data 
          })
          .catch(error => {
            console.error(error)
            // Handle error, show error message
          })
      },
      updateProfile() {
        this.error = null 
  
        axios.put('/api/profile', this.form)
          .then(() => {
            // Handle successful update (e.g., show a success message)
            this.$emit('profileUpdated') // Notify parent component if needed
          })
          .catch(error => {
            if (error.response && error.response.status === 409) {
              this.error = 'Username or email already exists.'
            } else {
              this.error = 'An error occurred while updating your profile.'
            }
          })
      }
    }
  }
  </script>
  