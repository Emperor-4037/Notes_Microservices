import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="container nav-container">
                <NavLink to="/" className="nav-logo">
                    <h2>Study<span>App</span></h2>
                </NavLink>

                <ul className="nav-links">
                    <li>
                        <NavLink to="/dashboard" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                            Dashboard
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/notes" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                            Notes
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/study" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                            Study Session
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/qa" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                            RAG Q&A
                        </NavLink>
                    </li>
                </ul>

                <div className="nav-actions">
                    <button className="btn btn-primary" style={{ padding: '0.5rem 1rem', fontSize: '0.9rem' }}>
                        Login
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
