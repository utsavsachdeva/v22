<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <router-link class="navbar-brand" to="/">Influencer Platform</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/campaigns">Campaigns</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/influencers">Influencers</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <router-link class="nav-link" to="/profile">Profile</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn && currentUser.role === 'admin'">
            <router-link class="nav-link" to="/admin">Admin</router-link>
          </li>
        </ul>
        <form class="form-inline my-2 my-lg-0">
          <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit" @click.prevent="performSearch">Search</button>
        </form>
  
        <ul class="navbar-nav">
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item" v-if="!isLoggedIn">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
          <li class="nav-item" v-if="isLoggedIn">
            <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
          </li>
        </ul>
      </div>
    </nav>
  </template>
  
  <script>
  import { mapState, mapActions } from 'vuex' // Import from Vuex
  
  export default {
    name: 'AppHeader',
    data() {
      return {
        searchQuery: ''
      }
    },
    computed: {
      ...mapState('auth', ['isLoggedIn', 'currentUser']) // Map state from Vuex auth module
    },
    methods: {
      ...mapActions('auth', ['logout']), // Map logout action from Vuex
      performSearch() {
  if (this.searchType === 'campaigns') {
    this.$router.push({ name: 'CampaignSearchResults', query: { q: this.searchQuery } })
  } else if (this.searchType === 'influencers') {
    this.$router.push({ name: 'InfluencerSearchResults', query: { q: this.searchQuery } })
  }
}
    }
  }
  </script>
  