const BASE = '/api/v1'

export const tokenStore = {
  get: () => localStorage.getItem('finsky_token'),
  set: (t) => localStorage.setItem('finsky_token', t),
  clear: () => localStorage.removeItem('finsky_token'),
}

let onUnauthorized = () => {}
export const setUnauthorizedHandler = (fn) => (onUnauthorized = fn)

async function req(path, { method = 'GET', json, form, body, raw } = {}) {
  const headers = {}
  const token = tokenStore.get()
  if (token) headers.Authorization = `Bearer ${token}`
  let payload = body
  if (json !== undefined) {
    headers['Content-Type'] = 'application/json'
    payload = JSON.stringify(json)
  }
  if (form) payload = new URLSearchParams(form)

  const res = await fetch(BASE + path, { method, headers, body: payload })
  if (res.status === 401 && token) onUnauthorized()
  if (!res.ok) {
    let msg = `Request gagal (${res.status})`
    try {
      const d = await res.json()
      if (typeof d.detail === 'string') msg = d.detail
      else if (Array.isArray(d.detail)) msg = d.detail.map((x) => x.msg).join(', ')
    } catch {}
    throw new Error(msg)
  }
  if (raw) return res
  if (res.status === 204) return null
  return res.json()
}

const q = (limit, offset) => `limit=${limit}&offset=${offset}`
const file = (f) => {
  const fd = new FormData()
  fd.append('file', f)
  return fd
}

export const api = {
  register: (b) => req('/auth/register', { method: 'POST', json: b }),
  login: (username, password) => req('/auth/login', { method: 'POST', form: { username, password } }),
  me: () => req('/auth/me'),
  myProfile: () => req('/profiles/me'),
  profile: (u) => req(`/profiles/${encodeURIComponent(u)}`),
  updateProfile: (b) => req('/profiles/me', { method: 'PATCH', json: b }),
  uploadAvatar: (f) => req('/profiles/me/avatar', { method: 'POST', body: file(f) }),
  uploadBanner: (f) => req('/profiles/me/banner', { method: 'POST', body: file(f) }),
  follow: (id) => req(`/users/${id}/follow`, { method: 'POST' }),
  unfollow: (id) => req(`/users/${id}/follow`, { method: 'DELETE' }),
  followers: (id, limit = 1000, offset = 0) => req(`/users/${id}/followers?${q(limit, offset)}`),
  following: (id, limit = 1000, offset = 0) => req(`/users/${id}/following?${q(limit, offset)}`),
  feed: (kind, limit, offset) => req(`/feed/${kind}?${q(limit, offset)}`),
  userPosts: (id, limit, offset) => req(`/users/${id}/posts?${q(limit, offset)}`),
  getPost: (id) => req(`/posts/${id}`),
  createPost: (content) => req('/posts', { method: 'POST', json: { content, visibility: 'public' } }),
  deletePost: (id) => req(`/posts/${id}`, { method: 'DELETE' }),
  uploadPostMedia: (id, f) => {
    const fd = file(f)
    fd.append('media_type', f.type.startsWith('video') ? 'video' : 'image')
    return req(`/posts/${id}/media`, { method: 'POST', body: fd })
  },
  like: (id) => req(`/posts/${id}/like`, { method: 'POST' }),
  unlike: (id) => req(`/posts/${id}/like`, { method: 'DELETE' }),
  comments: (id, limit, offset) => req(`/posts/${id}/comments?${q(limit, offset)}`),
  addComment: (id, content) => req(`/posts/${id}/comments`, { method: 'POST', json: { content } }),
  deleteComment: (pid, cid) => req(`/posts/${pid}/comments/${cid}`, { method: 'DELETE' }),
  // /media/{id} butuh token, jadi diambil sebagai blob
  mediaBlob: async (id) => (await req(`/media/${id}`, { raw: true })).blob(),
}

export const avatarUrl = (username, v = 0) => `${BASE}/profiles/${encodeURIComponent(username)}/avatar?v=${v}`
export const bannerUrl = (username, v = 0) => `${BASE}/profiles/${encodeURIComponent(username)}/banner?v=${v}`

export function timeAgo(iso) {
  if (!iso) return ''
  const hasTz = /(Z|[+-]\d\d:?\d\d)$/.test(iso)
  const s = Math.max(0, (Date.now() - new Date(hasTz ? iso : iso + 'Z').getTime()) / 1000)
  const units = [['year', 31536000], ['month', 2592000], ['day', 86400], ['hour', 3600], ['minute', 60]]
  if (s < 60) return 'just now'
  for (const [name, sec] of units) {
    if (s >= sec) {
      const n = Math.floor(s / sec)
      return `${n} ${name}${n > 1 ? 's' : ''} ago`
    }
  }
}

export const idOf = (x) => x?.id || x?.user_id || x?.followee_id || x?.following_id || x?.follower_id
