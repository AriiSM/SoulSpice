"use client"

import { useState, useRef, useEffect, useContext } from "react"
import { Send } from "react-feather"
import { processMessage, getChatHistory } from "../api/api"
import { UserContext } from "../UserContext"
import "./SoulSpice.css"

function SoulSpice() {
  const { userId } = useContext(UserContext)
  const [messages, setMessages] = useState([
    {
      id: Date.now(),
      text: "😃 Hi! I'm SoulSpice, your virtual assistant for culinary wellness. I can offer you advice on healthy eating, recipes tailored to your emotional state, and mindful eating techniques. How are you feeling today, or what kind of craving do you have?",
      sender: "bot",
      timestamp: new Date().toISOString(),
    },
  ])
  const [input, setInput] = useState("")
  const [isTyping, setIsTyping] = useState(false)

  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  // Scroll to last message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // Focus input on load
  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  // Load chat history from backend
  useEffect(() => {
    const fetchHistory = async () => {
      if (!userId) return
      try {
        const history = await getChatHistory(userId)
        if (history?.messages) {
          const formatted = history.messages.map((msg, index) => ({
            id: Date.now() + index,
            text: msg.content,
            sender: msg.role === "assistant" ? "bot" : "user",
            timestamp: msg.timestamp || new Date().toISOString(),
          }))
          setMessages(formatted)
        }
      } catch (error) {
        console.error("Failed to load chat history:", error)
      }
    }

    fetchHistory()
  }, [userId])

  // Format timestamp to readable time
  const formatMessageTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString("ro-RO", { hour: "2-digit", minute: "2-digit" })
  }

  // Handle sending a message
  const handleSubmit = async (e) => {
    e.preventDefault()
    const trimmed = input.trim()
    if (!trimmed) return

    const userMessage = {
      id: Date.now(),
      text: trimmed,
      sender: userId,
      timestamp: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsTyping(true)

    try {
      const response = await processMessage({
        text: trimmed,
        sender: userId,
      })

      const botMessage = {
        id: Date.now() + 1,
        text: response.text || "Nu am putut procesa mesajul.",
        sender: "bot",
        timestamp: response.timestamp || new Date().toISOString(),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      console.error("Error processing message:", error)
      const errorMessage = {
        id: Date.now() + 2,
        text: "⚠️ I'm sorry, I encountered a problem processing your message. Please check your server connection and try again.",
        sender: "bot",
        timestamp: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsTyping(false)
      inputRef.current?.focus()
    }
  }

  // Add emoji to input
  const addEmoji = (emoji) => {
    setInput((prev) => prev + emoji)
    inputRef.current?.focus()
  }

  const quickEmojis = ["😊", "😋", "🍲", "🥗", "🍰", "😢", "🤔", "❤️"]

  return (
    <div className="soulspice-container">
      <div className="chat-card">
        <div className="card-header">
          <div className="header-content">
            <div className="title-section">
              <h2>SoulSpice – Culinary Psychologist</h2>
              <p>
                An assistant that blends psychology with the culinary arts to 
                offer you personalized advice on healthy eating and recipes tailored to your emotional state.
              </p>
            </div>
          </div>
        </div>

        <div className="chat-content">
          <div className="messages-container">
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.sender === "bot" ? "bot-message" : "user-message"}`}>
                <div className={`avatar ${message.sender === "bot" ? "bot-avatar" : "user-avatar"}`}>
                  {message.sender === "bot" ? "Soul" : "Me"}
                </div>
                <div className="message-bubble">
                  <div className="message-text">{message.text}</div>
                  <div className="message-time">{formatMessageTime(message.timestamp)}</div>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="message bot-message">
                <div className="avatar bot-avatar">Soul</div>
                <div className="message-bubble typing">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="emoji-toolbar">
            {quickEmojis.map((emoji, index) => (
              <button 
                key={index} 
                className="emoji-button" 
                onClick={() => addEmoji(emoji)}
                aria-label={`Add emoji ${emoji}`}
              >
                {emoji}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="message-form">
            <input
              id="soulspice-message-input"
              name="soulspiceMessage"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Say how you're feeling or what you're craving..."
              disabled={isTyping}
              className="message-input"
              ref={inputRef}
            />
            <button type="submit" className="send-button" disabled={isTyping || input.trim() === ""}>
              <Send size={18} />
              <span className="sr-only">Trimite mesaj</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default SoulSpice
