import React, { useState, useEffect } from 'react';

const DarkModeSwitch = () => {
    const [isDarkMode, setIsDarkMode] = useState(() => {
        const savedMode = localStorage.getItem('dark-mode');
        return savedMode === 'true' || false;
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