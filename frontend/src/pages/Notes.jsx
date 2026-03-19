import React, { useState } from 'react';
import { notesApi } from '../services/api';

const Notes = () => {
    const [uploadStatus, setUploadStatus] = useState('');

    const handleUpload = async (e) => {
        e.preventDefault();
        setUploadStatus('Uploading...');

        // Fake upload process since real file handling requires real backend implementation
        setTimeout(async () => {
            try {
                const res = await notesApi.uploadNote(new FormData());
                setUploadStatus(`Success: ${res.data.message}`);
            } catch (err) {
                setUploadStatus('Failed to connect to Notes Service via API Gateway.');
            }
        }, 1500);
    };

    return (
        <div className="page">
            <h2>My <span style={{ color: 'var(--accent-color)' }}>Notes</span></h2>

            <div className="grid grid-cols-2">
                <div className="glass-panel">
                    <h3>Upload Material</h3>
                    <form onSubmit={handleUpload} style={{ marginTop: '1.5rem' }}>
                        <div style={{ border: '2px dashed var(--glass-border)', padding: '2rem', textAlign: 'center', borderRadius: '8px', marginBottom: '1.5rem' }}>
                            <p style={{ color: 'var(--text-secondary)' }}>Drag and drop your PDF or text file here</p>
                            <p style={{ margin: '0.5rem 0', fontSize: '0.9rem' }}>or</p>
                            <input type="file" style={{ display: 'none' }} id="file-upload" />
                            <label htmlFor="file-upload" className="btn btn-secondary">
                                Browse Files
                            </label>
                        </div>
                        <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
                            Upload to Platform
                        </button>

                        {uploadStatus && (
                            <p style={{ marginTop: '1rem', textAlign: 'center', color: uploadStatus.includes('Error') || uploadStatus.includes('Fail') ? 'var(--danger)' : 'var(--success)' }}>
                                {uploadStatus}
                            </p>
                        )}
                    </form>
                </div>

                <div className="glass-panel">
                    <h3>Library</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1.5rem' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                            <span>Introduction_To_Machine_Learning.pdf</span>
                            <span style={{ color: 'var(--success)' }}>Processed</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '1rem', background: 'rgba(255,255,255,0.05)', borderRadius: '8px' }}>
                            <span>Discrete_Math_Chapter_4.pdf</span>
                            <span style={{ color: 'var(--warning)' }}>Processing...</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Notes;
