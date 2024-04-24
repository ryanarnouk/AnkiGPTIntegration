import axios from 'axios';
import React, { useState, useEffect, ChangeEvent } from 'react';

const GptDropdown = () => {
    const options = [
        { value: 'gpt-3.5-turbo', label: 'gpt-3.5-turbo (4,097 tokens)' },
        { value: 'gpt-3.5-turbo-16k', label: 'gpt-3.5-turbo-16k (16,385 tokens)' },
        { value: 'gpt-4', label: 'gpt-4 (8,192 tokens)'},
        { value: 'gpt-4-32k', label: 'gpt-4-32k (32,768 tokens)' }
    ];

    const tfOptions = [
        { value: 'True', label: 'Use T/F Questions' },
        { value: 'False', label: 'Normal Questions' },
    ];

    const [selectedElement, setSelectedElement] = useState('gpt-3.5-turbo');
    const [trueFalseElement, setTrueFalseElement] = useState("False");

    useEffect(() => {
        const fetchData = async () => {
            try {
                await axios.post(`http://127.0.0.1:105/setModel?model=${selectedElement}&tf=${trueFalseElement}`);
            } catch (error) {
                alert("Unable to update model");
            }
        };

        fetchData();
    }, [selectedElement, trueFalseElement]);

    const handleDropdownChange = (event: ChangeEvent<HTMLSelectElement>) => {
        setSelectedElement(event.target.value);
    }

    const handleSetTrueFalseChange = (event: ChangeEvent<HTMLSelectElement>) => {
        setTrueFalseElement(event.target.value);
    }

    return (
        <div>
            <select value={selectedElement} onChange={handleDropdownChange} className='select-input'>
                {options.map(option => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                ))}
            </select>
            <select value={trueFalseElement} onChange={handleSetTrueFalseChange} className='select-input'>
                {tfOptions.map(option => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                ))}
            </select>
        </div>
    );
}

export default GptDropdown;