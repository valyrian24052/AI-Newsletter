"use client";
import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import logo from '../../public/logo.svg';

// Function to get the formatted date for headlines
function getFormattedDate() {
  const today = new Date();
  
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
  const formattedDate = today.toLocaleDateString('en-US', options).replace(',', '').split(' ');
  
  // Convert the date to the format "wednesday-august-21"
  const day = formattedDate[0].toLowerCase();
  const month = formattedDate[1].toLowerCase();
  const date = parseInt(formattedDate[2], 10);

  return `${day}-${month}-${date}`;
}

const Navbar = () => {
  // Generate the top news URL with the current date
  const formattedDate = getFormattedDate();
  const topNewsUrl = `https://www.wmar2news.com/local/top-news-headlines-for-${formattedDate}`;

  return (
    <header className="navbar-container">
      <div className="navbar">
        <div className="navbar-left">
          <Link href="/" passHref legacyBehavior>
            <a>
              <Image src={logo} alt="Logo" width={50} height={50} />
            </a>
          </Link>
          <nav className="navbar-links">
            <Link href="/" passHref legacyBehavior>
              <a className="navbar-link">Home</a>
            </Link>
            {/* Updated dynamic top news link */}
            <Link href={topNewsUrl} passHref legacyBehavior>
              <a target="_blank" rel="noopener noreferrer" className="navbar-link">Headlines</a>
            </Link>
            <Link href="https://news.google.com/home" passHref legacyBehavior>
              <a target="_blank" rel="noopener noreferrer" className="navbar-link">Google News</a>
            </Link>

            
          </nav>
        </div>
        <div className="navbar-right">
          <Link href="https://github.com/valyrian24052/DoseVisor" passHref legacyBehavior>
            <a target="_blank" rel="noopener noreferrer" className="navbar-link">View on GitHub</a>
          </Link>
          <a href="mailto:shashanksharma@gmail.com" className="navbar-link">Connect</a>
        </div>
      </div>
      
      {/* Inline styles with JSX */}
      <style jsx>{`
        .navbar-container {
          width: 100%;
          display: flex;
          justify-content: center;
          background-color: #000;
          padding: 20px 0;
        }
        .navbar {
          width: 100%;
          max-width: 1400px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0 20px;
          position: relative;
        }
        .navbar-left, .navbar-right {
          display: flex;
          align-items: center;
        }
        .navbar-logo img {
          height: 40px;
        }
        .navbar-links {
          display: flex;
          align-items: center;
          gap: 20px;
          margin-left: 20px;
        }
        .navbar-link {
          color: white;
          font-size: 18px;
          font-weight: 500;
          text-decoration: none;
          padding: 5px 0;
          position: relative;
          z-index: 1;
          background: linear-gradient(90deg, white, white);
          background-size: 0% 100%;
          background-repeat: no-repeat;
          transition: background-size 0.6s ease-in-out;
          -webkit-background-clip: text;
          -webkit-text-fill-color: white;
        }
        .navbar-link:hover {
          background-size: 100% 100%;
          background-image: linear-gradient(90deg, #cdffd8, #94b9ff);
          -webkit-text-fill-color: transparent;
        }
        .navbar-right .navbar-link {
          margin-left: 15px;
        }
      `}</style>
    </header>
  );
};

export default Navbar;
