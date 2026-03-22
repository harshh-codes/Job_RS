import { useLocation, Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from 'axios'
import { MapPin, Building2, ExternalLink, Briefcase, Trophy, ChevronRight, Share2, Globe } from 'lucide-react'

export default function Recommendations() {
  const location = useLocation()
  const [jobs, setJobs] = useState(location.state?.jobs || [])
  const [skills, setSkills] = useState(location.state?.skills || [])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // If we have no results, fetch all jobs as fallback
    if (jobs.length === 0) {
      setLoading(true)
      axios.get('/api/jobs/')
        .then(res => setJobs(res.data))
        .catch(err => console.error(err))
        .finally(() => setLoading(false))
    }
  }, [jobs.length])

  const handleInteraction = async (jobId, type) => {
    try {
      await axios.post('/api/jobs/interaction', null, {
        params: { job_id: jobId, type: type }
      })
      if (type === 'apply') {
        alert('Application submitted successfully! Interaction recorded.')
      }
    } catch (err) {
      console.error('Failed to record interaction', err)
    }
  }

  return (
    <div className="max-w-7xl mx-auto py-12 px-6 lg:px-8 space-y-12 animate-fade-in text-slate-900">
      {/* Header Section */}
      <div className="relative group overflow-hidden rounded-3xl bg-slate-900 p-12 text-white shadow-2xl">
        <div className="absolute top-0 right-0 -m-12 w-64 h-64 bg-primary-500 rounded-full blur-[100px] opacity-20 group-hover:opacity-40 transition-opacity" />
        <div className="absolute bottom-0 left-0 -m-12 w-64 h-64 bg-indigo-500 rounded-full blur-[100px] opacity-20 group-hover:opacity-40 transition-opacity" />
        
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-8">
          <div className="space-y-4">
            <h1 className="text-4xl md:text-5xl font-black tracking-tight leading-none">
              Top Picks For <span className="text-primary-400">You.</span>
            </h1>
            <p className="text-slate-400 text-lg max-w-xl font-medium antialiased">
              We've analyzed your profile and matched you with local and remote opportunities that fit your skills perfectly.
            </p>
          </div>
          <Link 
            to="/upload" 
            className="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 backdrop-blur-xl border border-white/10 px-6 py-3 rounded-2xl font-bold transition-all hover:scale-105 active:scale-95 group shadow-inner"
          >
            Update Profile <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </div>

      {/* Extracted Skills Section */}
      {skills.length > 0 && (
        <div className="bg-white rounded-[2rem] p-8 border border-slate-100 shadow-sm animate-slide-up">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-primary-50 rounded-lg text-primary-600">
              <Trophy size={20} />
            </div>
            <h2 className="text-xl font-bold text-slate-800 tracking-tight">Identified Skills</h2>
          </div>
          <div className="flex flex-wrap gap-2">
            {skills.map((skill) => (
              <span key={skill} className="px-4 py-2 bg-primary-50 text-primary-700 rounded-xl text-sm font-bold border border-primary-100 shadow-sm hover:scale-105 transition-transform cursor-default">
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-[400px] bg-white rounded-3xl border border-slate-100 animate-pulse" />
          ))}
        </div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-32 flex flex-col items-center gap-8 bg-white rounded-3xl border border-dashed border-slate-200 shadow-inner">
          <div className="p-6 bg-slate-50 rounded-full text-slate-300">
            <Briefcase size={48} />
          </div>
          <div className="space-y-2">
            <p className="text-2xl font-bold text-slate-800">No matches found yet</p>
            <p className="text-slate-400 font-medium">Try refining your resume or upload a more detailed profile.</p>
          </div>
          <Link to="/upload" className="btn-primary">Go to Upload</Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {jobs.map((job) => (
            <div key={job.id} className="group relative bg-white border border-slate-100 rounded-[2rem] p-8 flex flex-col gap-6 transition-all hover:shadow-[0_20px_50px_rgba(0,0,0,0.08)] hover:-translate-y-2 overflow-hidden">
              {/* Match Score Badge */}
              <div className="flex justify-between items-start">
                <div className="p-4 bg-slate-50 text-slate-400 rounded-2xl group-hover:bg-primary-600 group-hover:text-white transition-all transform group-hover:rotate-6 shadow-sm">
                  <Briefcase size={24} />
                </div>
                {job.recommendation_score > 0 && (
                  <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 text-emerald-600 rounded-full text-xs font-black border border-emerald-100 shadow-sm uppercase tracking-tighter">
                    <Trophy size={14} />
                    {(job.recommendation_score * 100).toFixed(0)}% Match
                  </div>
                )}
              </div>

              {/* Info Section */}
              <div className="space-y-4">
                <div className="space-y-1">
                  <span className="inline-flex items-center gap-1 text-[10px] font-black uppercase tracking-widest text-primary-500 bg-primary-50 px-2 py-0.5 rounded-md">
                    <Globe size={10} /> {job.source || 'Direct'}
                  </span>
                  <h3 className="text-2xl font-bold text-slate-900 group-hover:text-primary-600 transition-colors tracking-tight leading-tight">
                    {job.title}
                  </h3>
                </div>

                <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-2.5 text-slate-600 font-semibold text-sm">
                    <Building2 size={18} className="text-slate-300" />
                    {job.company}
                  </div>
                  <div className="flex items-center gap-2.5 text-slate-400 font-medium text-sm">
                    <MapPin size={18} className="text-slate-200" />
                    {job.location}
                  </div>
                </div>

                {/* Match Explanation */}
                {job.explanation && (
                  <p className="text-sm font-medium text-slate-500 leading-relaxed bg-slate-50 p-4 rounded-2xl border border-slate-100 italic">
                    <span className="text-primary-600 font-bold not-italic">Why this match: </span>
                    "{job.explanation}"
                  </p>
                )}
              </div>

              {/* Skills/Description */}
              <div className="pt-6 border-t border-slate-50 mt-auto">
                <div className="flex flex-wrap gap-2">
                  {job.required_skills.slice(0, 3).map((skill) => (
                    <span key={skill} className="px-3 py-1 bg-slate-50 text-slate-500 rounded-lg text-xs font-bold border border-slate-100 hover:bg-slate-100 transition-colors">
                      {skill}
                    </span>
                  ))}
                  {job.required_skills.length > 3 && (
                    <span className="px-3 py-1 text-slate-300 text-[10px] font-black uppercase">
                      +{job.required_skills.length - 3} More
                    </span>
                  )}
                </div>
              </div>

              {/* CTA Section */}
              <div className="flex gap-3 mt-2">
                <button 
                  onClick={() => handleInteraction(job.id, 'apply')}
                  className="flex-1 bg-slate-900 text-white rounded-2xl py-4 px-6 font-black hover:bg-primary-600 transition-all shadow-xl shadow-slate-200 active:scale-95 transform"
                >
                  Apply Now
                </button>
                <button className="p-4 bg-slate-50 text-slate-400 rounded-2xl hover:bg-slate-100 transition-colors border border-slate-100">
                  <Share2 size={20} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
