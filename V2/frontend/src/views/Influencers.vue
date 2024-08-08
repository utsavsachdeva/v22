<template>
    <div class="container mt-4">
      <SearchForm @search="handleSearch" search-type="influencers" /> 
  
      <div v-if="isLoading">
        <p>Loading influencers...</p>
      </div>
      <div v-else-if="error">
        <p class="alert alert-danger">{{ error }}</p>
      </div>
      <div v-else-if="influencers.length > 0">
        <InfluencerCard v-for="influencer in influencers" :key="influencer.id" :influencer="influencer" />
      </div>
      <div v-else>
        <p>No influencers found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState, mapActions } from 'vuex'
  import InfluencerCard from '../components/InfluencerCard.vue'
  import SearchForm from '../components/SearchForm.vue'
  
  export default {
    name: 'Influencers',
    components: {
      InfluencerCard,
      SearchForm
    },
    data() {
      return {
        isLoading: true,
        error: null
      }
    },
    computed: {
      ...mapState('influencers', ['influencers']) 
    },
    mounted() {
      this.fetchInfluencers()
        .then(() => {
          this.isLoading = false;
        })
        .catch(error => {
          this.error = 'An error occurred while fetching influencers.';
          this.isLoading = false;
        });
    },
    methods: {
      ...mapActions('influencers', ['fetchInfluencers', 'searchInfluencers']),
      handleSearch(query) {
        this.isLoading = true;
        this.error = null;
  
        this.searchInfluencers(query)
          .then(() => {
            this.isLoading = false;
          })
          .catch(error => {
            console.error('Error searching for influencers:', error);
            this.error = 'An error occurred during the search.';
            this.isLoading = false;
          });
      }
    }
  }
  </script>
  
  