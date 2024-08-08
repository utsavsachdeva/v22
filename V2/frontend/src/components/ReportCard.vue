<template>
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title">
          Report for {{ report.start_date }} - {{ report.end_date }}
          <span class="badge badge-info ml-2" v-if="report.format">{{ report.format.toUpperCase() }}</span> 
        </h5>
        <p class="card-text">
          <strong>Generated On:</strong> {{ formatDate(report.created_at) }}
        </p>
  
        <div v-if="downloadError" class="alert alert-danger">{{ downloadError }}</div>
  
        <a 
          :href="getDownloadUrl()" 
          class="btn btn-primary" 
          download 
          :disabled="isDownloading"
          @click.prevent="downloadReport"
        >
          <span v-if="isDownloading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          Download Report
        </a>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'

  export default {
    name: 'ReportCard',
    props: {
      report: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        isDownloading: false,
        downloadError: null
      }
    },
    methods: {
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString(); 
      },
      getDownloadUrl() {
        return `/api/reports/${this.report.id}?format=${this.report.format || 'pdf'}` 
      },
      downloadReport() {
        this.isDownloading = true;
        this.downloadError = null;
  
        axios.get(this.getDownloadUrl(), {
          responseType: 'blob' // Important for file downloads
        })
          .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `report_${this.report.id}.${this.report.format || 'pdf'}`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
            this.isDownloading = false;
          })
          .catch(error => {
            console.error('Error downloading report:', error);
            this.isDownloading = false;
            this.downloadError = 'An error occurred while downloading the report. Please try again later.'
          })
      }
    }
  }
  </script>
  
  