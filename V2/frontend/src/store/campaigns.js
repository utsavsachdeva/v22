import axios from 'axios';

export default {
  namespaced: true,
  state: {
    campaigns: [],
    currentCampaign: null 
  },
  mutations: {
    SET_CAMPAIGNS(state, campaigns) {
      state.campaigns = campaigns
    },
    SET_CURRENT_CAMPAIGN(state, campaign) {
      state.currentCampaign = campaign
    },
    ADD_CAMPAIGN(state, campaign) {
      state.campaigns.push(campaign)
    },
    UPDATE_CAMPAIGN(state, updatedCampaign) {
      const index = state.campaigns.findIndex(c => c.id === updatedCampaign.id)
      if (index !== -1) {
        state.campaigns.splice(index, 1, updatedCampaign)
      }
      if (state.currentCampaign && state.currentCampaign.id === updatedCampaign.id) {
        state.currentCampaign = updatedCampaign
      }
    },
    DELETE_CAMPAIGN(state, campaignId) {
      state.campaigns = state.campaigns.filter(c => c.id !== campaignId)
      if (state.currentCampaign && state.currentCampaign.id === campaignId) {
        state.currentCampaign = null
      }
    }
  },
  actions: {
    fetchCampaigns({ commit }) {
      return axios.get('/api/campaigns')
        .then(response => {
          commit('SET_CAMPAIGNS', response.data)
        })
        .catch(error => {
          console.error('Error fetching campaigns:', error)
          // Handle error, maybe show a notification to the user
        })
    },
    fetchCampaignById({ commit }, campaignId) {
      return axios.get(`/api/campaigns/${campaignId}`)
        .then(response => {
          commit('SET_CURRENT_CAMPAIGN', response.data)
        })
        .catch(error => {
          console.error('Error fetching campaign:', error)
        })
    },
    createCampaign({ commit }, campaignData) {
      return axios.post('/api/campaigns', campaignData)
        .then(response => {
          commit('ADD_CAMPAIGN', response.data)
        })
        .catch(error => {
          console.error('Error creating campaign:', error)
        })
    },
    updateCampaign({ commit }, { campaignId, campaignData }) {
      return axios.put(`/api/campaigns/${campaignId}`, campaignData)
        .then(response => {
          commit('UPDATE_CAMPAIGN', response.data)
        })
        .catch(error => {
          console.error('Error updating campaign:', error)
        })
    },
    deleteCampaign({ commit }, campaignId) {
      return axios.delete(`/api/campaigns/${campaignId}`)
        .then(() => {
          commit('DELETE_CAMPAIGN', campaignId)
        })
        .catch(error => {
          console.error('Error deleting campaign:', error)
        })
    }
  },
  getters: {
    allCampaigns: state => state.campaigns,
    currentCampaign: state => state.currentCampaign
  }
}
