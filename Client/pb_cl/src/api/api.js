// api.js - Simplificat pentru ChefMind
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

// Funcție pentru gestionarea erorilor
const handleApiError = (error, operation) => {
  if (error.response) {
    // Eroare de la server cu răspuns
    console.error(`${operation} failed: ${error.response.status} - ${error.response.data?.message || error.response.statusText}`);
    throw error;
  } else if (error.request) {
    // Cererea a fost făcută dar nu s-a primit răspuns
    console.error(`${operation} failed: No response received`);
    throw new Error('Server did not respond. Please check your connection.');
  } else {
    // Ceva a cauzat o eroare la configurarea cererii
    console.error(`${operation} error: ${error.message}`);
    throw error;
  }
};

// ChefMind API calls
export const processMessage = async (messageData) => {
  try {
    if (!messageData) {
      throw new Error("Message data is required");
    }

    const response = await axios.post(`${API_URL}/process-message`, messageData);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Process message');
  }
};

// Verifică starea API-ului
export const checkApiStatus = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/`);
    return response.data;
  } catch (error) {
    handleApiError(error, 'Check API status');
  }
};