# AI Newsletter Generator

![image](https://github.com/user-attachments/assets/33a0504c-da07-41dd-ae4a-6e727ae2335d)


## Description
AI Newsletter Generator is a Next.js application that creates personalized newsletters based on user-selected topics and preferences. It uses AI to summarize recent news articles and delivers the content via email.

## Features
- Topic selection for personalized content
- AI-powered article summarization
- Email delivery of personalized newsletters
- Integration with Google's Generative AI (Gemini)

## Technologies Used
- Next.js
- React
- Node.js
- Google Generative AI (Gemini)
- SerpAPI for search results
- Nodemailer for email sending

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-newsletter-generator.git
   cd ai-newsletter-generator
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables:
   Create a `.env.local` file in the root directory and add the following:
   ```
   SERP_API_KEY=your_serp_api_key
   GOOGLE_GENAI_API_KEY=your_google_genai_api_key
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_SECURE=false
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password
   ```

4. Run the development server:
   ```
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Usage
1. Select topics of interest or enter a custom description.
2. Enter your email address.
3. Submit the form to receive a personalized newsletter.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Thanks to Google for providing the Generative AI API.
- SerpAPI for search result data.
- All contributors and maintainers of the open-source libraries used in this project.
