<template>
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title">{{ campaign.name }}</h5>
        <p class="card-text">{{ campaign.description }}</p>
        <p class="card-text">
          <strong>Sponsor:</strong> {{ campaign.sponsor.username }}
        </p>
        <p class="card-text">
          <strong>Budget:</strong> ${{ campaign.budget }}
        </p>
        <p class="card-text">
          <strong>Visibility:</strong> {{ campaign.visibility }}
        </p>
        <p class="card-text">
          <strong>Start Date:</strong> {{ formatDate(campaign.start_date) }}
        </p>
        <p class="card-text">
          <strong>End Date:</strong> {{ formatDate(campaign.end_date) }}
        </p>
  
        <router-link :to="{ name: 'CampaignDetails', params: { id: campaign.id } }" class="btn btn-primary">
          View Details
        </router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CampaignCard',
    props: {
      campaign: {
        type: Object,
        required: true
      }
    },
    methods: {
      formatDate(dateString) {
        const date = new Date(dateString)
        return date.toLocaleDateString() // You can customize the date format here
      }
    }
  }
  </script>
  