<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h3>My Profile</h3>
            </div>
            <div class="card-body">
              <div v-if="isLoading">
                <p>Loading profile...</p>
              </div>
              <div v-else>
                <p><strong>Username:</strong> {{ currentUser.username }}</p>
                <p><strong>Email:</strong> {{ currentUser.email }}</p>
                <p><strong>Role:</strong> {{ currentUser.role }}</p>
                
                <button class="btn btn-primary mt-3" @click="isEditing = true">Edit Profile</button>
  
                <ProfileForm 
                  v-if="isEditing" 
                  :initialProfile="currentUser" 
                  @profileUpdated="fetchUserProfile" 
                  @close="isEditing = false" 
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState, mapActions } from 'vuex'
  import ProfileForm from '../components/ProfileForm.vue'
  
  export default {
    name: 'Profile',
    components: { ProfileForm },
    data() {
      return {
        isEditing: false,
        isLoading: true
      }
    },
    computed: {
      ...mapState('auth', ['currentUser'])
    },
    mounted() {
      this.fetchUserProfile()
    },
    methods: {
      ...mapActions('auth', ['fetchUserProfile']),
      fetchUserProfile() {
        this.isLoading = true
        this.$store.dispatch('auth/fetchUserProfile')
          .then(() => {
            this.isLoading = false
          })
          .catch(error => {
            console.error('Error fetching profile:', error)
            this.isLoading = false
            // Handle error, maybe show a notification to the user
          })
      }
    }
  }
  </script>
  