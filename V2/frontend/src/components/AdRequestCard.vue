<template>
  <div class="card mb-3">
    <div class="card-body">
      <h5 class="card-title">{{ adRequest.campaign.name }}</h5>
      <p class="card-text">
        <strong>Influencer:</strong> {{ adRequest.influencer.username }}
      </p>
      <p class="card-text">
        <strong>Message:</strong> {{ adRequest.message }}
      </p>
      <p class="card-text">
        <strong>Requirements:</strong> {{ adRequest.requirements }}
      </p>
      <p class="card-text">
        <strong>Payment:</strong> ${{ adRequest.payment_amount.toFixed(2) }} 
      </p>
      <p class="card-text">
        <strong>Status:</strong>
        <span :class="`badge badge-${statusBadgeClass}`">{{ adRequest.status }}</span>
      </p>

      <div v-if="currentUser.role === 'sponsor' && adRequest.status === 'pending'">
        <button class="btn btn-success mr-2" @click="acceptAdRequest">Accept</button>
        <button class="btn btn-danger" @click="rejectAdRequest">Reject</button>
      </div>
      <div v-else-if="currentUser.role === 'influencer' && adRequest.status === 'pending'">
        <button class="btn btn-success mr-2" @click="acceptAdRequest">Accept</button>
        <button class="btn btn-warning mr-2" @click="showNegotiationModal = true">Negotiate</button>
        <button class="btn btn-danger" @click="rejectAdRequest">Reject</button>

        <div v-if="showNegotiationModal" class="modal" tabindex="-1" role="dialog">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Negotiate Payment</h5>
                <button type="button" class="close" @click="showNegotiationModal = false">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <div class="form-group">
                  <label for="newPaymentAmount">New Payment Amount:</label>
                  <input type="number" id="newPaymentAmount" v-model.number="newPaymentAmount" class="form-control" required>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="showNegotiationModal = false">Close</button>
                <button type="button" class="btn btn-primary" @click="sendNegotiationRequest">Send Request</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdRequestCard',
  props: {
    adRequest: {
      type: Object,
      required: true
    },
    currentUser: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      showNegotiationModal: false,
      newPaymentAmount: this.adRequest.payment_amount 
    };
  },
  computed: {
    statusBadgeClass() {
      switch (this.adRequest.status) {
        case 'pending': return 'secondary';
        case 'accepted': return 'success';
        case 'rejected': return 'danger';
        case 'negotiating': return 'warning';
        default: return 'light';
      }
    }
  },
  methods: {
    acceptAdRequest() {
      axios.put(`/api/ad_requests/${this.adRequest.id}`, { status: 'accepted' })
        .then(() => {
          this.adRequest.status = 'accepted'; 
          this.$emit('adRequestAccepted', this.adRequest.id); 
          // Show a success message 
          this.$emit('showSuccess', 'Ad request accepted successfully!');
        })
        .catch(error => {
          console.error('Error accepting ad request:', error);
          // Display an error message to the user
          this.$emit('showError', 'An error occurred while accepting the ad request. Please try again later.');
        });},
    

        rejectAdRequest() {
      axios.put(`/api/ad_requests/${this.adRequest.id}`, { status: 'rejected' })
        .then(() => {
          this.adRequest.status = 'rejected';
          this.$emit('adRequestRejected', this.adRequest.id);
          this.$emit('showSuccess', 'Ad request rejected.');
        })
        .catch(error => {
          console.error('Error rejecting ad request:', error);
          this.$emit('showError', 'An error occurred while rejecting the ad request. Please try again later.');
        });
    },



    sendNegotiationRequest() {
      if (!this.newPaymentAmount || isNaN(this.newPaymentAmount) || this.newPaymentAmount <= 0) {
        alert("Please enter a valid positive number for the payment amount.");
        return;
      }

      axios.put(`/api/ad_requests/${this.adRequest.id}`, {
        payment_amount: this.newPaymentAmount,
        status: 'negotiating'
      })
        .then(() => {
          this.$emit('adRequestNegotiationStarted', this.adRequest.id, this.newPaymentAmount);
          this.$emit('showSuccess', 'Negotiation initiated. Waiting for sponsor response.');
          this.showNegotiationModal = false; 
        })
        .catch(error => {
          console.error('Error initiating negotiation:', error);
          this.$emit('showError', 'An error occurred while initiating negotiation. Please try again later.');
        });
    }
  }
}
</script>
