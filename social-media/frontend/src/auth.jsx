import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { api, setUnauthorizedHandler, tokenStore } from './api.js'

const Ctx = createContext(null)
export const useAuth = () => useContext(Ctx)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [profile, setProfile] = useState(null)
  const [ready, setReady] = useState(false)
  const [ver, setVer] = useState(0) // naik setiap profil diubah, untuk refresh avatar/banner

  const logout = useCallback(() => {
    tokenStore.clear()
    setUser(null)
    setProfile(null)
  }, [])

  const load = useCallback(async () => {
    const [u, p] = await Promise.all([api.me(), api.myProfile()])
    setUser(u)
    setProfile(p)
  }, [])

  useEffect(() => {
    setUnauthorizedHandler(logout)
    if (!tokenStore.get()) return setReady(true)
    load().catch(logout).finally(() => setReady(true))
  }, [])

  const login = useCallback(async (username, password) => {
    const t = await api.login(username, password)
    tokenStore.set(t.access_token)
    await load()
  }, [load])

  const register = useCallback(async (b) => {
    await api.register(b)
    await login(b.username, b.password)
  }, [login])

  const refresh = useCallback(async () => {
    await load()
    setVer((v) => v + 1)
  }, [load])

  const me = useMemo(
    () => (user ? { id: user.id, username: user.username, display_name: profile?.display_name } : null),
    [user, profile]
  )

  return <Ctx.Provider value={{ user, profile, me, ready, ver, login, register, logout, refresh }}>{children}</Ctx.Provider>
}

/**
 * Backend sekarang hanya mengirim author_id di PostOut/CommentOut.
 * Kalau backend menambahkan objek `author` {username, display_name}, otomatis dipakai.
 */
export function authorOf(entity, me) {
  if (entity.author) return entity.author
  if (me && entity.author_id === me.id) return me
  return { id: entity.author_id, username: null, display_name: `user-${String(entity.author_id).slice(0, 6)}` }
}
