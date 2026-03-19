import React, { useEffect, useState } from 'react';
import { userApi } from '../services/api';

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Attempting to hit the User Service through the API Gateway
        userApi.getProfile()
            .then(res => {
                setData(res.data);
                setLoading(false);
            })
            .catch(err => {
                console.error("Dashboard API Error:", err);
                setError("Failed to fetch dashboard data. Make sure the API Gateway and User Service are running.");
                setLoading(false);
            });
    }, []);

    return (
        <div className="page">
            <h2>Welcome Back, <span style={{ color: 'var(--accent-color)' }}>Student!</span></h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>Here is an overview of your progress.</p>

            {error && (
                <div className="glass-panel" style={{ borderLeft: '4px solid var(--danger)', marginBottom: '2rem' }}>
                    <h4 style={{ color: 'var(--danger)' }}>Connection Error</h4>
                    <p>{error}</p>
                </div>
            )}

            <div className="grid grid-cols-2">
                <div className="glass-panel">
                    <h3>Recent Study Sessions</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>Your recently reviewed materials will appear here once you start studying.</p>
                    <div style={{ marginTop: '1.5rem', background: 'rgba(0,0,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
                        <p><strong>Physics 101</strong> - 80% Mastery</p>
                    </div>
                </div>

                <div className="glass-panel">
                    <h3>Upcoming Goals</h3>
                    <p style={{ color: 'var(--text-secondary)' }}>You have no quizzes scheduled for today.</p>
                    <button className="btn btn-secondary" style={{ marginTop: '1.5rem', width: '100%' }}>
                        Resume Last Session
                    </button>
                </div>
            </div>

            <div className="glass-panel" style={{ marginTop: '2rem' }}>
                <h3>API Data Dump</h3>
                <pre style={{ background: 'rgba(0,0,0,0.3)', padding: '1rem', borderRadius: '8px', overflowX: 'auto' }}>
                    {loading ? 'Loading user profile...' : JSON.stringify(data, null, 2)}
                </pre>
            </div>
        </div>
    );
};

export default Dashboard;
