import React, { useState, useEffect } from 'react';
import DarkModeSwitch from './components/DarkModeSwitch';
import './assets/styles.css';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      setIsDarkMode(savedTheme === 'dark');
    }
  }, []);

  useEffect(() => {
    document.body.className = isDarkMode ? 'dark-mode' : 'light-mode';
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
  }, [isDarkMode]);

  return (
    <div className="app">
      <h1>Welcome to the Creative Web Project</h1>
      <DarkModeSwitch isDarkMode={isDarkMode} toggleDarkMode={() => setIsDarkMode(!isDarkMode)} />
      <p>This is a colorful and creative design project.</p>
    </div>
  );
}

export default App;