import axios from 'axios'

// Validate environment variable
const API_URL = import.meta.env.VITE_API_URL

if (!API_URL && import.meta.env.PROD) {
  console.error('VITE_API_URL environment variable is required in production!')
  throw new Error('Missing required environment variable: VITE_API_URL')
}

// Fallback to localhost only in development
const API_BASE_URL = API_URL || (import.meta.env.DEV ? 'http://localhost:5000' : '')

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 seconds timeout
    })

    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('labManagementAccessToken') || localStorage.getItem('accessToken')
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true

          try {
            const refreshToken = localStorage.getItem('labManagementRefreshToken') || localStorage.getItem('refreshToken')
            if (refreshToken) {
              const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {
                refreshToken,
              })
              
              localStorage.setItem('labManagementAccessToken', response.data.accessToken)
              localStorage.setItem('labManagementRefreshToken', response.data.refreshToken)
              
              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${response.data.accessToken}`
              }
              
              return this.client(originalRequest)
            }
          } catch (refreshError) {
            localStorage.removeItem('labManagementAccessToken')
            localStorage.removeItem('labManagementRefreshToken')
            localStorage.removeItem('labManagementUser')
            window.location.href = '/'
            return Promise.reject(refreshError)
          }
        }

        return Promise.reject(error)
      }
    )
  }

  setToken(token) {
    if (token) {
      this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      delete this.client.defaults.headers.common['Authorization']
    }
  }

  async get(url) {
    const response = await this.client.get(url)
    return response.data
  }

  async post(url, data) {
    const response = await this.client.post(url, data)
    return response.data
  }

  async put(url, data) {
    const response = await this.client.put(url, data)
    return response.data
  }

  async delete(url) {
    const response = await this.client.delete(url)
    return response.data
  }

  async patch(url, data) {
    const response = await this.client.patch(url, data)
    return response.data
  }
}

export const apiService = new ApiService()

// Mock data services for now - can be replaced with real API calls
const mockDelay = (ms = 50) => new Promise(resolve => setTimeout(resolve, ms))

// Simple cache mechanism
const cache = new Map()
const CACHE_TTL = 30000 // 30 seconds

const getCached = (key) => {
  const cached = cache.get(key)
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data
  }
  return null
}

const setCached = (key, data) => {
  cache.set(key, { data, timestamp: Date.now() })
}

const clearCache = (pattern) => {
  if (pattern) {
    for (const key of cache.keys()) {
      if (key.includes(pattern)) {
        cache.delete(key)
      }
    }
  } else {
    cache.clear()
  }
}

// Customers Service
export const customersService = {
  getAll: async () => {
    const cacheKey = 'customers:all'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const data = [
      { id: 1, companyName: 'TechCorp Industries', email: 'contact@techcorp.com' },
      { id: 2, companyName: 'ElectroSystems Ltd', email: 'info@electrosystems.com' },
      { id: 3, companyName: 'Digital Solutions Inc', email: 'hello@digitalsolutions.com' },
      { id: 4, companyName: 'Innovation Labs', email: 'contact@innovationlabs.com' },
    ]
    setCached(cacheKey, data)
    return data
  },
  getById: (id) => apiService.get(`/api/customers/${id}`),
  create: (data) => apiService.post('/api/customers', data),
  update: (id, data) => apiService.put(`/api/customers/${id}`, data),
  delete: (id) => apiService.delete(`/api/customers/${id}`),
}

// RFQs Service
export const rfqsService = {
  getAll: async () => {
    const cacheKey = 'rfqs:all'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const data = [
      { id: 1, customerId: 1, customerName: 'TechCorp Industries', product: 'EMC Testing Device', receivedDate: '2024-01-15', status: 'pending' },
      { id: 2, customerId: 2, customerName: 'ElectroSystems Ltd', product: 'RF Compliance Module', receivedDate: '2024-01-20', status: 'approved' },
    ]
    setCached(cacheKey, data)
    return data
  },
  getById: (id) => apiService.get(`/api/rfqs/${id}`),
  create: (data) => apiService.post('/api/rfqs', data),
}

// Estimations Service
export const estimationsService = {
  getAll: async () => {
    const cacheKey = 'estimations:all'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const data = []
    setCached(cacheKey, data)
    return data
  },
  getById: (id) => apiService.get(`/api/estimations/${id}`),
  create: (data) => apiService.post('/api/estimations', data),
  review: (id, data) => apiService.post(`/api/estimations/${id}/review`, data),
  getTestTypes: async () => {
    await mockDelay()
    return [
      { id: 1, name: 'EMC Testing', hsnCode: '9030', defaultRate: 5000 },
      { id: 2, name: 'RF Testing', hsnCode: '9030', defaultRate: 6000 },
      { id: 3, name: 'Safety Testing', hsnCode: '9030', defaultRate: 4500 },
    ]
  },
}

// Projects Service
export const projectsService = {
  getAll: async () => {
    const cacheKey = 'projects:all'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const data = [
      { id: 1, code: 'PROJ-001', name: 'EMC Testing - Project Alpha', clientId: 1, clientName: 'TechCorp Industries', status: 'active' },
      { id: 2, code: 'PROJ-002', name: 'RF Compliance Testing', clientId: 2, clientName: 'ElectroSystems Ltd', status: 'active' },
    ]
    setCached(cacheKey, data)
    return data
  },
  getById: (id) => apiService.get(`/api/projects/${id}`),
  create: (data) => apiService.post('/api/projects', data),
}

// Dashboard Service
export const dashboardService = {
  getSummary: async () => {
    const cacheKey = 'dashboard:summary'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const data = {
      instrumentStatuses: [
        { status: 'Active', count: 12 },
        { status: 'Maintenance', count: 2 },
        { status: 'Calibration', count: 1 },
      ],
      toDoItems: [
        { id: 1, title: 'Review Test Plan for PROJ-001', type: 'review', dueDate: '2024-01-25' },
        { id: 2, title: 'Complete Sample Analysis', type: 'analysis', dueDate: '2024-01-26' },
      ],
      billingProgress: {
        target: 5000000,
        current: 3200000,
        percentage: 64,
      },
    }
    setCached(cacheKey, data)
    return data
  },
}

// Export cache utilities for manual cache clearing
export { clearCache, setCached, getCached }

// Test Plans Service
export const testPlansService = {
  getAll: async (projectId) => {
    const cacheKey = projectId ? `testPlans:project:${projectId}` : 'testPlans:all'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const allPlans = [
      { 
        id: 1, 
        projectId: 1, 
        projectName: 'EMC Testing - Project Alpha', 
        name: 'EMC Compliance Test Plan', 
        description: 'Full EMC testing suite for electromagnetic compatibility', 
        testType: 'EMC', 
        status: 'Approved', 
        assignedEngineerName: 'John Doe',
        createdAt: '2024-01-15T10:00:00Z' 
      },
      { 
        id: 2, 
        projectId: 1, 
        projectName: 'EMC Testing - Project Alpha', 
        name: 'RF Emission Test Plan', 
        description: 'RF emission testing and compliance verification', 
        testType: 'RF', 
        status: 'InProgress', 
        assignedEngineerName: 'Jane Smith',
        createdAt: '2024-01-18T14:30:00Z' 
      },
      { 
        id: 3, 
        projectId: 2, 
        projectName: 'RF Compliance Testing', 
        name: 'Safety Certification Test', 
        description: 'Safety testing and certification process', 
        testType: 'Safety', 
        status: 'Completed', 
        assignedEngineerName: 'Mike Johnson',
        createdAt: '2024-01-10T09:00:00Z' 
      },
      { 
        id: 4, 
        projectId: 2, 
        projectName: 'RF Compliance Testing', 
        name: 'Environmental Stress Test', 
        description: 'Environmental stress testing under various conditions', 
        testType: 'Environmental', 
        status: 'Draft', 
        assignedEngineerName: 'Sarah Williams',
        createdAt: '2024-01-20T11:00:00Z' 
      },
    ]
    
    const data = projectId 
      ? allPlans.filter(plan => plan.projectId === parseInt(projectId))
      : allPlans
    setCached(cacheKey, data)
    return data
  },
  getById: (id) => apiService.get(`/api/test-plans/${id}`),
  create: (data) => apiService.post('/api/test-plans', data),
  update: (id, data) => apiService.put(`/api/test-plans/${id}`, data),
  delete: (id) => apiService.delete(`/api/test-plans/${id}`),
}

// Test Executions Service
export const testExecutionsService = {
  getAll: async () => {
    const cacheKey = 'testExecutions:all'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const data = []
    setCached(cacheKey, data)
    return data
  },
  getByTestPlan: (testPlanId) => apiService.get(`/api/test-executions?testPlanId=${testPlanId}`),
  getById: (id) => apiService.get(`/api/test-executions/${id}`),
  create: (data) => apiService.post('/api/test-executions', data),
  update: (id, data) => apiService.put(`/api/test-executions/${id}`, data),
  start: (id) => apiService.post(`/api/test-executions/${id}/start`, {}),
  complete: (id) => apiService.post(`/api/test-executions/${id}/complete`, {}),
}

// Test Results Service
export const testResultsService = {
  getAll: async () => {
    const cacheKey = 'testResults:all'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const data = []
    setCached(cacheKey, data)
    return data
  },
  getByExecution: (executionId) => apiService.get(`/api/test-results?executionId=${executionId}`),
  getById: (id) => apiService.get(`/api/test-results/${id}`),
  create: (data) => apiService.post('/api/test-results', data),
  update: (id, data) => apiService.put(`/api/test-results/${id}`, data),
}

// Samples Service
export const samplesService = {
  getAll: async (projectId) => {
    const cacheKey = projectId ? `samples:project:${projectId}` : 'samples:all'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const data = []
    setCached(cacheKey, data)
    return data
  },
  getById: (id) => apiService.get(`/api/samples/${id}`),
  create: (data) => apiService.post('/api/samples', data),
  update: (id, data) => apiService.put(`/api/samples/${id}`, data),
  delete: (id) => apiService.delete(`/api/samples/${id}`),
}

// TRFs Service
export const trfsService = {
  getAll: async (projectId) => {
    const cacheKey = projectId ? `trfs:project:${projectId}` : 'trfs:all'
    const cached = getCached(cacheKey)
    if (cached) return cached
    
    await mockDelay()
    const data = []
    setCached(cacheKey, data)
    return data
  },
  getById: (id) => apiService.get(`/api/trfs/${id}`),
  create: (data) => apiService.post('/api/trfs', data),
  update: (id, data) => apiService.put(`/api/trfs/${id}`, data),
  delete: (id) => apiService.delete(`/api/trfs/${id}`),
}

// Documents Service
export const documentsService = {
  getAll: () => apiService.get('/api/documents'),
  getById: (id) => apiService.get(`/api/documents/${id}`),
  create: (data) => apiService.post('/api/documents', data),
  update: (id, data) => apiService.put(`/api/documents/${id}`, data),
  delete: (id) => apiService.delete(`/api/documents/${id}`),
}

// Reports Service
export const reportsService = {
  getAll: () => apiService.get('/api/reports'),
  getById: (id) => apiService.get(`/api/reports/${id}`),
  generate: (data) => apiService.post('/api/reports/generate', data),
}

// Audits Service
export const auditsService = {
  getAll: () => apiService.get('/api/audits'),
  getById: (id) => apiService.get(`/api/audits/${id}`),
  create: (data) => apiService.post('/api/audits', data),
}

// NCRs Service
export const ncrsService = {
  getAll: () => apiService.get('/api/ncrs'),
  getById: (id) => apiService.get(`/api/ncrs/${id}`),
  create: (data) => apiService.post('/api/ncrs', data),
}

// Certifications Service
export const certificationsService = {
  getAll: () => apiService.get('/api/certifications'),
  getById: (id) => apiService.get(`/api/certifications/${id}`),
  create: (data) => apiService.post('/api/certifications', data),
}
