import axios from 'axios';
import { Article } from 'newspaper-js';
import { TextServiceClient } from '@google-cloud/genai';
import dotenv from 'dotenv';

dotenv.config();

async function getLatestResults(keywords) {
    console.log('Fetching latest results for keywords:', keywords);

    const apiKey = process.env.SERP_API_KEY;
    const params = {
        q: keywords.join(" "), // Combine keywords into a single search string
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
    const client = new TextServiceClient();
    const apiKey = process.env.GOOGLE_GENAI_API_KEY;
    const summarizedTexts = [];

    for (const url of urls) {
        try {
            const article = new Article(url);
            await article.download();
            article.parse();

            const [summarizedTextResponse] = await client.generateText({
                apiKey,
                prompt: `Summarize this text: ${article.text}`,
            });

            const summarizedText = summarizedTextResponse.text;
            summarizedTexts.push({ url, summarizedText });

            console.log(`Summary for ${url}:`, summarizedText);
        } catch (error) {
            console.error(`Error summarizing article from ${url}:`, error);
        }
    }

    return summarizedTexts;
}

export async function POST(req) {
    console.log('API route /api/newsletter hit');
    try {
        const { keywords } = await req.json();
        console.log('Received keywords:', keywords);

        const urls = await getLatestResults(keywords);
        console.log('Fetched URLs:', urls);

        const summaries = await summarizeText(urls);
        console.log('Generated summaries:', summaries);

        return new Response(JSON.stringify({ summaries }), {
            status: 200,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    } catch (error) {
        console.error('Error processing request:', error);
        return new Response(JSON.stringify({ error: 'Failed to process your request' }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }
}
