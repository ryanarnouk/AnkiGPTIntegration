import React from 'react';
import PdfUpload from './components/PdfUpload';
import './styles/App.css';
import AnkiCard from './components/AnkiCard';
import GptDropdown from './components/GptDropdown';

function App() {
  return (
    <div className="App">
      <h1>Upload</h1>
      <PdfUpload />
      <AnkiCard />
      <GptDropdown />
    </div>
  );
}

export default App;
