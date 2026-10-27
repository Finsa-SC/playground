import { useRef, useState } from 'react'
import { ImagePlus, X } from 'lucide-react'
import { api } from '../api.js'
import { useAuth } from '../auth.jsx'
import { Avatar } from './ui.jsx'

const MAX = 5000

export default function Composer({ onCreated }) {
  const { me } = useAuth()
  const [text, setText] = useState('')
  const [items, setItems] = useState([]) // {file, preview}
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const input = useRef(null)

  function pick(e) {
    const picked = [...e.target.files].map((file) => ({ file, preview: URL.createObjectURL(file) }))
    e.target.value = ''
    const all = [...items, ...picked]
    if (all.some((i) => i.file.type.startsWith('video')) && all.length > 1) {
      picked.forEach((i) => URL.revokeObjectURL(i.preview))
      return setErr('Video diunggah sendiri, tidak digabung dengan lampiran lain.')
    }
    setErr('')
    setItems(all.slice(0, 4))
  }

  function drop(i) {
    URL.revokeObjectURL(items[i].preview)
    setItems(items.filter((_, j) => j !== i))
  }

  async function submit(e) {
    e.preventDefault()
    if (!text.trim() && items.length === 0) return
    setBusy(true)
    setErr('')
    try {
      const post = await api.createPost(text.trim() || null)
      for (const it of items) await api.uploadPostMedia(post.id, it.file)
      const full = items.length ? await api.getPost(post.id) : post
      items.forEach((i) => URL.revokeObjectURL(i.preview))
      setText('')
      setItems([])
      onCreated?.(full)
    } catch (e) {
      setErr(e.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <form className="composer" onSubmit={submit}>
      <Avatar username={me?.username} name={me?.display_name} />
      <div className="composer-main">
        <textarea value={text} onChange={(e) => setText(e.target.value)} maxLength={MAX} placeholder="Apa yang sedang terjadi?" rows={text.length > 80 ? 4 : 2} />
        {items.length > 0 && (
          <div className="previews">
            {items.map((it, i) => (
              <div className="preview" key={it.preview}>
                {it.file.type.startsWith('video') ? <video src={it.preview} muted /> : <img src={it.preview} alt="" />}
                <button type="button" aria-label="Hapus lampiran" onClick={() => drop(i)}><X size={14} /></button>
              </div>
            ))}
          </div>
        )}
        {err && <p className="notice error">{err}</p>}
        <div className="composer-bar">
          <input ref={input} type="file" accept="image/*,video/*" multiple hidden onChange={pick} />
          <button type="button" className="icon-btn" onClick={() => input.current.click()} aria-label="Tambah gambar atau video"><ImagePlus size={20} /></button>
          <span className="muted counter">{text.length}/{MAX}</span>
          <button className="btn primary" disabled={busy || (!text.trim() && !items.length)}>{busy ? 'Posting…' : 'Post'}</button>
        </div>
      </div>
    </form>
  )
}
