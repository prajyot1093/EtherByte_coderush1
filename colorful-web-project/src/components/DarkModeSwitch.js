import React, { useState, useEffect } from 'react';
import './DarkModeSwitch.css'; // Assuming you have a CSS file for styling

const DarkModeSwitch = () => {
    const [isDarkMode, setIsDarkMode] = useState(() => {
        return localStorage.getItem('dark-mode') === 'true';
    });

    const toggleDarkMode = () => {
        setIsDarkMode(prevMode => !prevMode);
    };

    useEffect(() => {
        document.body.classList.toggle('dark-mode', isDarkMode);
        localStorage.setItem('dark-mode', isDarkMode);
    }, [isDarkMode]);

    return (
        <button onClick={toggleDarkMode} className="dark-mode-switch">
            {isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
        </button>
    );
};

export default DarkModeSwitch;