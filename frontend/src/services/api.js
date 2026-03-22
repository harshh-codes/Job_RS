import axios from 'axios';

// Backend URL from environment variables
// Ensure VITE_API_URL does NOT have a trailing slash for consistency
const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  // Using a trailing slash for baseURL and relative paths for endpoints is the safest approach in Axios
  baseURL: `${API_URL}/api/jobs/`,
});

export const jobApi = {
  // Get all jobs (resolves to: /api/jobs/)
  getJobs: () => api.get(''),
  
  // Get recommendations for text (resolves to: /api/jobs/recommend)
  getRecommendations: (resumeText) => api.post('recommend', null, {
    params: { resume_text: resumeText }
  }),
  
  // Upload resume PDF (resolves to: /api/jobs/upload-resume)
  uploadResume: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('upload-resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  
  // Record interaction (click/apply) (resolves to: /api/jobs/interaction)
  recordInteraction: (jobId, type) => api.post('interaction', null, {
    params: { job_id: jobId, type: type }
  }),
};

export default api;