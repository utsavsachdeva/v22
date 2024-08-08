import Vue from 'vue'
import VueRouter from 'vue-router'

// Import your views/components here
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import Campaigns from '../views/Campaigns.vue'
import Influencers from '../views/Influencers.vue'
import Profile from '../views/Profile.vue'
import Reports from '../views/Reports.vue'
import CampaignDetails from '../views/CampaignDetails.vue'
import InfluencerProfile from '../views/InfluencerProfile.vue'
import CampaignSearchResults from '../views/CampaignSearchResults.vue'
import InfluencerSearchResults from '../views/InfluencerSearchResults.vue'
import Admin from '../views/Admin.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true } // Requires authentication
  },
  {
    path: '/campaigns',
    name: 'Campaigns',
    component: Campaigns
  },
  {
    path: '/influencers',
    name: 'Influencers',
    component: Influencers
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports,
    meta: { requiresAuth: true, allowedRoles: ['sponsor'] } // Sponsor only
  },
  {
    path: '/campaigns/:id', // Dynamic route for campaign details
    name: 'CampaignDetails',
    component: CampaignDetails
  },
  {
    path: '/influencers/:id', // Dynamic route for influencer profile
    name: 'InfluencerProfile',
    component: InfluencerProfile
  },
  {
    path: '/search/campaigns',
    name: 'CampaignSearchResults',
    component: CampaignSearchResults
  },
  {
    path: '/search/influencers',
    name: 'InfluencerSearchResults',
    component: InfluencerSearchResults
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, allowedRoles: ['admin'] } // Admin only
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// Navigation guards (optional)
router.beforeEach((to, from, next) => {
  // ... (Implement authentication and authorization checks here if needed)
})

export default router
