import { useMemo, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Camera } from 'lucide-react'
import { api } from '../api.js'
import { useAuth } from '../auth.jsx'
import { Avatar, PageHeader } from '../components/ui.jsx'

export default function EditProfile() {
  const { user, profile, refresh, ver } = useAuth()
  const nav = useNavigate()
  const [f, setF] = useState({
    display_name: profile?.display_name || '',
    bio: profile?.bio || '',
    website_url: profile?.website_url || '',
    location: profile?.location || '',
  })
  const [avatar, setAvatar] = useState(null)
  const [banner, setBanner] = useState(null)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const avIn = useRef(null)
  const bnIn = useRef(null)
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value })
  const avPrev = useMemo(() => (avatar ? URL.createObjectURL(avatar) : null), [avatar])
  const bnPrev = useMemo(() => (banner ? URL.createObjectURL(banner) : null), [banner])

  async function save(e) {
    e.preventDefault()
    setBusy(true)
    setErr('')
    try {
      await api.updateProfile({
        display_name: f.display_name.trim(),
        bio: f.bio.trim() || null,
        website_url: f.website_url.trim() || null,
        location: f.location.trim() || null,
      })
      if (avatar) await api.uploadAvatar(avatar)
      if (banner) await api.uploadBanner(banner)
      await refresh()
      nav(`/profile/${user.username}`)
    } catch (e) {
      setErr(e.message)
      setBusy(false)
    }
  }

  return (
    <>
      <PageHeader title="Edit profile" />
      <form className="edit" onSubmit={save}>
        <div className="banner editable" onClick={() => bnIn.current.click()} role="button" tabIndex={0} aria-label="Ganti banner" onKeyDown={(e) => e.key === 'Enter' && bnIn.current.click()}>
          <img src={bnPrev || `/api/v1/profiles/${user.username}/banner?v=${ver}`} alt="" onError={(e) => (e.currentTarget.style.display = 'none')} onLoad={(e) => (e.currentTarget.style.display = '')} />
          <span className="cam"><Camera size={20} /></span>
          <input ref={bnIn} type="file" accept="image/*" hidden onChange={(e) => setBanner(e.target.files[0] || null)} />
        </div>
        <div className="profile-top">
          <button type="button" className="avatar-ring editable" onClick={() => avIn.current.click()} aria-label="Ganti foto profil">
            {avPrev ? <span className="avatar" style={{ width: 92, height: 92 }}><img src={avPrev} alt="" /></span> : <Avatar username={user.username} name={f.display_name} size={92} />}
            <span className="cam"><Camera size={20} /></span>
          </button>
          <input ref={avIn} type="file" accept="image/*" hidden onChange={(e) => setAvatar(e.target.files[0] || null)} />
        </div>
        <div className="fields">
          <label>Nama tampilan<input value={f.display_name} onChange={set('display_name')} maxLength={50} required /></label>
          <label>Bio<textarea value={f.bio} onChange={set('bio')} maxLength={280} rows={3} /><span className="muted counter">{f.bio.length}/280</span></label>
          <label>Lokasi<input value={f.location} onChange={set('location')} maxLength={100} /></label>
          <label>Website<input type="url" placeholder="https://" value={f.website_url} onChange={set('website_url')} maxLength={2083} /></label>
          {err && <p className="notice error">{err}</p>}
          <div className="row-end">
            <button type="button" className="btn" onClick={() => nav(-1)}>Batal</button>
            <button className="btn primary" disabled={busy}>{busy ? 'Menyimpan…' : 'Simpan'}</button>
          </div>
        </div>
      </form>
    </>
  )
}
