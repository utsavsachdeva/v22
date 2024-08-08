<template>
  <div>
    <h2>{{ isEditing ? 'Edit Ad Request' : 'Create New Ad Request' }}</h2>

    <div v-if="isLoading">
      <p>Loading influencers...</p> 
    </div>

    <form v-else @submit.prevent="submitForm">
      <div class="form-group">
        <label for="influencer">Influencer:</label>
        <select id="influencer" v-model="form.influencer_id" class="form-control" required>
          <option v-for="influencer in influencers" :key="influencer.id" :value="influencer.id">
            {{ influencer.username }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="message">Message:</label>
        <textarea id="message" v-model="form.message" class="form-control" rows="3" required></textarea>
      </div>

      <div class="form-group">
        <label for="requirements">Requirements:</label>
        <textarea id="requirements" v-model="form.requirements" class="form-control" rows="3" required></textarea>
      </div>

      <div class="form-group">
        <label for="payment_amount">Payment Amount:</label>
        <input type="number" id="payment_amount" v-model.number="form.payment_amount" class="form-control" required>
      </div>

      <div v-if="error" class="alert alert-danger">{{ error }}</div> 

      <button type="submit" class="btn btn-primary">{{ isEditing ? 'Update' : 'Create' }}</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdRequestForm',
  props: {
    campaignId: {
      type: Number,
      required: true
    },
    initialAdRequest: { 
      type: Object,
      default: null
    }
  },
  data() {
    return {
      influencers: [], 
      form: {
        influencer_id: null,
        message: '',
        requirements: '',
        payment_amount: 0
      },
      isLoading: true, 
      error: null
    }
  },
  computed: {
    isEditing() {
      return this.initialAdRequest !== null
    }
  },
  mounted() {
    this.fetchInfluencers()
  },
  methods: {
    fetchInfluencers() {
      axios.get('/api/search/influencers') 
        .then(response => {
          this.influencers = response.data
          this.isLoading = false; 
          if (this.isEditing) {
            this.form = { ...this.initialAdRequest }
          }
        })
        .catch(error => {
          console.error(error)
          this.isLoading = false;
          this.error = 'An error occurred while fetching influencers.';
        })
    },
    submitForm() {
      this.isLoading = true;
      this.error = null;

      const apiUrl = this.isEditing 
        ? `/api/ad_requests/${this.initialAdRequest.id}` 
        : `/api/campaigns/${this.campaignId}/ad_requests`;

      const method = this.isEditing ? 'put' : 'post';

      axios[method](apiUrl, this.form)
        .then(() => {
          this.isLoading = false; 
          this.$emit(this.isEditing ? 'adRequestUpdated' : 'adRequestCreated')
          
          this.$emit('showSuccess', this.isEditing ? 'Ad request updated successfully!' : 'Ad request created successfully!');

          if (!this.isEditing) {
            this.form = {
              influencer_id: null,
              message: '',
              requirements: '',
              payment_amount: 0
            }
          }
        })
        .catch(error => {
          this.isLoading = false;
          console.error(error)
          this.error = (error.response && error.response.data && error.response.data.message) || 'An error occurred.';
        })
    }
  }
}
</script>
