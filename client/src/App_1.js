import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';

function App() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    fetch("/test")
    .then(response => response.json())
    .then(data => {
      setItems(data["products"])
      // console.log(items)
    })
    .catch( (err, data) => console.log(err));
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn dasdasdasdiohjasdjkdasdasdasdasdasasdjkh
        </a>
        <ul>
          {items.map(i => <li>{i}</li>)}
        </ul>
      </header>
    </div>
  );
}

export default App;
