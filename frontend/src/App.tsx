import { FormEvent, KeyboardEvent, useEffect, useRef, useState } from 'react'
import './App.css'

type Role = 'user' | 'assistant'

type ChatMessage = {
  id: number | string
  role: Role
  content: string
}

type ChatResponse = {
  session_id: number
  user: ChatMessage
  assistant: ChatMessage
}

type LearningNote = {
  id: number
  category: string
  content: string
  created_at: string
}

type TutorSession = {
  id: number
  title: string
  created_at: string
}

const storedSessionKey = 'frenchTutorSessionId'
const levelOptions = ['beginner', 'A1', 'A2', 'B1']
const modeOptions = ['conversation', 'grammar help', 'roleplay']

function App() {
  const [sessionId, setSessionId] = useState<number | null>(null)
  const [sessions, setSessions] = useState<TutorSession[]>([])
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [learningNotes, setLearningNotes] = useState<LearningNote[]>([])
  const [message, setMessage] = useState('')
  const [level, setLevel] = useState('beginner')
  const [mode, setMode] = useState('conversation')
  const [isSending, setIsSending] = useState(false)
  const [isLoadingSession, setIsLoadingSession] = useState(true)
  const [error, setError] = useState('')
  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoadingSession])

  useEffect(() => {
    const storedSessionId = window.localStorage.getItem(storedSessionKey)

    if (!storedSessionId) {
      setIsLoadingSession(false)
      return
    }

    const parsedSessionId = Number(storedSessionId)
    if (!Number.isInteger(parsedSessionId)) {
      window.localStorage.removeItem(storedSessionKey)
      setIsLoadingSession(false)
      return
    }

    async function loadStoredSession() {
      try {
        const response = await fetch(`/messages/${parsedSessionId}`)

        if (!response.ok) {
          throw new Error('Saved session could not be loaded.')
        }

        const savedMessages = (await response.json()) as ChatMessage[]
        setSessionId(parsedSessionId)
        setMessages(savedMessages)
        loadLearningNotes(parsedSessionId)
      } catch (err) {
        window.localStorage.removeItem(storedSessionKey)
        setError(err instanceof Error ? err.message : 'Saved session could not be loaded.')
      } finally {
        setIsLoadingSession(false)
      }
    }

    loadStoredSession()
  }, [])

  useEffect(() => {
    loadSessions()
  }, [])

  async function loadSessions() {
    try {
      const response = await fetch('/sessions')

      if (!response.ok) {
        throw new Error('Sessions could not be loaded.')
      }

      const savedSessions = (await response.json()) as TutorSession[]
      setSessions(
        savedSessions.sort(
          (first, second) =>
            new Date(second.created_at).getTime() - new Date(first.created_at).getTime(),
        ),
      )
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sessions could not be loaded.')
    }
  }

  async function loadSession(selectedSessionId: number) {
    setIsLoadingSession(true)
    setError('')

    try {
      const response = await fetch(`/messages/${selectedSessionId}`)

      if (!response.ok) {
        throw new Error('Session could not be loaded.')
      }

      const savedMessages = (await response.json()) as ChatMessage[]
      setSessionId(selectedSessionId)
      setMessages(savedMessages)
      setMessage('')
      window.localStorage.setItem(storedSessionKey, String(selectedSessionId))
      loadLearningNotes(selectedSessionId)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Session could not be loaded.')
    } finally {
      setIsLoadingSession(false)
    }
  }

  async function sendMessage(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const trimmedMessage = message.trim()
    if (!trimmedMessage || isSending) {
      return
    }

    setIsSending(true)
    setError('')
    setMessage('')

    const pendingUserMessage: ChatMessage = {
      id: `pending-${Date.now()}`,
      role: 'user',
      content: trimmedMessage,
    }
    setMessages((currentMessages) => [...currentMessages, pendingUserMessage])

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: trimmedMessage,
          session_id: sessionId,
          level,
          mode,
        }),
      })

      if (!response.ok) {
        throw new Error('The tutor could not respond. Please try again.')
      }

      const data = (await response.json()) as ChatResponse

      setSessionId(data.session_id)
      window.localStorage.setItem(storedSessionKey, String(data.session_id))
      setMessages((currentMessages) => [
        ...currentMessages,
        data.assistant,
      ])
      loadSessions()
      loadLearningNotes(data.session_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong.')
    } finally {
      setIsSending(false)
    }
  }

  function startNewSession() {
    window.localStorage.removeItem(storedSessionKey)
    setSessionId(null)
    setMessages([])
    setLearningNotes([])
    setMessage('')
    setError('')
  }

  async function loadLearningNotes(selectedSessionId: number) {
    try {
      const response = await fetch(`/learning-notes/${selectedSessionId}`)

      if (!response.ok) {
        throw new Error('Learning notes could not be loaded.')
      }

      const savedNotes = (await response.json()) as LearningNote[]
      setLearningNotes(savedNotes)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Learning notes could not be loaded.')
    }
  }

  function handleComposerKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      event.currentTarget.form?.requestSubmit()
    }
  }

  function formatSessionDate(createdAt: string) {
    return new Intl.DateTimeFormat(undefined, {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    }).format(new Date(createdAt))
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <aside className="session-panel" aria-label="Tutor settings">
          <div>
            <p className="eyebrow">French Tutor</p>
            <h1>Practice with a patient tutor.</h1>
          </div>

          <label>
            Level
            <select value={level} onChange={(event) => setLevel(event.target.value)}>
              {levelOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label>
            Mode
            <select value={mode} onChange={(event) => setMode(event.target.value)}>
              {modeOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <div className="session-status">
            <span>Session</span>
            <strong>{sessionId ?? 'new'}</strong>
          </div>

          <button className="new-session-button" type="button" onClick={startNewSession}>
            New session
          </button>

          <div className="session-list" aria-label="Saved sessions">
            <div className="session-list-header">
              <span>Saved sessions</span>
              <strong>{sessions.length}</strong>
            </div>

            {sessions.length === 0 ? (
              <p className="session-list-empty">No saved sessions yet.</p>
            ) : (
              sessions.map((tutorSession) => (
                <button
                  className={`session-list-item ${
                    tutorSession.id === sessionId ? 'active' : ''
                  }`}
                  key={tutorSession.id}
                  type="button"
                  onClick={() => loadSession(tutorSession.id)}
                >
                  <span>{tutorSession.title || `Session ${tutorSession.id}`}</span>
                  <small>
                    Session {tutorSession.id} · {formatSessionDate(tutorSession.created_at)}
                  </small>
                </button>
              ))
            )}
          </div>
        </aside>

        <section className="chat-panel" aria-label="Tutor chat">
          <div className="message-list">
            {isLoadingSession ? (
              <div className="empty-state">
                <h2>Loading session.</h2>
                <p>Getting your saved conversation back in place.</p>
              </div>
            ) : messages.length === 0 ? (
              <div className="empty-state">
                <h2>Start with a goal.</h2>
                <p>Try asking to practice ordering coffee, introductions, or travel phrases.</p>
              </div>
            ) : (
              messages.map((chatMessage) => (
                <article
                  className={`message-bubble ${chatMessage.role}`}
                  key={chatMessage.id}
                >
                  <span>{chatMessage.role === 'user' ? 'You' : 'Tutor'}</span>
                  <p>{chatMessage.content}</p>
                </article>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          {learningNotes.length > 0 && (
            <aside className="learning-notes" aria-label="Learning notes">
              <div className="learning-notes-header">
                <span>Learning notes</span>
                <strong>{learningNotes.length}</strong>
              </div>
              <div className="learning-note-list">
                {learningNotes.map((note) => (
                  <article className="learning-note" key={note.id}>
                    <span>{note.category}</span>
                    <p>{note.content}</p>
                  </article>
                ))}
              </div>
            </aside>
          )}

          {error && <p className="error-message">{error}</p>}

          <form className="composer" onSubmit={sendMessage}>
            <textarea
              aria-label="Message"
              placeholder="What would you like to practice?"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              onKeyDown={handleComposerKeyDown}
              rows={3}
            />
            <button type="submit" disabled={isSending || !message.trim()}>
              {isSending ? 'Sending...' : 'Send'}
            </button>
          </form>
        </section>
      </section>
    </main>
  )
}

export default App
