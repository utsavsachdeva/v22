// Function to fetch and display user data
function fetchAndDisplayUsers() {
    axios.get('/api/users')
      .then(response => {
        const users = response.data;
        const userTableBody = document.querySelector('#user-table tbody');
        userTableBody.innerHTML = ''; // Clear existing rows
  
        users.forEach(user => {
          const row = userTableBody.insertRow();
          const cells = [user.id, user.username, user.email, user.role, user.is_active ? 'Yes' : 'No'];
          cells.forEach(cellData => {
            const cell = row.insertCell();
            cell.textContent = cellData;
          });
  
          // Actions cell
          const actionsCell = row.insertCell();
  
          // Edit button
          const editButton = document.createElement('button');
          editButton.classList.add('btn', 'btn-sm', 'btn-warning', 'mr-2');
          editButton.textContent = 'Edit';
          editButton.addEventListener('click', () => editUser(user.id));
          actionsCell.appendChild(editButton);
  
          // Delete button
          const deleteButton = document.createElement('button');
          deleteButton.classList.add('btn', 'btn-sm', 'btn-danger', 'mr-2');
          deleteButton.textContent = 'Delete';
          deleteButton.addEventListener('click', () => deleteUser(user.id));
          actionsCell.appendChild(deleteButton);
  
          // Activate/Deactivate button (only for non-admin users)
          if (user.role !== 'admin') {
            const toggleButton = document.createElement('button');
            toggleButton.classList.add('btn', 'btn-sm', user.is_active ? 'btn-secondary' : 'btn-success');
            toggleButton.textContent = user.is_active ? 'Deactivate' : 'Activate';
            toggleButton.addEventListener('click', () => toggleUserActive(user.id));
            actionsCell.appendChild(toggleButton);
          }
        });
      })
      .catch(error => {
        console.error('Error fetching users:', error);
        // Display an error message on the dashboard (e.g., using an alert)
        alert('An error occurred while fetching users. Please try again later.');
      });
  }
  
  // Function to fetch and display campaign data
  function fetchAndDisplayCampaigns() {
    axios.get('/api/campaigns')
      .then(response => {
        const campaigns = response.data;
        const campaignTableBody = document.querySelector('#campaign-table tbody');
        campaignTableBody.innerHTML = ''; 
  
        campaigns.forEach(campaign => {
          const row = campaignTableBody.insertRow();
          const cells = [
            campaign.id, 
            campaign.name, 
            campaign.sponsor.username, 
            '$' + campaign.budget.toFixed(2), // Format budget with currency
            campaign.visibility
          ];
          cells.forEach(cellData => {
            const cell = row.insertCell();
            cell.textContent = cellData;
          });
  
          // Actions cell
          const actionsCell = row.insertCell();
  
          // View button
          const viewButton = document.createElement('button');
          viewButton.classList.add('btn', 'btn-sm', 'btn-info', 'mr-2');
          viewButton.textContent = 'View';
          viewButton.addEventListener('click', () => viewCampaignDetails(campaign.id));
          actionsCell.appendChild(viewButton);
  
          // Edit button
          const editButton = document.createElement('button');
          editButton.classList.add('btn', 'btn-sm', 'btn-warning', 'mr-2');
          editButton.textContent = 'Edit';
          editButton.addEventListener('click', () => editCampaign(campaign.id));
          actionsCell.appendChild(editButton);
  
          // Delete button
          const deleteButton = document.createElement('button');
          deleteButton.classList.add('btn', 'btn-sm', 'btn-danger');
          deleteButton.textContent = 'Delete';
          deleteButton.addEventListener('click', () => deleteCampaign(campaign.id));
          actionsCell.appendChild(deleteButton);
        });
      })
      .catch(error => {
        console.error('Error fetching campaigns:', error);
        alert('An error occurred while fetching campaigns. Please try again later.');
      });
  }
  
  // Function to fetch and display ad request data
  function fetchAndDisplayAdRequests() {
    axios.get('/api/ad_requests') // You might need to adjust the endpoint based on your backend implementation
      .then(response => {
        const adRequests = response.data;
        const adRequestTableBody = document.querySelector('#ad-request-table tbody');
        adRequestTableBody.innerHTML = ''; 
  
        adRequests.forEach(adRequest => {
          const row = adRequestTableBody.insertRow();
          const cells = [
            adRequest.id, 
            adRequest.campaign.name, 
            adRequest.influencer.username, 
            '$' + adRequest.payment_amount.toFixed(2), 
            adRequest.status
          ];
          cells.forEach(cellData => {
            const cell = row.insertCell();
            cell.textContent = cellData;
          });
  
          // Actions cell
          const actionsCell = row.insertCell();
  
          // View button
          const viewButton = document.createElement('button');
          viewButton.classList.add('btn', 'btn-sm', 'btn-info', 'mr-2');
          viewButton.textContent = 'View';
          viewButton.addEventListener('click', () => viewAdRequestDetails(adRequest.id));
          actionsCell.appendChild(viewButton);
  
          // Delete button
          const deleteButton = document.createElement('button');
          deleteButton.classList.add('btn', 'btn-sm', 'btn-danger');
          deleteButton.textContent = 'Delete';
          deleteButton.addEventListener('click', () => deleteAdRequest(adRequest.id));
          actionsCell.appendChild(deleteButton);
        });
      })
      .catch(error => {
        console.error('Error fetching ad requests:', error);
        alert('An error occurred while fetching ad requests. Please try again later.');
      });
  }
  
  // Call the functions to fetch and display data when the page loads
  window.onload = () => {
    fetchAndDisplayUsers();
    fetchAndDisplayCampaigns();
    fetchAndDisplayAdRequests();
  };
  
