import React, { useState } from 'react';
import { qaApi } from '../services/api';

const QA = () => {
    const [question, setQuestion] = useState('');
    const [chat, setChat] = useState([
        { role: 'ai', text: 'Hello! I am your RAG study assistant. Ask me anything about your uploaded materials.' }
    ]);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question.trim()) return;

        const userMsg = { role: 'user', text: question };
        setChat(prev => [...prev, userMsg]);
        setQuestion('');
        setLoading(true);

        try {
            const response = await qaApi.askQuestion(userMsg.text, 1);

            setChat(prev => [...prev, {
                role: 'ai',
                text: `Backend Response: ${response.data.message} \n\n(This is a placeholder. A real RAG pipeline will return contextually retrieved answers here.)`
            }]);
        } catch (error) {
            setChat(prev => [...prev, {
                role: 'ai',
                text: 'Sorry, I failed to reach the RAG QA service. Is the backend running?'
            }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page" style={{ height: 'calc(100vh - 80px)', display: 'flex', flexDirection: 'column' }}>
            <h2>RAG <span style={{ color: 'var(--accent-color)' }}>Tutor</span></h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>Ask questions and get answers directly from your study context.</p>

            <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '1.5rem', overflow: 'hidden' }}>
                <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1.5rem' }}>
                    {chat.map((msg, index) => (
                        <div key={index} style={{
                            alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                            background: msg.role === 'user' ? 'rgba(59, 130, 246, 0.2)' : 'rgba(255, 255, 255, 0.05)',
                            border: `1px solid ${msg.role === 'user' ? 'rgba(59, 130, 246, 0.4)' : 'var(--glass-border)'}`,
                            padding: '1rem 1.5rem',
                            borderRadius: '12px',
                            maxWidth: '80%',
                            lineHeight: '1.5'
                        }}>
                            {msg.text}
                        </div>
                    ))}
                    {loading && (
                        <div style={{ alignSelf: 'flex-start', color: 'var(--text-secondary)' }}>
                            <i>AI is thinking...</i>
                        </div>
                    )}
                </div>

                <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '1rem' }}>
                    <input
                        type="text"
                        className="input-field"
                        style={{ margin: 0 }}
                        placeholder="Type your question..."
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        disabled={loading}
                    />
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
};

export default QA;
