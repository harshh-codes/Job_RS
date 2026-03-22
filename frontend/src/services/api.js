const API_URL = import.meta.env.VITE_API_URL;

// Get all jobs
export const getJobs = async () => {
  const response = await fetch(`${API_URL}/api/jobs`);
  return response.json();
};

// Record interaction
export const recordInteraction = async (jobId, type) => {
  const response = await fetch(
    `${API_URL}/api/jobs/interaction?job_id=${jobId}&type=${type}`,
    {
      method: "POST",
    }
  );

  return response.json();
};