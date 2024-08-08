<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3>Register</h3>
            </div>
            <div class="card-body">
              <RegisterForm @registrationSuccessful="handleRegistrationSuccess" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import RegisterForm from '../components/RegisterForm.vue';
  
  export default {
    name: 'Register',
    components: { RegisterForm },
    methods: {
      handleRegistrationSuccess() {
        // Handle successful registration (e.g., show a success message, redirect to login)
        this.$router.push('/login'); // Redirect to login after successful registration
      }
    }
  };
  </script>
  