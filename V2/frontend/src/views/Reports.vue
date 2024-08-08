<template>
    <div class="container mt-4">
      <h2>Your Reports</h2>
  
      <div v-if="reports.length > 0">
        <ReportCard v-for="report in reports" :key="report.id" :report="report" />
      </div>
      <div v-else>
        <p>No reports available yet.</p>
      </div>
  
      <button class="btn btn-secondary mt-3" @click="exportCampaignData">Export Campaign Data (CSV)</button>
  
      <div v-if="exportStatus" class="mt-3">
        <p v-if="exportStatus === 'pending'">Export in progress...</p>
        <p v-else-if="exportStatus === 'success'">Export complete! Check your email for the download link.</p>
        <p v-else-if="exportStatus === 'error'">An error occurred during export. Please try again later.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { mapState, mapActions } from 'vuex';
  import ReportCard from '../components/ReportCard.vue';
  
  export default {
    name: 'Reports',
    components: { ReportCard },
    data() {
      return {
        exportStatus: null // 'pending', 'success', 'error'
      };
    },
    computed: {
      ...mapState('auth', ['currentUser']),
      ...mapState('reports', ['reports'])
    },
    mounted() {
      this.fetchReports();
    },
    methods: {
      ...mapActions('reports', ['fetchReports', 'exportCampaignData']),
      exportCampaignData() {
        this.exportStatus = 'pending';
        this.$store.dispatch('reports/exportCampaignData', this.currentUser.id)
          .then(() => {
            this.exportStatus = 'success';
          })
          .catch(error => {
            console.error('Error exporting campaign data:', error);
            this.exportStatus = 'error';
          });
      }
    }
  };
  </script>
  