// ... (other functions in admin_dashboard.js)

// Admin action functions 

function editUser(userId) {
    // 1. Fetch user data from the API
    axios.get(`/api/users/${userId}`)
      .then(response => {
        const user = response.data;
  
        // 2. Populate the modal form with the user data
        $('#editUserModal #edit-username').val(user.username);
        $('#editUserModal #edit-email').val(user.email);
        $('#editUserModal #edit-role').val(user.role);
        $('#editUserModal #edit-is-active').prop('checked', user.is_active);
  
        // 3. Show the modal
        $('#editUserModal').modal('show');
  
        // 4. Handle form submission (within the modal)
        $('#edit-user-form').submit(function(event) {
          event.preventDefault();
  
          // Get the updated data from the form
          const updatedUserData = {
            username: $('#edit-username').val(),
            email: $('#edit-email').val(),
            role: $('#edit-role').val(),
            is_active: $('#edit-is-active').is(':checked')
          };
  
          // Send PUT request to update the user
          axios.put(`/api/users/${userId}`, updatedUserData)
            .then(() => {
              // Handle success
              $('#editUserModal').modal('hide');
              fetchAndDisplayUsers(); // Refresh the user table
              alert('User updated successfully!');
            })
            .catch(error => {
              console.error('Error updating user:', error);
              // Handle error, display an error message in the modal (you might need to add an error display area in your modal)
              $('#editUserModal .modal-body').append('<div class="alert alert-danger">An error occurred while updating the user.</div>');
            });
        });
      })
      .catch(error => {
        console.error('Error fetching user data for edit:', error);
        // Handle error, display an error message on the dashboard
        alert('An error occurred while fetching user data.');
      });
  }
  
  
  function deleteUser(userId) {
    // 1. Confirm deletion with the user
    if (confirm('Are you sure you want to delete this user?')) {
      // 2. Send DELETE request to the API
      axios.delete(`/api/users/${userId}`)
        .then(() => {
          // 3. Handle success (refresh the user table)
          fetchAndDisplayUsers();
          alert('User deleted successfully!');
        })
        .catch(error => {
          console.error('Error deleting user:', error);
          // Handle error, display an error message
          alert('An error occurred while deleting the user. Please try again later.');
        });
    }
  }
  
  function toggleUserActive(userId) {
    // 1. Send PUT request to the API to toggle the user's active status
    axios.put(`/api/users/${userId}/activate`) 
      .then(response => {
        // 2. Handle success (update the user table)
        fetchAndDisplayUsers();
        alert(response.data.message); 
      })
      .catch(error => {
        console.error('Error toggling user active status:', error);
        // Handle error, display an error message
        alert('An error occurred while updating the user\'s status. Please try again later.');
      });
  }
  
  // ... similar functions for campaigns and ad requests
