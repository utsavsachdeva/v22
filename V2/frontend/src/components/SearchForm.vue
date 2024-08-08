<template>
    <form class="form-inline my-2 my-lg-0" @submit.prevent="performSearch">
      <input 
        class="form-control mr-sm-2" 
        type="search" 
        placeholder="Search" 
        aria-label="Search" 
        v-model="searchQuery"
      >
  
      <select v-model="searchType" class="form-control mr-sm-2">
        <option value="campaigns">Campaigns</option>
        <option value="influencers">Influencers</option>
      </select>
  
      <button class="btn btn-outline-success my-2 my-sm-0 mr-2" type="submit">Search</button>
      <button class="btn btn-outline-secondary my-2 my-sm-0" type="button" @click="clearSearch">
        <i class="fas fa-times"></i> Clear 
      </button>
    </form>
  </template>
  
  <script>
  import _ from 'lodash';
  
  export default {
    name: 'SearchForm',
    data() {
      return {
        searchQuery: '',
        searchType: 'campaigns'
      }
    },
    methods: {
      performSearch: _.debounce(function() {
        this.$emit('search', this.searchQuery, this.searchType);
      }, 300), 
  
      clearSearch() {
        this.searchQuery = '';
        this.$emit('search', '', this.searchType); // Trigger search with empty query to reset results
      }
    }
  }
  </script>
  