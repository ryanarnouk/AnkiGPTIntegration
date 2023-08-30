import React from 'react';
import PdfUpload from './components/PdfUpload';
import './styles/App.css';
import AnkiCard from './components/AnkiCard';

function App() {
  return (
    <div className="App">
      <h1>Upload</h1>
      <PdfUpload />
      <AnkiCard />
    </div>
  );
}

export default App;
