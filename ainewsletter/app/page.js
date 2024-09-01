import React from 'react';

export default function Home() {
  return (
    <div className="container">
      <form className="newsletter-form">
        <div className="input-section">
          <InputGroup 
            id="description" 
            label="Describe in words what you want to read" 
            placeholder="Text here ..."
            className="input-left" // Assign a class for the left input
          />
          <InputGroup 
            id="keywords" 
            label="Select Keywords" 
            className="input-right" // Assign a class for the right input
          />
        </div>

        <div className="email-section">
          <EmailInput />
          <SubmitButton />
        </div>
      </form>
    </div>
  );
}

function InputGroup({ id, label, placeholder, className }) {
  return (
    <div className={`input-group ${className}`}>
      <label htmlFor={id}>{label}</label>
      <textarea id={id} placeholder={placeholder}></textarea>
    </div>
  );
}

function EmailInput() {
  return (
    <div>
      <label htmlFor="email" className="email-label">Enter Your Email Address</label>
      <input type="email" id="email" placeholder="Example@gmail.com" />
    </div>
  );
}

function SubmitButton() {
  return (
    <button type="submit" className="submit-button">
      Get Your Newsletter
    </button>
  );
}
