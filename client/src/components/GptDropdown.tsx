import axios from 'axios';
import React, { useState, useEffect, ChangeEvent } from 'react';

const GptDropdown = () => {
    const options = [
        { value: 'gpt-3.5-turbo', label: 'gpt-3.5-turbo (4,097 tokens)' },
        { value: 'gpt-3.5-turbo-16k', label: 'gpt-3.5-turbo-16k (16,385 tokens)' },
        { value: 'gpt-4', label: 'gpt-4 (8,192 tokens)'},
        { value: 'gpt-4-32k', label: 'gpt-4-32k (32,768 tokens)' }
    ];

    const [selectedElement, setSelectedElement] = useState('gpt-3.5-turbo');

    useEffect(() => {
        const fetchData = async () => {
            try {
                await axios.post(`http://127.0.0.1:105/setModel?model=${selectedElement}`);
            } catch (error) {
                alert("Unable to update model");
            }
        };

        fetchData();
    }, [selectedElement]);

    const handleDropdownChange = (event: ChangeEvent<HTMLSelectElement>) => {
        setSelectedElement(event.target.value);
    }

    return (
        <select value={selectedElement} onChange={handleDropdownChange} className='select-input'>
            {options.map(option => (
                <option key={option.value} value={option.value}>{option.label}</option>
            ))}
        </select>
    );
}

export default GptDropdown;