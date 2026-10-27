import { NavLink, Navigate, Outlet, Route, Routes, useLocation } from 'react-router-dom'
import { Home, LogOut, User, Users } from 'lucide-react'
import { useAuth } from './auth.jsx'
import { Spinner } from './components/ui.jsx'
import { Login, Register } from './pages/Auth.jsx'
import Feed from './pages/Feed.jsx'
import PostPage from './pages/PostPage.jsx'
import Profile, { ProfileRedirect } from './pages/Profile.jsx'
import EditProfile from './pages/EditProfile.jsx'

function Layout() {
  const { user, ready, logout } = useAuth()
  const loc = useLocation()
  if (!ready) return <div className="boot"><Spinner /></div>
  if (!user) return <Navigate to="/login" replace state={{ from: loc.pathname }} />

  const links = [
    ['/foryou', 'For you', Home],
    ['/following', 'Following', Users],
    ['/profile', 'Profile', User],
  ]
  return (
    <div className="shell">
      <nav className="side" aria-label="Utama">
        <div className="brand"><img src="/favicon.ico" alt="" /> <span>FinSky</span></div>
        {links.map(([to, label, Icon]) => (
          <NavLink key={to} to={to} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <Icon size={22} /> <span>{label}</span>
          </NavLink>
        ))}
        <button className="nav-link logout" onClick={logout}><LogOut size={22} /> <span>Keluar</span></button>
      </nav>
      <main className="col"><Outlet /></main>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<Layout />}>
        <Route path="/" element={<Navigate to="/foryou" replace />} />
        <Route path="/foryou" element={<Feed kind="foryou" />} />
        <Route path="/following" element={<Feed kind="following" />} />
        <Route path="/post/:id" element={<PostPage />} />
        <Route path="/profile" element={<ProfileRedirect />} />
        <Route path="/profile/edit" element={<EditProfile />} />
        <Route path="/profile/:username" element={<Profile />} />
        <Route path="*" element={<Navigate to="/foryou" replace />} />
      </Route>
    </Routes>
  )
}
