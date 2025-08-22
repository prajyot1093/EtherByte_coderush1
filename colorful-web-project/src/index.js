import React from 'react';
import ReactDOM from 'react-dom';
import './styles/main.css';
import DarkModeSwitch from './components/DarkModeSwitch';

const App = () => {
    return (
        <div className="app">
            <h1>Welcome to the Colorful Web Project</h1>
            <DarkModeSwitch />
            <p>This is a colorful design with a dark mode feature!</p>
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));