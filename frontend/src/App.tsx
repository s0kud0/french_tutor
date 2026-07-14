import { FormEvent, useEffect, useState } from 'react'
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

const storedSessionKey = 'frenchTutorSessionId'
const levelOptions = ['beginner', 'A1', 'A2', 'B1']
const modeOptions = ['conversation', 'grammar help', 'roleplay']

function App() {
  const [sessionId, setSessionId] = useState<number | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [message, setMessage] = useState('')
  const [level, setLevel] = useState('beginner')
  const [mode, setMode] = useState('conversation')
  const [isSending, setIsSending] = useState(false)
  const [isLoadingSession, setIsLoadingSession] = useState(true)
  const [error, setError] = useState('')

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
      } catch (err) {
        window.localStorage.removeItem(storedSessionKey)
        setError(err instanceof Error ? err.message : 'Saved session could not be loaded.')
      } finally {
        setIsLoadingSession(false)
      }
    }

    loadStoredSession()
  }, [])

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
    setMessage('')
    setError('')
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
          </div>

          {error && <p className="error-message">{error}</p>}

          <form className="composer" onSubmit={sendMessage}>
            <textarea
              aria-label="Message"
              placeholder="What would you like to practice?"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
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
