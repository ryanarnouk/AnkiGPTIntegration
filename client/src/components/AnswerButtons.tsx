import React from 'react';

interface AnswerButtonProps {
    time: string[];
    answerClick: (ease: number) => void;
}

const AnswerButtons: React.FC<AnswerButtonProps> = ({ time, answerClick }) => {
    const handleClick = (ease: number) => {
        answerClick(ease);
    }

    return (
        <div className="answer-buttons">
            <button className="button answer" onClick={() => handleClick(0)}>Again {time[0]}</button>
            <button className="button answer" onClick={() => handleClick(1)}>Hard {time[1]}</button>
            <button className="button answer" onClick={() => handleClick(2)}>Good {time[2]}</button>
            <button className="button answer" onClick={() => handleClick(3)}>Easy {time[3]}</button>
        </div>
    )
}

export default AnswerButtons; 