// ... other functions in admin_dashboard.js

// Admin action functions for Campaigns

function viewCampaignDetails(campaignId) {
    // Navigate to the campaign details page (you'll need to set up the route in your Vue.js router)
    this.$router.push({ name: 'CampaignDetails', params: { id: campaignId } });
  }
  
  function editCampaign(campaignId) {
    // 1. Fetch campaign data from the API
    axios.get(`/api/campaigns/${campaignId}`)
      .then(response => {
        const campaign = response.data;
  
        // 2. Populate the modal form with the campaign data
        $('#editCampaignModal #edit-campaign-name').val(campaign.name);
        $('#editCampaignModal #edit-campaign-description').val(campaign.description);
        $('#editCampaignModal #edit-campaign-start_date').val(campaign.start_date);
        $('#editCampaignModal #edit-campaign-end_date').val(campaign.end_date);
        $('#editCampaignModal #edit-campaign-budget').val(campaign.budget);
        $('#editCampaignModal #edit-campaign-visibility').val(campaign.visibility);
        $('#editCampaignModal #edit-campaign-goals').val(campaign.goals);
  
        // 3. Show the modal
        $('#editCampaignModal').modal('show');
  
        // 4. Handle form submission (within the modal)
        $('#edit-campaign-form').submit(function(event) {
          event.preventDefault();
  
          // Get the updated data from the form
          const updatedCampaignData = {
            name: $('#edit-campaign-name').val(),
            description: $('#edit-campaign-description').val(),
            start_date: $('#edit-campaign-start_date').val(),
            end_date: $('#edit-campaign-end_date').val(),
            budget: $('#edit-campaign-budget').val(),
            visibility: $('#edit-campaign-visibility').val(),
            goals: $('#edit-campaign-goals').val()
          };
  
          // Send PUT request to update the campaign
          axios.put(`/api/campaigns/${campaignId}`, updatedCampaignData)
            .then(() => {
              // Handle success
              $('#editCampaignModal').modal('hide');
              fetchAndDisplayCampaigns(); 
              alert('Campaign updated successfully!');
            })
            .catch(error => {
              console.error('Error updating campaign:', error);
              // Display error in the modal
              let errorMessage = 'An error occurred while updating the campaign.';
              if (error.response && error.response.data && error.response.data.message) {
                errorMessage = error.response.data.message;
              }
              $('#editCampaignModal .modal-body').append(`<div class="alert alert-danger">${errorMessage}</div>`);
            });
        });
      })
      .catch(error => {
        console.error('Error fetching campaign data for edit:', error);
        alert('An error occurred while fetching campaign data.');
      });
  }
  
  
  
  function deleteCampaign(campaignId) {
    if (confirm('Are you sure you want to delete this campaign?')) {
      axios.delete(`/api/campaigns/${campaignId}`)
        .then(() => {
          fetchAndDisplayCampaigns();
          alert('Campaign deleted successfully!');
        })
        .catch(error => {
          console.error('Error deleting campaign:', error);
          alert('An error occurred while deleting the campaign. Please try again later.');
        });
    }
  }
  
  // ... similar functions for ad requests
// ... other functions in admin_dashboard.js

// Admin action functions for Ad Requests

function viewAdRequestDetails(adRequestId) {
    // Navigate to the ad request details page (you'll need to set up the route in your Vue.js router)
    this.$router.push({ name: 'AdRequestDetails', params: { id: adRequestId } });
  }
  
  function deleteAdRequest(adRequestId) {
    if (confirm('Are you sure you want to delete this ad request?')) {
      axios.delete(`/api/ad_requests/${adRequestId}`)
        .then(() => {
          fetchAndDisplayAdRequests();
          alert('Ad Request deleted successfully!');
        })
        .catch(error => {
          console.error('Error deleting ad request:', error);
          alert('An error occurred while deleting the ad request.');
        });
    }
  }
  
  // ... other functions
  function handleSearch(query, searchType) { // Add searchType as an argument
    if (!query) {
      // If the query is empty, reset the table to display all data
      if (searchType === 'campaigns') {
        fetchAndDisplayCampaigns();
      } else if (searchType === 'influencers') {
        fetchAndDisplayInfluencers();
      } 
      return; 
    }
  
    // Make API calls to your Flask backend to perform the search
    // You'll need to adjust the endpoints and search logic based on your backend implementation
    let apiEndpoint;
    if (searchType === 'campaigns') {
      apiEndpoint = `/api/search/campaigns?q=${query}`;
    } else if (searchType === 'influencers') {
      apiEndpoint = `/api/search/influencers?q=${query}`;
    } else {
      console.error('Invalid search type:', searchType);
      return; // Or handle the error in a more user-friendly way
    }
  
    axios.get(apiEndpoint)
      .then(response => {
        const searchResults = response.data;
  
        // Update the relevant table with the search results
        if (searchType === 'campaigns') {
          updateCampaignTable(searchResults);
        } else if (searchType === 'influencers') {
          updateUserTable(searchResults);
        }
      })
      .catch(error => {
        console.error('Error performing search:', error);
        // Display an error message on the dashboard
      });
  }      
  // ... other functions in admin_dashboard.js

