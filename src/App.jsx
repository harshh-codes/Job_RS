import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import UploadResume from './pages/UploadResume'
import Recommendations from './pages/Recommendations'

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<UploadResume />} />
          <Route path="/recommendations" element={<Recommendations />} />
        </Routes>
      </main>
      <footer className="py-8 text-center text-slate-400 text-sm">
        © 2026 Job Recommendation System. All rights reserved.
      </footer>
    </div>
  )
}

export default App
