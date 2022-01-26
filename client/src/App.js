import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import { Table } from 'rsuite';

const { Column, HeaderCell, Cell, Pagination } = Table;

function Td({value, children}) {
  if (value > 0) {
    return <td className='increase'>{children}</td>
  } else if (value < 0) {
    return <td className='decrease'>{children}</td>
  } else {
    return <td className='neutral'>{children}</td>
  }
}

function Link({children}) {
  const link = `https://finance.yahoo.com/quote/${children}`
  return <a href={link} target="_blank">{children}</a>
}

function App() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    // Confused: when I have to work with HTTP calls I had to use http:server (see package.json).
    // With websockets, I have to use localhost:5001 for it to work?

    // Source: https://stackoverflow.com/a/23176223
    const ws_url = "ws://localhost:5001/"
    let ws = new WebSocket(ws_url)
    ws.onopen = () => {
      console.log('connected')
      ws.send(JSON.stringify({'status': 'connected'}));
    }
    ws.onmessage = (e) => {
      setItems(JSON.parse(e.data))
    }

    ws.onclose = function(e) {
      console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
      setTimeout(function() {
        ws = new WebSocket(ws_url)
      }, 1000);
    };
  
    ws.onerror = function(err) {
      console.error('Socket encountered error: ', err.message, 'Closing socket');
      ws = new WebSocket(ws_url)
    };
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <h1>/r/wallstreetbets 📈</h1>
        <table>
        <tr>
          <th>Ticker</th>
          <th>Sentiment</th>
          <th>Volume Change</th>
          <th>Price Change</th>
        </tr>
        {items.map(i => <tr>
          <td><Link>{i.ticker}</Link></td>
          <Td value={i.sentiment}>{i.sentiment}</Td>
          <Td value={i.volume_change}>{i.volume_change}%</Td>
          <Td value={i.price_change}>{i.price_change}%</Td>
        </tr>)}
        </table>
      </header>
    </div>
  );
}

export default App;
