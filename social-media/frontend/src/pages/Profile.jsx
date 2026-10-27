import { useCallback, useEffect, useState } from 'react'
import { Link, Navigate, useParams } from 'react-router-dom'
import { Link as LinkIcon, MapPin } from 'lucide-react'
import { api, bannerUrl, idOf } from '../api.js'
import { useAuth } from '../auth.jsx'
import PostCard from '../components/PostCard.jsx'
import { Avatar, PageHeader, Paged, Spinner } from '../components/ui.jsx'

export function ProfileRedirect() {
  const { user } = useAuth()
  return <Navigate to={`/profile/${user.username}`} replace />
}

export default function Profile() {
  const { username } = useParams()
  const { user, ver } = useAuth()
  const [p, setP] = useState(null)
  const [err, setErr] = useState('')
  const [counts, setCounts] = useState({ followers: 0, following: 0 })
  const [following, setFollowing] = useState(false)
  const [banner, setBanner] = useState(true)
  const own = user.username.toLowerCase() === username.toLowerCase()

  useEffect(() => {
    setP(null)
    setErr('')
    setBanner(true)
    api.profile(username).then(async (prof) => {
      setP(prof)
      const id = prof.user_id
      const [fers, fing, mine] = await Promise.all([
        api.followers(id).catch(() => []),
        api.following(id).catch(() => []),
        own ? [] : api.following(user.id).catch(() => []),
      ])
      setCounts({ followers: fers.length, following: fing.length })
      setFollowing(mine.some((x) => idOf(x) === id))
    }).catch((e) => setErr(e.message))
  }, [username, own, user.id, ver])

  async function toggleFollow() {
    const next = !following
    setFollowing(next)
    setCounts((c) => ({ ...c, followers: c.followers + (next ? 1 : -1) }))
    try {
      await (next ? api.follow(p.user_id) : api.unfollow(p.user_id))
    } catch (e) {
      setFollowing(!next)
      setCounts((c) => ({ ...c, followers: c.followers + (next ? -1 : 1) }))
      alert(e.message)
    }
  }

  const fetchPage = useCallback((l, o) => api.userPosts(p.user_id, l, o), [p?.user_id])

  if (err) return <><PageHeader title="Profil" /><p className="notice error">{err}</p></>
  if (!p) return <><PageHeader title="Profil" /><Spinner /></>

  return (
    <>
      <PageHeader title={p.display_name} />
      <section className="profile">
        <div className="banner">
          {banner && <img src={bannerUrl(username, ver)} alt="" onError={() => setBanner(false)} />}
        </div>
        <div className="profile-top">
          <div className="avatar-ring"><Avatar username={username} name={p.display_name} size={92} /></div>
          {own ? (
            <Link className="btn" to="/profile/edit">Edit profile</Link>
          ) : (
            <button className={`btn ${following ? '' : 'primary'}`} onClick={toggleFollow}>{following ? 'Following' : 'Follow'}</button>
          )}
        </div>
        <h2 className="profile-name">{p.display_name}</h2>
        <p className="muted">@{username}</p>
        {p.bio && <p className="bio">{p.bio}</p>}
        <div className="profile-info muted">
          {p.location && <span><MapPin size={15} /> {p.location}</span>}
          {p.website_url && <a href={p.website_url} target="_blank" rel="noreferrer noopener"><LinkIcon size={15} /> {p.website_url.replace(/^https?:\/\//, '')}</a>}
        </div>
        <div className="counts">
          <span><b>{counts.following}</b> following</span>
          <span><b>{counts.followers}</b> followers</span>
        </div>
      </section>
      <Paged key={p.user_id} fetchPage={fetchPage} render={(x) => <PostCard key={x.id} post={x} />} empty={own ? 'Kamu belum posting apa-apa.' : 'Belum ada post.'} />
    </>
  )
}
