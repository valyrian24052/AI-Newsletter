import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from './components/navbar';

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Driftio",
  description: "AI Newsletter",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/logo.svg" type="image/svg+xml" />
        {/* Add other meta tags here as needed */}
      </head>
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
