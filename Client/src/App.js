import logo from './logo.svg';
// import './App.css';
// import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from "./account/Login.js";
import Register from "./account/Register.js";
import SoulSpice from "./ChatBot/SoulSpice.js";
import { UserProvider } from "./UserContext";

function App() {
  return (
    <UserProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path='/dashboard' element={<SoulSpice />} />
        </Routes>
      </Router>
    </UserProvider>
  );
}

export default App;