import React, { ChangeEvent, useState } from 'react';
import axios from 'axios';

const PdfUpload: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [deckName, setInputValue] = useState('');

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = event.target.files?.[0];
        if (selectedFile && selectedFile.type === 'application/pdf') {
            setFile(selectedFile);
        } else {
            setFile(null);
        }
    };

    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        setInputValue(event.target.value);
    }

    const handleUpload = async () => {
        if (file) {
            try {
                // TODO: make API URL an env variable
                const apiUrl = `http://127.0.0.1:105/uploadNewNotes?deck=${deckName}`;
                const formData = new FormData();
                formData.append('pdfFile', file);

                const response = await axios.post(apiUrl, formData);
                console.log('API response', response.data);
            } catch (error) {
                console.error('Request failed:', error);
            }
        }
    }

    return (
        <div className="side-view main">
            <div className="side-view">
                <label htmlFor="file-upload" className="upload button">Select File</label>
                <p className="file-name">{file?.name}</p>
            </div>
            <input type="file" accept=".pdf" onChange={handleFileChange} id='file-upload' />
            <input type="text" value={deckName} onChange={handleInputChange} placeholder='Deck name' className='deck-input'/>
            <button onClick={handleUpload} disabled={!file} className='button submit'>
                Upload PDF  
            </button>
        </div>
    )
}

export default PdfUpload;