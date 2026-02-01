import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';
const BASE_URL = `${API_URL}/scope-management`;

const scopeManagementService = {
    // --- Composite Data ---
    getAllData: async () => {
        const response = await axios.get(`${BASE_URL}/all`);
        return response.data;
    },

    // --- Global Settings ---
    updateSettings: async (data) => {
        const response = await axios.put(`${BASE_URL}/settings`, data);
        return response.data;
    },

    // --- ILC Programmes ---
    createILC: async (data) => {
        const response = await axios.post(`${BASE_URL}/ilc`, data);
        return response.data;
    },
    updateILC: async (id, data) => {
        const response = await axios.put(`${BASE_URL}/ilc/${id}`, data);
        return response.data;
    },
    deleteILC: async (id) => {
        const response = await axios.delete(`${BASE_URL}/ilc/${id}`);
        return response.data;
    },

    // --- Lab Scope ---
    createScope: async (data) => {
        const response = await axios.post(`${BASE_URL}/scope`, data);
        return response.data;
    },
    updateScope: async (id, data) => {
        const response = await axios.put(`${BASE_URL}/scope/${id}`, data);
        return response.data;
    },
    deleteScope: async (id) => {
        const response = await axios.delete(`${BASE_URL}/scope/${id}`);
        return response.data;
    },

    // --- Equipment ---
    createEquipment: async (data) => {
        const response = await axios.post(`${BASE_URL}/equipment`, data);
        return response.data;
    },
    updateEquipment: async (id, data) => {
        const response = await axios.put(`${BASE_URL}/equipment/${id}`, data);
        return response.data;
    },
    deleteEquipment: async (id) => {
        const response = await axios.delete(`${BASE_URL}/equipment/${id}`);
        return response.data;
    },

    // --- Scope Tests ---
    createTest: async (data) => {
        const response = await axios.post(`${BASE_URL}/test`, data);
        return response.data;
    },
    updateTest: async (id, data) => {
        const response = await axios.put(`${BASE_URL}/test/${id}`, data);
        return response.data;
    },
    deleteTest: async (id) => {
        const response = await axios.delete(`${BASE_URL}/test/${id}`);
        return response.data;
    },

    // --- Facilities Available ---
    createFacilityAvailable: async (data) => {
        const response = await axios.post(`${BASE_URL}/facility-available`, data);
        return response.data;
    },
    updateFacilityAvailable: async (id, data) => {
        const response = await axios.put(`${BASE_URL}/facility-available/${id}`, data);
        return response.data;
    },
    deleteFacilityAvailable: async (id) => {
        const response = await axios.delete(`${BASE_URL}/facility-available/${id}`);
        return response.data;
    },

    // --- Facilities Not Available ---
    createFacilityNotAvailable: async (data) => {
        const response = await axios.post(`${BASE_URL}/facility-not-available`, data);
        return response.data;
    },
    updateFacilityNotAvailable: async (id, data) => {
        const response = await axios.put(`${BASE_URL}/facility-not-available/${id}`, data);
        return response.data;
    },
    deleteFacilityNotAvailable: async (id) => {
        const response = await axios.delete(`${BASE_URL}/facility-not-available/${id}`);
        return response.data;
    },

    // --- Reference Material ---
    createReferenceMaterial: async (data) => {
        const response = await axios.post(`${BASE_URL}/reference-material`, data);
        return response.data;
    },
    updateReferenceMaterial: async (id, data) => {
        const response = await axios.put(`${BASE_URL}/reference-material/${id}`, data);
        return response.data;
    },
    deleteReferenceMaterial: async (id) => {
        const response = await axios.delete(`${BASE_URL}/reference-material/${id}`);
        return response.data;
    },

    // --- Exclusions ---
    createExclusion: async (data) => {
        const response = await axios.post(`${BASE_URL}/exclusion`, data);
        return response.data;
    },
    updateExclusion: async (id, data) => {
        const response = await axios.put(`${BASE_URL}/exclusion/${id}`, data);
        return response.data;
    },
    deleteExclusion: async (id) => {
        const response = await axios.delete(`${BASE_URL}/exclusion/${id}`);
        return response.data;
    },

    // --- Testing Charges ---
    createTestingCharge: async (data) => {
        const response = await axios.post(`${BASE_URL}/testing-charge`, data);
        return response.data;
    },
    updateTestingCharge: async (id, data) => {
        const response = await axios.put(`${BASE_URL}/testing-charge/${id}`, data);
        return response.data;
    },
    deleteTestingCharge: async (id) => {
        const response = await axios.delete(`${BASE_URL}/testing-charge/${id}`);
        return response.data;
    },
};

export default scopeManagementService;
