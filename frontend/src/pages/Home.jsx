import React from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="page">
            <div className="hero-section" style={{ textAlign: 'center', marginTop: '4rem' }}>
                <h1 style={{ fontSize: '3.5rem', marginBottom: '1.5rem', background: 'linear-gradient(to right, #60a5fa, #c084fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                    Master Your Studies with AI
                </h1>
                <p style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto 3rem auto' }}>
                    Upload your notes, generate smart flashcards, take AI-driven quizzes, and ask natural language questions about your materials.
                </p>

                <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                    <button className="btn btn-primary" onClick={() => navigate('/dashboard')} style={{ fontSize: '1.1rem', padding: '1rem 2.5rem' }}>
                        Get Started
                    </button>
                    <button className="btn btn-secondary" onClick={() => navigate('/notes')} style={{ fontSize: '1.1rem', padding: '1rem 2.5rem' }}>
                        View Notes
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-3" style={{ marginTop: '6rem' }}>
                <div className="glass-panel text-center">
                    <h3 style={{ color: '#3b82f6' }}>Upload Notes</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>Securely store all your study materials in one place, easily accessible from anywhere.</p>
                </div>
                <div className="glass-panel text-center">
                    <h3 style={{ color: '#8b5cf6' }}>Smart Flashcards</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>Automatically generate key concept flashcards from your uploaded documents using AI.</p>
                </div>
                <div className="glass-panel text-center">
                    <h3 style={{ color: '#10b981' }}>RAG Q&A</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>Ask highly specific questions and get answers directly sourced from your own notes.</p>
                </div>
            </div>
        </div>
    );
};

export default Home;
