import { useLocation, Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from 'axios'
import { MapPin, Building2, Briefcase, Trophy, ChevronRight, Share2, Globe } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL;

export default function Recommendations() {
  const location = useLocation()

  const [jobs, setJobs] = useState(location.state?.jobs || [])
  const [skills, setSkills] = useState(location.state?.skills || [])
  const [loading, setLoading] = useState(false)

  // ✅ Fetch jobs if empty
  useEffect(() => {
    if (jobs.length === 0) {
      setLoading(true)

      axios.get(`${API_URL}/api/jobs`)
        .then(res => setJobs(res.data))
        .catch(err => console.error(err))
        .finally(() => setLoading(false))
    }
  }, [jobs.length])

  // ✅ Handle apply
  const handleInteraction = async (jobId, type) => {
    try {
      await axios.post(`${API_URL}/api/jobs/interaction`, null, {
        params: { job_id: jobId, type: type }
      })

      if (type === 'apply') {
        alert('Application submitted successfully!')
      }

    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="max-w-7xl mx-auto py-12 px-6 lg:px-8 space-y-12">

      {/* Header */}
      <div className="bg-slate-900 text-white p-10 rounded-3xl">
        <h1 className="text-4xl font-bold">
          Top Picks For You
        </h1>
      </div>

      {/* Skills */}
      {skills.length > 0 && (
        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="font-bold mb-3">Identified Skills</h2>
          <div className="flex flex-wrap gap-2">
            {skills.map(skill => (
              <span key={skill} className="px-3 py-1 bg-blue-100 rounded-lg">
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Loading */}
      {loading && <p>Loading jobs...</p>}

      {/* Jobs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        {jobs.map(job => (
          <div key={job.id} className="bg-white p-6 rounded-xl shadow">

            <h2 className="text-xl font-bold">{job.title}</h2>
            <p>{job.company}</p>
            <p className="text-sm text-gray-500">{job.location}</p>

            {job.explanation && (
              <p className="text-sm mt-2 italic">{job.explanation}</p>
            )}

            <button
              onClick={() => handleInteraction(job.id, 'apply')}
              className="mt-4 bg-black text-white px-4 py-2 rounded"
            >
              Apply
            </button>

          </div>
        ))}

      </div>
    </div>
  )
}