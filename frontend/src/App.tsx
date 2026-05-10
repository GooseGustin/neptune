import { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { supabase } from '@/lib/supabase'
import { useAuthStore } from '@/stores/authStore'

// Pages (stubs — to be implemented)
const LoginPage        = () => <div className="flex items-center justify-center min-h-screen"><p className="text-text-secondary">Login page — coming soon</p></div>
const DashboardPage    = () => <div className="p-8"><p className="text-text-secondary">Dashboard — coming soon</p></div>
const SettingsPage     = () => <div className="p-8"><p className="text-text-secondary">Settings — coming soon</p></div>
const NewCoursePage    = () => <div className="p-8"><p className="text-text-secondary">New course — coming soon</p></div>
const CourseViewPage   = () => <div className="p-8"><p className="text-text-secondary">Course view — coming soon</p></div>
const CompletionPage   = () => <div className="p-8"><p className="text-text-secondary">Completion — coming soon</p></div>

function RequireAuth({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuthStore()
  if (loading) return <div className="flex items-center justify-center min-h-screen"><div className="animate-spin w-6 h-6 border-2 border-accent border-t-transparent rounded-full" /></div>
  if (!user) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function App() {
  const { setSession, setLoading } = useAuthStore()

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setLoading(false)
    })
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_e, session) => {
      setSession(session)
      setLoading(false)
    })
    return () => subscription.unsubscribe()
  }, [setSession, setLoading])

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<RequireAuth><DashboardPage /></RequireAuth>} />
      <Route path="/settings" element={<RequireAuth><SettingsPage /></RequireAuth>} />
      <Route path="/courses/new" element={<RequireAuth><NewCoursePage /></RequireAuth>} />
      <Route path="/courses/:id" element={<RequireAuth><CourseViewPage /></RequireAuth>} />
      <Route path="/courses/:id/complete" element={<RequireAuth><CompletionPage /></RequireAuth>} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
