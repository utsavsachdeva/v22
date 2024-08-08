<template>
    <div class="card mb-3">
      <div class="card-body">
        <h5 class="card-title">{{ influencer.username }}</h5>
        <p class="card-text">
          <strong>Niche:</strong> {{ influencer.niche }}
        </p>
        <p class="card-text">
          <strong>Reach:</strong> {{ influencer.reach }}
        </p>
        <p class="card-text">
          <strong>Categories:</strong>
          <span v-for="category in influencer.categories" :key="category.id" class="badge badge-secondary mr-1">
            {{ category.name }}
          </span>
        </p>
  
        <router-link :to="{ name: 'InfluencerProfile', params: { id: influencer.id } }" class="btn btn-primary">
          View Profile
        </router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'InfluencerCard',
    props: {
      influencer: {
        type: Object,
        required: true
      }
    }
  }
  </script>
  