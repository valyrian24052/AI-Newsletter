import { NextResponse } from 'next/server';
import axios from 'axios';
import { extract } from '@extractus/article-extractor';
import { GoogleGenerativeAI } from '@google/generative-ai';
import nodemailer from 'nodemailer';

// Initialize the Google Generative AI with your API key
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENAI_API_KEY);

async function getLatestResults(searchSentence) {
    console.log('Fetching latest results for search sentence:', searchSentence);

    const apiKey = process.env.SERP_API_KEY;
    const params = {
        q: searchSentence,
        location: "United States",
        hl: "en",
        gl: "us",
        google_domain: "google.com",
        tbs: "qdr:d", // Time filter (past 24 hours)
        api_key: apiKey,
    };

    try {
        const response = await axios.get('https://serpapi.com/search', { params });
        console.log('Response received from SerpAPI:', response.data);
        const results = response.data;
        const excludedWebsites = ["ft.com", "cointelegraph.com", "cell.com", "futuretools.io"];
        const urls = results.organic_results
            .filter(r => !excludedWebsites.some(site => r.link.includes(site)))
            .slice(0, 5) // Limiting to top 5 for simplicity
            .map(r => r.link);

        console.log('Filtered URLs:', urls);

        return urls;
    } catch (error) {
        console.error('Error fetching results from SerpAPI:', error);
        throw error;
    }
}

async function summarizeText(urls) {
    console.log('Summarizing text...');
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });
    const summarizedTexts = [];

    for (const url of urls) {
        try {
            const article = await extract(url);
            if (!article || !article.content) {
                console.error(`Failed to extract content from ${url}`);
                continue;
            }

            const prompt = `Summarize this text in about 100 words: ${article.content}`;
            const result = await model.generateContent(prompt);
            const summarizedText = result.response.text();

            summarizedTexts.push({ url, summarizedText });

            console.log(`Summary for ${url}:`, summarizedText);
        } catch (error) {
            console.error(`Error summarizing article from ${url}:`, error);
        }
    }

    return summarizedTexts;
}

async function sendEmail(to, subject, content) {
    let transporter = nodemailer.createTransport({
        host: process.env.EMAIL_HOST,
        port: process.env.EMAIL_PORT,
        secure: process.env.EMAIL_SECURE === 'true',
        auth: {
            user: process.env.EMAIL_USER,
            pass: process.env.EMAIL_PASS,
        },
    });

    let info = await transporter.sendMail({
        from: '"Driftio" <noreply@driftio.com>',
        to: to,
        subject: subject,
        html: content,
    });

    console.log("Message sent: %s", info.messageId);
}

export async function POST(req) {
    console.log('API route /api/newsletter hit');
    try {
        const { searchSentence, email } = await req.json();
        console.log('Received search sentence:', searchSentence);
        console.log('Received email:', email);

        const urls = await getLatestResults(searchSentence);
        console.log('Fetched URLs:', urls);

        const summaries = await summarizeText(urls);
        console.log('Generated summaries:', summaries);

        const emailContent = `
            <h1>Your Personalized Newsletter</h1>
            <p><strong>Search query:</strong> ${searchSentence}</p>
            ${summaries.map(summary => `
                <div>
                    <h2>${summary.url}</h2>
                    <p>${summary.summarizedText}</p>
                    <a href="${summary.url}">Read more</a>
                </div>
            `).join('<hr>')}
        `;

        await sendEmail(email, 'DRIFTIO DELIVERY: Here is your personalized newsletter', emailContent);

        return NextResponse.json({ message: 'Your personalized newsletter has been sent to your email.' });
    } catch (error) {
        console.error('Error processing request:', error);
        return NextResponse.json({ error: 'Failed to process your request' }, { status: 500 });
    }
}
