import { useState } from 'react'
import { Link } from 'react-router-dom'
import { Heart, MessageCircle, Trash2 } from 'lucide-react'
import { api, timeAgo } from '../api.js'
import { authorOf, useAuth } from '../auth.jsx'
import { Avatar, PostMedia } from './ui.jsx'

export default function PostCard({ post, detail = false }) {
  const { me } = useAuth()
  const [liked, setLiked] = useState(!!post.liked_by_me)
  const [likes, setLikes] = useState(post.like_count || 0)
  const [gone, setGone] = useState(false)
  const author = authorOf(post, me)
  const mine = me?.id === post.author_id
  const profileLink = author.username ? `/profile/${author.username}` : null

  async function toggleLike() {
    const next = !liked
    setLiked(next)
    setLikes((n) => n + (next ? 1 : -1))
    try {
      await (next ? api.like(post.id) : api.unlike(post.id))
    } catch {
      setLiked(!next)
      setLikes((n) => n + (next ? -1 : 1))
    }
  }

  async function remove() {
    if (!confirm('Hapus post ini?')) return
    try {
      await api.deletePost(post.id)
      setGone(true)
    } catch (e) {
      alert(e.message)
    }
  }

  if (gone) return null
  const media = [...(post.media || [])].sort((a, b) => a.position - b.position)

  return (
    <article className="post">
      {profileLink ? <Link to={profileLink}><Avatar username={author.username} name={author.display_name} /></Link> : <Avatar name={author.display_name} />}
      <div className="post-body">
        <div className="post-meta">
          {profileLink ? (
            <Link to={profileLink} className="post-name">{author.display_name || author.username}</Link>
          ) : (
            <span className="post-name">{author.display_name}</span>
          )}
          {author.username && <span className="muted">@{author.username}</span>}
          <Link to={`/post/${post.id}`} className="muted post-time">{timeAgo(post.created_at)}</Link>
          {post.edited_at && <span className="muted">(edited)</span>}
        </div>
        {post.content && <p className={`post-text ${detail ? 'big' : ''}`}>{post.content}</p>}
        {media.length > 0 && (
          <div className={`media-grid n${Math.min(media.length, 4)}`}>
            {media.map((m) => <PostMedia key={m.id} media={m} />)}
          </div>
        )}
        <div className="post-actions">
          <button className={`act like ${liked ? 'on' : ''}`} onClick={toggleLike} aria-pressed={liked} aria-label="Like">
            <Heart size={18} fill={liked ? 'currentColor' : 'none'} /> {likes}
          </button>
          <Link className="act comment" to={`/post/${post.id}`} aria-label="Comments">
            <MessageCircle size={18} /> {post.comment_count || 0}
          </Link>
          {mine && (
            <button className="act danger" onClick={remove} aria-label="Hapus post"><Trash2 size={17} /></button>
          )}
        </div>
      </div>
    </article>
  )
}
