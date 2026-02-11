import api from './api';

const BASE_URL = '/scope-management';

const scopeManagementService = {
    // --- Composite Data ---
    getAllData: async () => {
        const response = await api.get(`${BASE_URL}/all`);
        return response; // api.js interceptor already returns response.data
    },

    // --- Global Settings ---
    updateSettings: async (data) => {
        const response = await api.put(`${BASE_URL}/settings`, data);
        return response;
    },

    // --- ILC Programmes ---
    createILC: async (data) => {
        const response = await api.post(`${BASE_URL}/ilc`, data);
        return response;
    },
    updateILC: async (id, data) => {
        const response = await api.put(`${BASE_URL}/ilc/${id}`, data);
        return response;
    },
    deleteILC: async (id) => {
        const response = await api.delete(`${BASE_URL}/ilc/${id}`);
        return response;
    },

    // --- Lab Scope ---
    createScope: async (data) => {
        const response = await api.post(`${BASE_URL}/scope`, data);
        return response;
    },
    updateScope: async (id, data) => {
        const response = await api.put(`${BASE_URL}/scope/${id}`, data);
        return response;
    },
    deleteScope: async (id) => {
        const response = await api.delete(`${BASE_URL}/scope/${id}`);
        return response;
    },

    // --- Equipment ---
    createEquipment: async (data) => {
        const response = await api.post(`${BASE_URL}/equipment`, data);
        return response;
    },
    updateEquipment: async (id, data) => {
        const response = await api.put(`${BASE_URL}/equipment/${id}`, data);
        return response;
    },
    deleteEquipment: async (id) => {
        const response = await api.delete(`${BASE_URL}/equipment/${id}`);
        return response;
    },

    // --- Scope Tests ---
    createTest: async (data) => {
        const response = await api.post(`${BASE_URL}/test`, data);
        return response;
    },
    updateTest: async (id, data) => {
        const response = await api.put(`${BASE_URL}/test/${id}`, data);
        return response;
    },
    deleteTest: async (id) => {
        const response = await api.delete(`${BASE_URL}/test/${id}`);
        return response;
    },

    // --- Facilities Available ---
    createFacilityAvailable: async (data) => {
        const response = await api.post(`${BASE_URL}/facility-available`, data);
        return response;
    },
    updateFacilityAvailable: async (id, data) => {
        const response = await api.put(`${BASE_URL}/facility-available/${id}`, data);
        return response;
    },
    deleteFacilityAvailable: async (id) => {
        const response = await api.delete(`${BASE_URL}/facility-available/${id}`);
        return response;
    },

    // --- Facilities Not Available ---
    createFacilityNotAvailable: async (data) => {
        const response = await api.post(`${BASE_URL}/facility-not-available`, data);
        return response;
    },
    updateFacilityNotAvailable: async (id, data) => {
        const response = await api.put(`${BASE_URL}/facility-not-available/${id}`, data);
        return response;
    },
    deleteFacilityNotAvailable: async (id) => {
        const response = await api.delete(`${BASE_URL}/facility-not-available/${id}`);
        return response;
    },

    // --- Reference Material ---
    createReferenceMaterial: async (data) => {
        const response = await api.post(`${BASE_URL}/reference-material`, data);
        return response;
    },
    updateReferenceMaterial: async (id, data) => {
        const response = await api.put(`${BASE_URL}/reference-material/${id}`, data);
        return response;
    },
    deleteReferenceMaterial: async (id) => {
        const response = await api.delete(`${BASE_URL}/reference-material/${id}`);
        return response;
    },

    // --- Exclusions ---
    createExclusion: async (data) => {
        const response = await api.post(`${BASE_URL}/exclusion`, data);
        return response;
    },
    updateExclusion: async (id, data) => {
        const response = await api.put(`${BASE_URL}/exclusion/${id}`, data);
        return response;
    },
    deleteExclusion: async (id) => {
        const response = await api.delete(`${BASE_URL}/exclusion/${id}`);
        return response;
    },

    // --- Testing Charges ---
    createTestingCharge: async (data) => {
        const response = await api.post(`${BASE_URL}/testing-charge`, data);
        return response;
    },
    updateTestingCharge: async (id, data) => {
        const response = await api.put(`${BASE_URL}/testing-charge/${id}`, data);
        return response;
    },
    deleteTestingCharge: async (id) => {
        const response = await api.delete(`${BASE_URL}/testing-charge/${id}`);
        return response;
    },
};

export default scopeManagementService;
