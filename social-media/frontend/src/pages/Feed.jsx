import { useCallback, useState } from 'react'
import { api } from '../api.js'
import Composer from '../components/Composer.jsx'
import PostCard from '../components/PostCard.jsx'
import { PageHeader, Paged } from '../components/ui.jsx'

export default function Feed({ kind }) {
  const [fresh, setFresh] = useState([])
  const fetchPage = useCallback((l, o) => api.feed(kind, l, o), [kind])
  return (
    <>
      <PageHeader title={kind === 'foryou' ? 'For you' : 'Following'} />
      {kind === 'foryou' && <Composer onCreated={(p) => setFresh((f) => [p, ...f])} />}
      {kind === 'foryou' && fresh.map((p) => <PostCard key={p.id} post={p} />)}
      <Paged
        key={kind}
        fetchPage={fetchPage}
        render={(p) => <PostCard key={p.id} post={p} />}
        empty={kind === 'foryou' ? 'Belum ada post. Tulis yang pertama!' : 'Belum ada post dari akun yang kamu ikuti. Cari akun menarik dan tekan Follow.'}
      />
    </>
  )
}
