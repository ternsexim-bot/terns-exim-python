import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import ContactForm from './components/ContactForm'
import { cn } from '@/lib/utils'

const tabCls = ({ isActive }) =>
  cn(
    'border-b-2 border-transparent px-4 py-2.5 text-[13px] font-medium text-slate-500 transition-colors hover:text-navy',
    isActive && 'border-gold text-navy'
  )

export default function App() {
  return (
    <BrowserRouter>
      <nav className="sticky top-0 z-[101] flex gap-1 border-b border-slate-200 bg-white px-7">
        <NavLink to="/" end className={tabCls}>
          CRM Dashboard
        </NavLink>
        <NavLink to="/contact" className={tabCls}>
          Enquiry Form
        </NavLink>
      </nav>
      <Routes>
        <Route path="/"        element={<Dashboard />} />
        <Route path="/contact" element={<ContactForm />} />
      </Routes>
    </BrowserRouter>
  )
}
