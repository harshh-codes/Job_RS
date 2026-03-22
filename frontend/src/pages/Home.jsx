import { Link } from 'react-router-dom'
import { Rocket, Target, Zap, ChevronRight } from 'lucide-react'

export default function Home() {
  const steps = [
    {
      title: 'Upload Your Resume',
      desc: 'Our AI analyzes your skills, experience, and career trajectory.',
      icon: <Rocket className="text-primary-500" size={32} />,
    },
    {
      title: 'Analyze & Match',
      desc: 'Get ranked job recommendations tailored to your profile.',
      icon: <Target className="text-secondary-500" size={32} />,
    },
    {
      title: 'Apply Instantly',
      desc: 'Directly connect with top employers looking for your expertise.',
      icon: <Zap className="text-yellow-500" size={32} />,
    },
  ]

  return (
    <div className="flex flex-col gap-16 py-8">
      <section className="text-center flex flex-col items-center gap-6 py-12 animate-fade-in relative">
        <div className="absolute top-0 -z-10 bg-primary-200/20 blur-[100px] w-64 h-64 rounded-full" />
        <h1 className="text-5xl md:text-7xl gradient-text leading-tight max-w-4xl tracking-tight">
          Find Your Dream Job with AI Accuracy
        </h1>
        <p className="text-xl text-slate-500 max-w-2xl leading-relaxed">
          The next generation job recommendation system. Upload your resume and let our matching engine do the hard work for you.
        </p>
        <Link to="/upload" className="btn-primary flex items-center gap-2 group">
          Get Started <ChevronRight size={20} className="group-hover:translate-x-1 transition-transform" />
        </Link>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-8 px-4 animate-slide-up">
        {steps.map((step, idx) => (
          <div key={idx} className="card group relative overflow-hidden bg-white/50">
            <div className="absolute top-0 left-0 w-1 h-full bg-primary-200 opacity-20 group-hover:opacity-100 transition-opacity" />
            <div className="mb-6 p-4 bg-primary-50 w-fit rounded-2xl group-hover:scale-110 transition-transform">
              {step.icon}
            </div>
            <h3 className="text-xl font-bold mb-3 text-slate-800 tracking-tight">{step.title}</h3>
            <p className="text-slate-500 leading-relaxed font-normal">{step.desc}</p>
          </div>
        ))}
      </section>
    </div>
  )
}
