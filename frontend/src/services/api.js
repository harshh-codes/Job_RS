import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

export const jobApi = {
  getAllJobs: () => api.get('/jobs/'),
  getRecommendations: (resumeText) => api.post('/jobs/recommend', null, {
    params: { resume_text: resumeText }
  }),
  uploadResume: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/jobs/upload-resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export default api;
