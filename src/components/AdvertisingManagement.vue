<template>
  <div class="advertising-management">
    <h1>Advertising Data Management</h1>
    
    <!-- Form for Adding New Entry -->
    <div class="add-entry-form">
      <h2>Add New Entry</h2>
      <form @submit.prevent="addAdvertisingEntry">
        <div class="form-group">
          <label>TV Advertising:</label>
          <input v-model.number="newEntry.TV" type="number" step="1.0" required>
        </div>
        <div class="form-group">
          <label>Radio Advertising:</label>
          <input v-model.number="newEntry.Radio" type="number" step="1.0" required>
        </div>
        <div class="form-group">
          <label>Newspaper Advertising:</label>
          <input v-model.number="newEntry.Newspaper" type="number" step="1.0" required>
        </div>
        <div class="form-group">
          <label>Sales:</label>
          <input v-model.number="newEntry.Sales" type="number" step="1.0" required>
        </div>
        <button type="submit">Add Entry</button>
      </form>
    </div>

    <!-- Advertising Data Table -->
    <div class="advertising-table">
      <h2>Advertising Entries</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>TV</th>
            <th>Radio</th>
            <th>Newspaper</th>
            <th>Sales</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in advertisingData" :key="entry.id">
            <td>{{ entry.id }}</td>
            <td>{{ entry.TV }}</td>
            <td>{{ entry.Radio }}</td>
            <td>{{ entry.Newspaper }}</td>
            <td>{{ entry.Sales }}</td>
            <td>
              <button @click="deleteEntry(entry.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Error Handling -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdvertisingManagement',
  data() {
    return {
      advertisingData: [],
      newEntry: {
        TV: 0,
        Radio: 0,
        Newspaper: 0,
        Sales: 0
      },
      error: null
    }
  },
  mounted() {
    this.fetchAdvertisingData();
  },
  methods: {
    async fetchAdvertisingData() {
      try {
        const response = await axios.get('/advertising');
        this.advertisingData = response.data;
        this.error = null;
      } catch (error) {
        this.error = `Failed to fetch advertising data: ${error.message}`;
        console.error('Error fetching data:', error);
      }
    },
    async addAdvertisingEntry() {
      try {
        // eslint-disable-next-line no-unused-vars
        const response = await axios.post('/advertising', this.newEntry); // Remove the semicolon under response to use it.
        // Reset form and refresh data
        this.newEntry = {
          TV: 0,
          Radio: 0,
          Newspaper: 0,
          Sales: 0
        };
        
        // Refresh the table
        await this.fetchAdvertisingData();
        
        this.error = null;
      } catch (error) {
        this.error = `Failed to add entry: ${error.response?.data?.error || error.message}`;
        console.error('Error adding entry:', error);
      }
    },
    async deleteEntry(id) {
      try {
        await axios.delete(`/advertising/${id}`);
        
        // Refresh the table
        await this.fetchAdvertisingData();
        
        this.error = null;
      } catch (error) {
        this.error = `Failed to delete entry: ${error.response?.data?.error || error.message}`;
        console.error('Error deleting entry:', error);
      }
    }
  }
}
</script>

<style scoped>
.advertising-management {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.add-entry-form {
  background-color: #f4f4f4;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 10px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table th, table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

table th {
  background-color: #f2f2f2;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>