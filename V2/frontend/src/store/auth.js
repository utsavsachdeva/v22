import axios from 'axios';

export default {
  namespaced: true,
  state: {
    isLoggedIn: false,
    user: null,
    token: localStorage.getItem('token') || null 
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
    SET_TOKEN(state, token) {
      state.token = token;
      localStorage.setItem('token', token); 
    },
    LOGIN(state) {
      state.isLoggedIn = true;
    },
    LOGOUT(state) {
      state.isLoggedIn = false;
      state.user = null;
      state.token = null;
      localStorage.removeItem('token');
    }
  },
  actions: {
    login({ commit }, credentials) {
      return new Promise((resolve, reject) => {
        axios.post('/api/login', credentials)
          .then(response => {
            const token = response.data.access_token;
            commit('SET_TOKEN', token);
            // Fetch user profile after successful login
            dispatch('fetchUserProfile')
              .then(user => {
                commit('SET_USER', user);
                commit('LOGIN');
                resolve(user); // Resolve the promise with the user data
              })
              .catch(error => {
                commit('LOGOUT'); // Logout on profile fetch error
                reject(error);
              });
          })
          .catch(error => {
            reject(error);
          });
      });
    },
    logout({ commit }) {
      commit('LOGOUT');
    },
    register({ commit }, userData) {
      return new Promise((resolve, reject) => {
        axios.post('/api/register', userData)
          .then(() => {
            resolve(); // Registration successful
          })
          .catch(error => {
            reject(error);
          });
      });
    },
    fetchUserProfile({ commit, state }) {
      return new Promise((resolve, reject) => {
        axios.get('/api/profile', {
          headers: { Authorization: `Bearer ${state.token}` } 
        })
          .then(response => {
            commit('SET_USER', response.data);
            resolve(response.data);
          })
          .catch(error => {
            reject(error);
          });
      });
    }
  },
  getters: {
    isLoggedIn: state => state.isLoggedIn,
    currentUser: state => state.user
  }
}
