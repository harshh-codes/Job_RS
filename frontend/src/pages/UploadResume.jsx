import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { FileUp, Search, CheckCircle, AlertCircle } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL;

export default function UploadResume() {
  const [resumeText, setResumeText] = useState('')
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile)
      setError('')
    } else {
      setError('Please select a valid PDF file.')
      setFile(null)
    }
  }

  const handleRecommend = async (e) => {
    e.preventDefault()

    if (!file && !resumeText.trim()) {
      setError('Please provide a resume.')
      return
    }

    setLoading(true)
    setError('')

    try {
      let response;

      if (file) {
        const formData = new FormData()
        formData.append('file', file)

        response = await axios.post(
          `${API_URL}/api/jobs/upload-resume`,
          formData,
          { headers: { 'Content-Type': 'multipart/form-data' } }
        )

        navigate('/recommendations', {
          state: {
            jobs: response.data.recommendations,
            skills: response.data.extracted_skills
          }
        })

      } else {
        response = await axios.post(
          `${API_URL}/api/jobs/recommend`,
          null,
          { params: { resume_text: resumeText } }
        )

        navigate('/recommendations', {
          state: { jobs: response.data }
        })
      }

    } catch (err) {
      console.error(err)
      setError('Failed to fetch recommendations')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto py-12 animate-fade-in px-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold gradient-text mb-4">Upload Your Profile</h1>
        <p className="text-slate-500">Choose your preferred method to find matching opportunities.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* File Upload Section */}
        <div className="card bg-white p-8 flex flex-col gap-6">
          <div className="flex items-center gap-3 text-slate-800 font-bold text-lg border-b pb-4">
            <FileUp className="text-primary-600" />
            Upload PDF Resume
          </div>
          
          <label className="border-2 border-dashed border-slate-200 rounded-2xl p-8 flex flex-col items-center gap-4 cursor-pointer hover:border-primary-400 hover:bg-primary-50 transition-all group">
            <input type="file" className="hidden" accept=".pdf" onChange={handleFileChange} />
            <div className={`p-4 rounded-full ${file ? 'bg-green-100 text-green-600' : 'bg-primary-50 text-primary-500'}`}>
              {file ? <CheckCircle size={32} /> : <FileUp size={32} className="group-hover:bounce" />}
            </div>
            <div className="text-center">
              <p className="font-semibold text-slate-700">{file ? file.name : 'Click to Browse'}</p>
              <p className="text-xs text-slate-400 mt-1">PDF files only (Max 5MB)</p>
            </div>
          </label>
        </div>

        {/* Text Paste Section */}
        <div className="card bg-white p-8 flex flex-col gap-6">
          <div className="flex items-center gap-3 text-slate-800 font-bold text-lg border-b pb-4">
            <Search className="text-primary-600" />
            Paste Resume Text
          </div>
          <textarea
            className="flex-1 min-h-[140px] p-4 rounded-xl border border-slate-200 focus:border-primary-400 outline-none transition-all resize-none text-sm"
            placeholder="Paste skills, summary, or experience..."
            value={resumeText}
            onChange={(e) => {
              setResumeText(e.target.value)
              if (e.target.value) setFile(null)
            }}
          />
        </div>
      </div>

      <div className="mt-12 flex flex-col gap-6">
        {error && (
          <div className="p-4 bg-red-50 text-red-600 rounded-xl flex items-center gap-3 animate-slide-up border border-red-100">
            <AlertCircle size={20} />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        <button
          onClick={handleRecommend}
          disabled={loading}
          className={`btn-primary flex items-center justify-center gap-3 py-4 text-xl w-full shadow-2xl ${
            loading ? 'opacity-70 cursor-not-allowed' : ''
          }`}
        >
          {loading ? (
            <div className="flex items-center gap-3">
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>Analyzing...</span>
            </div>
          ) : (
            <>
              <Search size={20} />
              <span>Get Recommendations</span>
            </>
          )}
        </button>
      </div>
    </div>
  )
}

