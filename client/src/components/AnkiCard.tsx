import React, { ChangeEvent, useEffect, useState } from 'react';
import io, { Socket } from 'socket.io-client';
import AnswerButtons from './AnswerButtons';

interface CardData {
    cardId: number;
    fields: {
        Front: {
            value: string;
            order: number;
        };
        Back: {
            value: string;
            order: number;
        };
    };
    fieldOrder: number;
    question: string;
    answer: string;
    buttons: number[];
    nextReviews: string[];
    modelName: string;
    deckName: string;
    css: string;
    template: string;
}

const AnkiCard: React.FC = () => {
    const [currentCard, setCurrentCard] = useState<CardData | null>(null);
    const [answer, setAnswer] = useState('');
    const [answerScore, setAnswerScore] = useState('');
    const [socket, setSocket] = useState<Socket | null>(null);

    useEffect(() => {
        const socket = io('http://127.0.0.1:105');
        setSocket(socket);
        
        socket.on('connect', () => {
            console.log('Connected to web socket server');

            socket.emit('get_current_card');
        });

        socket.on('card', (data) => {
            setCurrentCard(JSON.parse(data) as CardData);
        })

        return () => {
            socket.disconnect();
        }
    }, []);

    const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
        setAnswer(event.target.value);
    }

    const handleSubmit = async () => {
        if (answer.length > 0 && currentCard != null && socket) {
            try {
                const requestBody = {
                    question: currentCard.fields.Front.value,
                    userAnswer: answer, 
                    aiAnswer: currentCard.fields.Back.value
                };
                
                socket.emit('score_answer', requestBody);
                setAnswerScore('Loading...');

                socket.on('score', (response) => {
                    setAnswerScore(response);
                    console.log('Response', response);
                });
            } catch (error) {
                console.error('Request failed:', error);
            }
        } else {
            alert('Empty answer');
        }
    }

    const handleAnswerSubmit = async (ease: number) => {
        if (socket) {
            socket.emit('submit_card', ease);

            socket.on('submit', (response) => {
                if (!response) {
                    alert("Could not submit card. Answer needs to be open on Anki for this method to work");
                }
            })
        }
    }

    return (
        <div>
            <h1>Anki Integration</h1>
            <p>{currentCard != null ? currentCard.fields.Front.value : "GUI does not have a currently selected card. Or, the web socket connection cannot be reached"}</p>
            <input type='text' value={answer} onChange={handleInputChange} placeholder='Your answer'/>
            <button onClick={handleSubmit}>
                Submit Answer
            </button>
            <p>{answerScore}</p>
            {currentCard != null ? <AnswerButtons time={currentCard.nextReviews} answerClick={handleAnswerSubmit} /> : undefined}
        </div>
    )
}

export default AnkiCard;