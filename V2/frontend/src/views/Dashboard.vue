<template>
    <div class="container mt-4">
      <h1 v-if="currentUser.role === 'sponsor'">Welcome, Sponsor {{ currentUser.username }}!</h1>
      <h1 v-else-if="currentUser.role === 'influencer'">Welcome, Influencer {{ currentUser.username }}!</h1>
  
      <div v-if="currentUser.role === 'sponsor'">
        <h2>Your Campaigns</h2>
        <div v-if="isLoadingCampaigns">
          <p>Loading campaigns...</p>
        </div>
        <div v-else-if="campaigns.length > 0">
          <CampaignCard v-for="campaign in campaigns" :key="campaign.id" :campaign="campaign" @viewDetails="viewCampaignDetails" />
        </div>
        <div v-else>
          <p>You haven't created any campaigns yet.</p>
          <button class="btn btn-primary" @click="$router.push('/campaigns')">Create a Campaign</button>
        </div>
  
        <div class="row mt-3">
          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Total Reach</h5>
                <p class="card-text">{{ totalReach }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Total Spend</h5>
                <p class="card-text">${{ totalSpend.toFixed(2) }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Avg. Payment per Influencer</h5>
                <p class="card-text">${{ avgPaymentPerInfluencer.toFixed(2) }}</p>
              </div>
            </div>
          </div>
        </div>
  
        <h2>Your Reports</h2>
        <div v-if="isLoadingReports">
          <p>Loading reports...</p>
        </div>
        <div v-else-if="reports.length > 0">
          <ReportCard v-for="report in reports" :key="report.id" :report="report" />
        </div>
        <div v-else>
          <p>No reports available yet.</p>
        </div>
      </div>
  
      <div v-else-if="currentUser.role === 'influencer'">
        <h2>Find Campaigns</h2>
        <SearchForm @search="handleSearch" search-type="campaigns" /> 
  
        <h2>Ad Requests</h2>
        <div v-if="isLoadingAdRequests">
          <p>Loading ad requests...</p>
        </div>
        <div v-else-if="adRequests.length > 0">
          <AdRequestCard v-for="adRequest in adRequests" :key="adRequest.id" :adRequest="adRequest" :currentUser="currentUser" />
        </div>
        <div v-else>
          <p>You have no ad requests at this time.</p>
          <button class="btn btn-primary" @click="$router.push('/campaigns')">Browse Campaigns</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState, mapActions } from 'vuex';
  import CampaignCard from '../components/CampaignCard.vue';
  import ReportCard from '../components/ReportCard.vue';
  import AdRequestCard from '../components/AdRequestCard.vue';
  import SearchForm from '../components/SearchForm.vue';
  
  export default {
    name: 'Dashboard',
    components: {
      CampaignCard,
      ReportCard,
      AdRequestCard,
      SearchForm
    },
    data() {
      return {
        isLoadingCampaigns: true,
        isLoadingReports: true,
        isLoadingAdRequests: true
      };
    },
    computed: {
      ...mapState('auth', ['currentUser']),
      ...mapState('campaigns', ['campaigns']),
      ...mapState('reports', ['reports']),
      ...mapState('adRequests', ['adRequests']),
      totalReach() {
        return this.campaigns.reduce((total, campaign) => total + (campaign.total_reach || 0), 0);
      },
      totalSpend() {
        return this.campaigns.reduce((total, campaign) => total + (campaign.total_spend || 0), 0);
      },
      avgPaymentPerInfluencer() {
        const totalAccepted = this.campaigns.reduce((total, campaign) => total + (campaign.accepted_ad_requests || 0), 0);
        return totalAccepted > 0 ? (this.totalSpend / totalAccepted) : 0;
      }
    },
    mounted() {
      if (this.currentUser.role === 'sponsor') {
        this.fetchCampaigns().then(() => { this.isLoadingCampaigns = false; });
        this.fetchReports().then(() => { this.isLoadingReports = false; });
      } else if (this.currentUser.role === 'influencer') {
        this.fetchAdRequests().then(() => { this.isLoadingAdRequests = false; });
      }
    },
    methods: {
      ...mapActions('campaigns', ['fetchCampaigns']),
      ...mapActions('reports', ['fetchReports']),
      ...mapActions('adRequests', ['fetchAdRequests']),
      handleSearch(query) {
        this.$router.push({ name: 'CampaignSearchResults', query: { q: query } });
      },
      viewCampaignDetails(campaignId) {
        this.$router.push({ name: 'CampaignDetails', params: { id: campaignId } });
      }
    }
  };
  </script>
  
  