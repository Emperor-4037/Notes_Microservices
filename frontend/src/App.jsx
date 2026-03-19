import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Notes from './pages/Notes';
import Study from './pages/Study';
import QA from './pages/QA';

function App() {
  return (
    <>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/notes" element={<Notes />} />
          <Route path="/study" element={<Study />} />
          <Route path="/qa" element={<QA />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
