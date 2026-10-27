import { useCallback, useEffect, useRef, useState } from 'react'
import { api, avatarUrl } from '../api.js'
import { useAuth } from '../auth.jsx'

export function Avatar({ username, name, size = 44 }) {
  const { ver } = useAuth()
  const [bad, setBad] = useState(false)
  useEffect(() => setBad(false), [username, ver])
  const letter = (name || username || '?').slice(0, 1).toUpperCase()
  return (
    <span className="avatar" style={{ width: size, height: size, fontSize: size * 0.42 }}>
      {username && !bad ? <img src={avatarUrl(username, ver)} alt="" onError={() => setBad(true)} /> : letter}
    </span>
  )
}

export function PageHeader({ title, children }) {
  return (
    <header className="page-header">
      <h1>{title}</h1>
      {children}
    </header>
  )
}

export function Spinner() {
  return <div className="spinner" role="status" aria-label="Loading" />
}

// /media/{id} butuh token, jadi file diambil sebagai blob lalu ditampilkan.
export function PostMedia({ media }) {
  const [src, setSrc] = useState(null)
  const [err, setErr] = useState(false)
  useEffect(() => {
    let url
    let alive = true
    api.mediaBlob(media.id)
      .then((b) => {
        url = URL.createObjectURL(b)
        if (alive) setSrc(url)
      })
      .catch(() => alive && setErr(true))
    return () => {
      alive = false
      if (url) URL.revokeObjectURL(url)
    }
  }, [media.id])

  const isVideo = media.media_type === 'video' || media.mime_type?.startsWith('video')
  const ratio = media.width && media.height ? { aspectRatio: `${media.width} / ${media.height}` } : undefined
  if (err) return <div className="media media-missing">Media tidak bisa dimuat</div>
  if (!src) return <div className="media media-loading" style={ratio} />
  return isVideo ? (
    <video className="media" src={src} controls preload="metadata" playsInline />
  ) : (
    <img className="media" src={src} alt={media.alt_text || ''} />
  )
}

// Daftar paginasi (limit/offset) dengan infinite scroll.
export function Paged({ fetchPage, render, empty, pageSize = 20 }) {
  const [items, setItems] = useState([])
  const [done, setDone] = useState(false)
  const [loading, setLoading] = useState(true)
  const [err, setErr] = useState('')
  const offset = useRef(0)
  const busy = useRef(false)
  const gen = useRef(0)
  const sentinel = useRef(null)

  const load = useCallback(async () => {
    if (busy.current) return
    busy.current = true
    const g = gen.current
    setLoading(true)
    try {
      const page = await fetchPage(pageSize, offset.current)
      if (g !== gen.current) return
      offset.current += page.length
      setItems((p) => {
        const ids = new Set(p.map((x) => x.id))
        return [...p, ...page.filter((x) => !ids.has(x.id))]
      })
      if (page.length < pageSize) setDone(true)
    } catch (e) {
      if (g === gen.current) {
        setErr(e.message)
        setDone(true)
      }
    } finally {
      if (g === gen.current) {
        busy.current = false
        setLoading(false)
      }
    }
  }, [fetchPage, pageSize])

  useEffect(() => {
    gen.current++
    busy.current = false
    offset.current = 0
    setItems([])
    setDone(false)
    setErr('')
    load()
  }, [load])

  useEffect(() => {
    if (done || !sentinel.current) return
    const io = new IntersectionObserver((e) => e[0].isIntersecting && load(), { rootMargin: '400px' })
    io.observe(sentinel.current)
    return () => io.disconnect()
  }, [done, load, items.length])

  return (
    <>
      {items.map(render)}
      {err && <p className="notice error">{err}</p>}
      {!loading && !err && items.length === 0 && <div className="empty">{empty}</div>}
      {loading && <Spinner />}
      {!done && <div ref={sentinel} style={{ height: 1 }} />}
    </>
  )
}
