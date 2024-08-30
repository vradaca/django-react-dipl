import React from 'react';
import '../CSS/Navbar.css';

function Navbar({ scrollToLayer }) {
  return (
    <nav className="navbar">
      <div className="nav-logo">Budget Manager</div>
      <div className="nav-links">
        <a href="#home" className="nav-item" onClick={() => scrollToLayer(0)}>Home</a>
        <a href="#about" className="nav-item" onClick={() => scrollToLayer(1)}>About</a>
        <a href="#services" className="nav-item" onClick={() => scrollToLayer(2)}>Services</a>
        <a href="#contact" className="nav-item" onClick={() => scrollToLayer(3)}>Contact</a>
      </div>
    </nav>
  );
}

export default Navbar;
