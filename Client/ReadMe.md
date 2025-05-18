# 🎨 SoulSpice Client Documentation

## Overview

The SoulSpice client is a modern React application that provides an intuitive and responsive user interface for interacting with the SoulSpice culinary psychology chatbot. The interface is designed to be warm, engaging, and visually aligned with the culinary wellness theme.

## Features

- **Real-time Chat Interface**: Smooth, animated conversation flow
- **Emoji Support**: Quick-access emotion and food-related emoji toolbar
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **Visual Feedback**: Typing indicators and message status displays
- **Themed Styling**: Custom color scheme reflecting culinary wellness

## Technology Stack

- **React**: Frontend library for building the user interface
- **CSS Variables**: Theme-based styling with custom properties
- **React Hooks**: State management and side effects
- **Axios**: API communication with the SoulSpice server
- **React Feather**: Lightweight icon library

## Project Structure

```
client/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── api/
│   │   └── api.js              # API communication functions
│   ├── ChatBot/
│   │     ├── SoulSpice.js    # Main chat component
│   │     └── SoulSpice.css   # Component styles      
│   ├── App.js                  # Root component
│   └── index.js                # Application entry point
├── package.json
└── README.md
```