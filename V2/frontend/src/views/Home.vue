<template>
    <div class="container mt-4">
      <div class="jumbotron">
        <h1 class="display-4">Welcome to the Influencer Platform!</h1>
        <p class="lead">Connect with sponsors and influencers to create impactful campaigns.</p>
        <hr class="my-4">
        <p v-if="!isLoggedIn">
          Get started today!
        </p>
        <div class="d-flex" v-if="!isLoggedIn">
          <router-link to="/register" class="btn btn-primary mr-2">Register</router-link>
          <router-link to="/login" class="btn btn-secondary">Login</router-link>
        </div>
      </div>
  
      <div class="row">
        <div class="col-md-6">
          <h2>Featured Campaigns</h2>
          <div v-if="featuredCampaigns.length > 0">
            <CampaignCard v-for="campaign in featuredCampaigns" :key="campaign.id" :campaign="campaign" />
          </div>
          <div v-else>
            <p>No featured campaigns at this time.</p>
          </div>
        </div>
        <div class="col-md-6">
          <h2>Top Influencers</h2>
          <div v-if="topInfluencers.length > 0">
            <InfluencerCard v-for="influencer in topInfluencers" :key="influencer.id" :influencer="influencer" />
          </div>
          <div v-else>
            <p>No top influencers to display.</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState } from 'vuex'
  import CampaignCard from '../components/CampaignCard.vue'
  import InfluencerCard from '../components/InfluencerCard.vue'
  
  export default {
    name: 'Home',
    components: {
      CampaignCard,
      InfluencerCard
    },
    computed: {
      ...mapState('auth', ['isLoggedIn']),
      ...mapState('campaigns', ['featuredCampaigns']), // Assuming you have a 'featuredCampaigns' getter in your campaigns module
      ...mapState('influencers', ['topInfluencers']) // Assuming you have a 'topInfluencers' getter in your influencers module
    },
    mounted() {
      // Fetch featured campaigns and top influencers from the store (or API directly)
      this.$store.dispatch('campaigns/fetchFeaturedCampaigns') 
      this.$store.dispatch('influencers/fetchTopInfluencers') 
    }
  }
  </script>
  