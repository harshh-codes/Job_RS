import { Link, useLocation } from 'react-router-dom'
import { Briefcase, Upload, List, Home } from 'lucide-react'

export default function Navbar() {
  const location = useLocation()

  const navLinks = [
    { name: 'Home', path: '/', icon: Home },
    { name: 'Upload', path: '/upload', icon: Upload },
    { name: 'Jobs', path: '/recommendations', icon: List },
  ]

  return (
    <nav className="glass sticky top-4 z-50 mx-4 mt-4 rounded-2xl px-6 py-4 flex items-center justify-between">
      <Link to="/" className="flex items-center gap-2 group">
        <div className="bg-primary-600 p-2 rounded-lg text-white transform transition-transform group-hover:rotate-12">
          <Briefcase size={24} />
        </div>
        <span className="text-xl font-bold gradient-text">JobRS</span>
      </Link>
      
      <div className="flex gap-1">
        {navLinks.map((link) => {
          const Icon = link.icon
          const isActive = location.pathname === link.path
          return (
            <Link
              key={link.path}
              to={link.path}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all ${
                isActive 
                  ? 'bg-primary-50 text-primary-600 font-medium' 
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Icon size={18} />
              <span>{link.name}</span>
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
