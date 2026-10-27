import { useState } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth.jsx'

function Shell({ title, sub, children, foot }) {
  return (
    <main className="auth">
      <div className="auth-card">
        <div className="brand big"><img src="/favicon.ico" alt="" /> FinSky</div>
        <h1>{title}</h1>
        <p className="muted">{sub}</p>
        {children}
        <p className="muted foot">{foot}</p>
      </div>
    </main>
  )
}

export function Login() {
  const { user, login } = useAuth()
  const nav = useNavigate()
  const from = useLocation().state?.from || '/foryou'
  const [f, setF] = useState({ username: '', password: '' })
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  if (user) return <Navigate to={from} replace />

  async function submit(e) {
    e.preventDefault()
    setBusy(true)
    setErr('')
    try {
      await login(f.username, f.password)
      nav(from, { replace: true })
    } catch (e) {
      setErr(e.message)
    } finally {
      setBusy(false)
    }
  }
  return (
    <Shell title="Masuk ke FinSky" sub="Lanjutkan percakapanmu." foot={<>Belum punya akun? <Link to="/register">Daftar</Link></>}>
      <form onSubmit={submit}>
        <label>Username<input autoFocus autoComplete="username" value={f.username} onChange={(e) => setF({ ...f, username: e.target.value })} required /></label>
        <label>Password<input type="password" autoComplete="current-password" value={f.password} onChange={(e) => setF({ ...f, password: e.target.value })} required /></label>
        {err && <p className="notice error">{err}</p>}
        <button className="btn primary wide" disabled={busy}>{busy ? 'Masuk…' : 'Masuk'}</button>
      </form>
    </Shell>
  )
}

export function Register() {
  const { user, register } = useAuth()
  const nav = useNavigate()
  const [f, setF] = useState({ display_name: '', username: '', email: '', password: '' })
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  if (user) return <Navigate to="/foryou" replace />
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value })

  async function submit(e) {
    e.preventDefault()
    setBusy(true)
    setErr('')
    try {
      await register(f)
      nav('/foryou', { replace: true })
    } catch (e) {
      setErr(e.message)
    } finally {
      setBusy(false)
    }
  }
  return (
    <Shell title="Buat akun FinSky" sub="Gratis, dan butuh waktu kurang dari satu menit." foot={<>Sudah punya akun? <Link to="/login">Masuk</Link></>}>
      <form onSubmit={submit}>
        <label>Nama tampilan<input value={f.display_name} onChange={set('display_name')} maxLength={50} required /></label>
        <label>Username<input value={f.username} onChange={set('username')} minLength={3} maxLength={30} pattern="[A-Za-z0-9_]+" title="Huruf, angka, dan underscore" required /></label>
        <label>Email<input type="email" value={f.email} onChange={set('email')} required /></label>
        <label>Password<input type="password" autoComplete="new-password" value={f.password} onChange={set('password')} minLength={8} maxLength={128} required /></label>
        {err && <p className="notice error">{err}</p>}
        <button className="btn primary wide" disabled={busy}>{busy ? 'Membuat akun…' : 'Daftar'}</button>
      </form>
    </Shell>
  )
}
