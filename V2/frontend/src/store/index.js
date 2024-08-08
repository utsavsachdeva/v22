import { createStore } from 'vuex'

// Import modules
import auth from './auth' 
import campaigns from './campaigns'
import adRequests from './adRequests'

export default createStore({
  modules: {
    auth,
    campaigns,
    adRequests
  }
})
