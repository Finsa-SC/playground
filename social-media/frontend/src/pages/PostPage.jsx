import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Trash2 } from 'lucide-react'
import { api, timeAgo } from '../api.js'
import { authorOf, useAuth } from '../auth.jsx'
import PostCard from '../components/PostCard.jsx'
import { Avatar, PageHeader, Paged, Spinner } from '../components/ui.jsx'

function Comment({ c, postId, onDeleted }) {
  const { me } = useAuth()
  const a = authorOf(c, me)
  const [gone, setGone] = useState(false)
  if (gone) return null
  return (
    <div className="post comment-row">
      {a.username ? <Link to={`/profile/${a.username}`}><Avatar username={a.username} name={a.display_name} size={36} /></Link> : <Avatar name={a.display_name} size={36} />}
      <div className="post-body">
        <div className="post-meta">
          <span className="post-name">{a.display_name || a.username}</span>
          {a.username && <span className="muted">@{a.username}</span>}
          <span className="muted">{timeAgo(c.created_at)}</span>
        </div>
        <p className="post-text">{c.content}</p>
      </div>
      {me?.id === c.author_id && (
        <button className="icon-btn danger" aria-label="Hapus komentar" onClick={async () => {
          try { await api.deleteComment(postId, c.id); setGone(true); onDeleted() } catch (e) { alert(e.message) }
        }}><Trash2 size={16} /></button>
      )}
    </div>
  )
}

export default function PostPage() {
  const { id } = useParams()
  const nav = useNavigate()
  const { me } = useAuth()
  const [post, setPost] = useState(null)
  const [err, setErr] = useState('')
  const [text, setText] = useState('')
  const [busy, setBusy] = useState(false)
  const [fresh, setFresh] = useState([])

  useEffect(() => {
    setPost(null)
    setFresh([])
    api.getPost(id).then(setPost).catch((e) => setErr(e.message))
  }, [id])

  const fetchPage = useCallback((l, o) => api.comments(id, l, o), [id])
  const bump = (n) => setPost((p) => ({ ...p, comment_count: Math.max(0, (p.comment_count || 0) + n) }))

  async function send(e) {
    e.preventDefault()
    if (!text.trim()) return
    setBusy(true)
    try {
      const c = await api.addComment(id, text.trim())
      setFresh((f) => [...f, c])
      bump(1)
      setText('')
    } catch (e) {
      setErr(e.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <>
      <PageHeader title="Post">
        <button className="icon-btn" onClick={() => nav(-1)} aria-label="Kembali"><ArrowLeft size={20} /></button>
      </PageHeader>
      {err && <p className="notice error">{err}</p>}
      {!post && !err && <Spinner />}
      {post && (
        <>
          <PostCard key={id} post={post} detail />
          <form className="composer reply" onSubmit={send}>
            <Avatar username={me?.username} name={me?.display_name} size={36} />
            <div className="composer-main">
              <textarea value={text} onChange={(e) => setText(e.target.value)} maxLength={2000} rows={2} placeholder="Tulis balasan…" />
              <div className="composer-bar">
                <span className="muted counter">{text.length}/2000</span>
                <button className="btn primary" disabled={busy || !text.trim()}>{busy ? 'Mengirim…' : 'Balas'}</button>
              </div>
            </div>
          </form>
          {fresh.map((c) => <Comment key={c.id} c={c} postId={id} onDeleted={() => bump(-1)} />)}
          <Paged
            fetchPage={fetchPage}
            pageSize={50}
            render={(c) => <Comment key={c.id} c={c} postId={id} onDeleted={() => bump(-1)} />}
            empty="Belum ada komentar. Jadilah yang pertama membalas."
          />
        </>
      )}
    </>
  )
}
