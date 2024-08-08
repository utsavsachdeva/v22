import axios from 'axios';

export default {
  namespaced: true,
  state: {
    adRequests: []
  },
  mutations: {
    SET_AD_REQUESTS(state, adRequests) {
      state.adRequests = adRequests;
    },
    ADD_AD_REQUEST(state, adRequest) {
      state.adRequests.push(adRequest);
    },
    UPDATE_AD_REQUEST(state, updatedAdRequest) {
      const index = state.adRequests.findIndex(ar => ar.id === updatedAdRequest.id);
      if (index !== -1) {
        state.adRequests.splice(index, 1, updatedAdRequest);
      }
    },
    DELETE_AD_REQUEST(state, adRequestId) {
      state.adRequests = state.adRequests.filter(ar => ar.id !== adRequestId);
    }
  },
  actions: {
    fetchAdRequestsForCampaign({ commit }, campaignId) {
      return axios.get(`/api/campaigns/${campaignId}/ad_requests`)
        .then(response => {
          commit('SET_AD_REQUESTS', response.data);
        })
        .catch(error => {
          console.error('Error fetching ad requests:', error);
          // Handle error, maybe show a notification to the user
        });
    },
    createAdRequest({ commit }, { campaignId, adRequestData }) {
      return axios.post(`/api/campaigns/${campaignId}/ad_requests`, adRequestData)
        .then(response => {
          commit('ADD_AD_REQUEST', response.data);
        })
        .catch(error => {
          console.error('Error creating ad request:', error);
          // Handle error, maybe show a notification to the user
        });
    },
    updateAdRequest({ commit }, { adRequestId, adRequestData }) {
      return axios.put(`/api/ad_requests/${adRequestId}`, adRequestData)
        .then(response => {
          commit('UPDATE_AD_REQUEST', response.data);
        })
        .catch(error => {
          console.error('Error updating ad request:', error);
          // Handle error, maybe show a notification to the user
        });
    },
    deleteAdRequest({ commit }, adRequestId) {
      return axios.delete(`/api/ad_requests/${adRequestId}`)
        .then(() => {
          commit('DELETE_AD_REQUEST', adRequestId);
        })
        .catch(error => {
          console.error('Error deleting ad request:', error);
          // Handle error, maybe show a notification to the user
        });
    }
  },
  getters: {
    allAdRequests: state => state.adRequests
    // Add more getters as needed for filtering or accessing specific ad requests
  }
}
