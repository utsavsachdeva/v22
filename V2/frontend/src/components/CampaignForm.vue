
<template>
  <div>
    <h2>{{ isEditing ? 'Edit Campaign' : 'Create New Campaign' }}</h2>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Campaign Name:</label>
        <input type="text" id="name" v-model="form.name" class="form-control" required>
      </div>

      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description"   
 v-model="form.description" class="form-control"  
 rows="3" required></textarea>
      </div>

      <div class="form-group">
        <label for="start_date">Start Date:</label>
        <input type="date" id="start_date" v-model="form.start_date" class="form-control" required>
      </div>

      <div class="form-group">
        <label for="end_date">End Date:</label>
        <input type="date" id="end_date"   
 v-model="form.end_date" class="form-control" required>
      </div>

      <div class="form-group">
        <label for="budget">Budget:</label>
        <input type="number" id="budget" v-model.number="form.budget" class="form-control" required>
      </div>

      <div class="form-group">
        <label for="visibility">Visibility:</label>
        <select id="visibility" v-model="form.visibility" class="form-control" required>
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
      </div>

      <div class="form-group">
        <label for="goals">Goals:</label>   

        <textarea id="goals" v-model="form.goals" class="form-control" rows="3" required></textarea>
      </div>

      <div class="form-group">
        <label for="categories">Categories:</label>
        <select id="categories" v-model="form.categories" class="form-control" multiple required>
          <option v-for="category in allCategories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>

      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div> 

      <button type="submit" class="btn btn-primary" :disabled="isLoading">
        <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 
  

        {{ isEditing ? 'Update' : 'Create' }}
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CampaignForm',
  props: {
    initialCampaign: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      form: {
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        budget: 0,
        visibility: 'public',
        goals: '',
        categories: [] // Add categories field to the form data
      },
      isLoading: false, 
      error: null,
      allCategories: [] // To store the list of all categories fetched from the API
    }
  },
  computed: {
    isEditing() {
      return this.initialCampaign !== null
    }
  },
  mounted() {
    if (this.isEditing) {
      this.form = { ...this.initialCampaign }
    }

    // Fetch all categories from the API
    this.fetchCategories();
  },
  methods: {
    fetchCategories() {
      axios.get('/api/categories')
        .then(response => {
          this.allCategories = response.data
        })
        .catch(error => {
          console.error('Error fetching categories:', error)
          // Handle error, show error message
          this.error = 'An error occurred while fetching categories.'
        })
    },
    submitForm() {
      this.isLoading = true
      this.error = null

      const apiUrl = this.isEditing
        ? `/api/campaigns/${this.initialCampaign.id}`
        : '/api/campaigns';

      const method = this.isEditing ? 'put' : 'post';

      axios[method](apiUrl, this.form)
        .then(() => {
          this.isLoading = false
          this.$emit(this.isEditing ? 'campaignUpdated' : 'campaignCreated')
          this.$emit('showSuccess', this.isEditing ? 'Campaign updated successfully!' : 'Campaign created successfully!')

          // Reset the form if creating a new campaign
          if (!this.isEditing) {
            this.form = {
              name: '',
              description: '',
              start_date: '',
              end_date: '',
              budget: 0,
              visibility: 'public',
              goals: '',
              categories: []
            }
          }
        })
        .catch(error => {
          this.isLoading = false
          console.error(error)
          this.error = (error.response && error.response.data && error.response.data.message) || 'An error occurred.';
        })
    }
  }
}
</script>
