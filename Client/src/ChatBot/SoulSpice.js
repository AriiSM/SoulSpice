"use client"

import { useState, useRef, useEffect } from "react"
import { Send } from "react-feather"
import { processMessage } from "../api/api"
import "./SoulSpice.css"

function SoulSpice() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "😃 Hi! I'm SoulSpice, your virtual assistant for culinary wellness. I can offer you advice on healthy eating, recipes tailored to your emotional state, and mindful eating techniques. How are you feeling today, or what kind of craving do you have?",
      sender: "bot",
      timestamp: new Date().toISOString(),
    },
  ])

  const [input, setInput] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  useEffect(() => {
    // Focus pe input când componenta se încarcă
    inputRef.current?.focus()
  }, [])

  // Formatarea datei pentru afișare
  const formatMessageTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString("ro-RO", { hour: "2-digit", minute: "2-digit" })
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() === "") return;

    // Adaugă mesajul utilizatorului
    const userMessage = {
      id: messages.length + 1,
      text: input,
      sender: "user",
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const userInput = input; // Salvăm inputul într-o variabilă separată
    setInput("");
    setIsTyping(true);

    try {
      // Trimite mesajul către API
      const response = await processMessage({
        text: userInput,
        sender: "user",
      });

      // Adaugă răspunsul botului
      const botMessage = {
        id: messages.length + 2,
        text: response.text || "Nu am putut procesa mesajul.",
        sender: "bot",
        timestamp: response.timestamp || new Date().toISOString(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error processing message:", error);

      // Adaugă un mesaj de eroare
      const errorMessage = {
        id: messages.length + 2,
        text: "⚠️ I'm sorry, I encountered a problem processing your message. Please check your server connection and try again.",
        sender: "bot",
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
      // Focus înapoi pe input după trimiterea mesajului
      inputRef.current?.focus();
    }
  };

  // Adaugă emoji în input
  const addEmoji = (emoji) => {
    setInput((prev) => prev + emoji)
    inputRef.current?.focus()
  }

  // Emoji-uri relevante pentru mâncare și stări emoționale
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
              <div key={message.id} className={`message ${message.sender === "user" ? "user-message" : "bot-message"}`}>
                <div className={`avatar ${message.sender === "user" ? "user-avatar" : "bot-avatar"}`}>
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
                <div className="avatar bot-avatar">CM</div>
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