"use client";
import React, { useState } from 'react';

export default function Home() {
  const [description, setDescription] = useState('');
  const [keywords, setKeywords] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log('Form submitted');
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('/api/newsletter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description, keywords, email }),
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        console.error('Failed to fetch. Status:', response.status);
        return;
      }

      const data = await response.json();
      console.log('Received data:', data);
      setResult(data.summaries);
    } catch (error) {
      console.error('Failed to submit form', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <form className="newsletter-form" onSubmit={handleSubmit}>
        <div className="input-section">
          <InputGroup 
            id="description"
            label="Describe in words what you want to read" 
            placeholder="Text here ..."
            className="input-left"
            value={description}
            onChange={(e) => setDescription(e.target.value)} 
          />
          <InputGroup 
            id="keywords" 
            label="Select Keywords"
            placeholder="Keywords here ..."
            className="input-right"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)} 
          />
        </div>

        <div className="email-section">
          <EmailInput value={email} onChange={(e) => setEmail(e.target.value)} />
          <SubmitButton loading={loading} />
        </div>
      </form>

      {result && (
        <div className="results-section">
          <h2>Generated Summaries</h2>
          <ul>
            {result.map((item, index) => (
              <li key={index}>
                <h3>{item[0]}</h3>
                <p>{item[1]}</p>
                <a href={item[2]} target="_blank" rel="noopener noreferrer">Read more</a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function InputGroup({ id, label, placeholder, className, value, onChange }) {
  return (
    <div className={`input-group ${className}`}>
      <label htmlFor={id}>{label}</label>
      <textarea id={id} placeholder={placeholder} value={value} onChange={onChange}></textarea>
    </div>
  );
}

function EmailInput({ value, onChange }) {
  return (
    <div>
      <label htmlFor="email" className="email-label">Enter Your Email Address</label>
      <input type="email" id="email" placeholder="Example@gmail.com" value={value} onChange={onChange} />
    </div>
  );
}

function SubmitButton({ loading }) {
  return (
    <button type="submit" className="submit-button" disabled={loading}>
      {loading ? 'Processing...' : 'Get Your Newsletter'}
    </button>
  );
}