// Helper functions to update tables
function updateUserTable(users) {
    const userTableBody = document.querySelector('#user-table tbody');
    userTableBody.innerHTML = ''; // Clear existing rows
  
    users.forEach(user => {
      const row = userTableBody.insertRow();
      const cells = [user.id, user.username, user.email, user.role, user.is_active ? 'Yes' : 'No'];
      cells.forEach(cellData => {
        const cell = row.insertCell();
        cell.textContent = cellData;
      });
  
      // Actions cell
      const actionsCell = row.insertCell();
  
      // Edit button
      const editButton = document.createElement('button');
      editButton.classList.add('btn', 'btn-sm', 'btn-warning', 'mr-2');
      editButton.textContent = 'Edit';
      editButton.addEventListener('click', () => editUser(user.id));
      actionsCell.appendChild(editButton);
  
      // Delete button
      const deleteButton = document.createElement('button');
      deleteButton.classList.add('btn', 'btn-sm', 'btn-danger', 'mr-2');
      deleteButton.textContent = 'Delete';
      deleteButton.addEventListener('click', () => deleteUser(user.id));
      actionsCell.appendChild(deleteButton);
  
      // Activate/Deactivate button (only for non-admin users)
      if (user.role !== 'admin') {
        const toggleButton = document.createElement('button');
        toggleButton.classList.add('btn', 'btn-sm', user.is_active ? 'btn-secondary' : 'btn-success');
        toggleButton.textContent = user.is_active ? 'Deactivate' : 'Activate';
        toggleButton.addEventListener('click', () => toggleUserActive(user.id));
        actionsCell.appendChild(toggleButton);
      }
    });
  }
  
  function updateCampaignTable(campaigns) {
    const campaignTableBody = document.querySelector('#campaign-table tbody');
    campaignTableBody.innerHTML = ''; // Clear existing rows
  
    campaigns.forEach(campaign => {
      const row = campaignTableBody.insertRow();
      const cells = [
        campaign.id, 
        campaign.name, 
        campaign.sponsor.username, 
        '$' + campaign.budget.toFixed(2), // Format budget with currency
        campaign.visibility
      ];
      cells.forEach(cellData => {
        const cell = row.insertCell();
        cell.textContent = cellData;
      });
  
      // Actions cell
      const actionsCell = row.insertCell();
  
      // View button
      const viewButton = document.createElement('button');
      viewButton.classList.add('btn', 'btn-sm', 'btn-info', 'mr-2');
      viewButton.textContent = 'View';
      viewButton.addEventListener('click', () => viewCampaignDetails(campaign.id));
      actionsCell.appendChild(viewButton);
  
      // Edit button
      const editButton = document.createElement('button');
      editButton.classList.add('btn', 'btn-sm', 'btn-warning', 'mr-2');
      editButton.textContent = 'Edit';
      editButton.addEventListener('click', () => editCampaign(campaign.id));
      actionsCell.appendChild(editButton);
  
      // Delete button
      const deleteButton = document.createElement('button');
      deleteButton.classList.add('btn', 'btn-sm', 'btn-danger');
      deleteButton.textContent = 'Delete';
      deleteButton.addEventListener('click', () => deleteCampaign(campaign.id));
      actionsCell.appendChild(deleteButton);
    });
  }
  
  // ... other functions
  