<template>
    <div class="container mt-4">
      <div v-if="isLoggedIn && currentUser.role === 'sponsor'">
        <button class="btn btn-primary mb-3" @click="showCreateCampaignForm = true">Create New Campaign</button>
      </div>
  
      <SearchForm @search="handleSearch" /> 
  
      <div v-if="showCreateCampaignForm">
        <CampaignForm @campaignCreated="fetchCampaigns" @close="showCreateCampaignForm = false" />
      </div>
  
      <div v-if="campaigns.length > 0">
        <CampaignCard v-for="campaign in campaigns" :key="campaign.id" :campaign="campaign" />
      </div>
      <div v-else>
        <p>No campaigns found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'

  import { mapState, mapActions } from 'vuex'
  import CampaignCard from '../components/CampaignCard.vue'
  import SearchForm from '../components/SearchForm.vue'
  import CampaignForm from '../components/CampaignForm.vue'
  
  export default {
    name: 'Campaigns',
    components: {
      CampaignCard,
      SearchForm,
      CampaignForm
    },
    data() {
      return {
        showCreateCampaignForm: false
      }
    },
    computed: {
      ...mapState('auth', ['isLoggedIn', 'currentUser']),
      ...mapState('campaigns', ['campaigns'])
    },
    mounted() {
      this.fetchCampaigns()
    },
    methods: {
      ...mapActions('campaigns', ['fetchCampaigns']),
      handleSearch(query) {
  // Make an API call to fetch filtered campaigns
  axios.get('/api/search/campaigns', { params: { q: query } })
    .then(response => {
      this.$store.commit('campaigns/SET_CAMPAIGNS', response.data) 
    })
    .catch(error => {
      console.error('Error searching for campaigns:', error)
      // Handle error, display an error message to the user
    })
}
    }
  }
  </script>
  