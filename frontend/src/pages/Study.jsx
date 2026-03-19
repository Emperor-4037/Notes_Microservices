import React, { useState } from 'react';
import { sessionApi } from '../services/api';

const Study = () => {
    const [generating, setGenerating] = useState(false);
    const [systemMessage, setSystemMessage] = useState('');

    const generateMaterial = async (type) => {
        setGenerating(true);
        setSystemMessage(`Requesting generation of ${type}...`);

        try {
            const response = type === 'flashcards'
                ? await sessionApi.createFlashcards(1)
                : await sessionApi.createQuiz(1);

            setSystemMessage(`Response from Study Session Service: ${response.data.message}`);
        } catch (error) {
            setSystemMessage(`Error communicating with Study Session Service: ${error.message}`);
        } finally {
            setGenerating(false);
        }
    };

    return (
        <div className="page">
            <h2>Study <span style={{ color: 'var(--accent-color)' }}>Sessions</span></h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>Active learning through flashcards and quizzes.</p>

            <div className="grid grid-cols-2">
                <div className="glass-panel text-center" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                    <h3 style={{ marginBottom: '1.5rem' }}>AI Flashcards</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>Generate spaced repetition flashcards from your latest notes.</p>
                    <button
                        className="btn btn-primary"
                        onClick={() => generateMaterial('flashcards')}
                        disabled={generating}
                    >
                        {generating ? 'Generating...' : 'Generate Flashcards'}
                    </button>
                </div>

                <div className="glass-panel text-center" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                    <h3 style={{ marginBottom: '1.5rem' }}>Knowledge Quiz</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>Test your understanding with a custom generated multiple-choice quiz.</p>
                    <button
                        className="btn btn-primary"
                        style={{ background: 'linear-gradient(135deg, #10b981, #059669)' }}
                        onClick={() => generateMaterial('quiz')}
                        disabled={generating}
                    >
                        {generating ? 'Generating...' : 'Start New Quiz'}
                    </button>
                </div>
            </div>

            {systemMessage && (
                <div className="glass-panel" style={{ marginTop: '2rem', borderLeft: '4px solid var(--accent-color)' }}>
                    <h4>System Logs</h4>
                    <pre style={{ margin: 0, color: 'var(--text-secondary)' }}>{systemMessage}</pre>
                </div>
            )}
        </div>
    );
};

export default Study;
