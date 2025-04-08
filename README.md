# Alai-Backend

This repository serves as the backend for Alai's product. This was made by reverse-engineering the frontend and writing the backend code on own.   
View `alai_docs.json` for FastAPI Swagger Docs.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/omkar-334/alai-backend.git
   cd alai-backend
   ```

2. Install dependencies:

     ```bash
     pip install -r requirements.txt
     ```

3. Enter your API keys and login credentials for [Alai](https://app.getalai.com) in the `.env` file:

   ```bash
    GEMINI_API_KEY=  
    FIRECRAWL_API_KEY=  
    TOKEN=  
    EMAIL=  
    PASSWORD=  
   ```

   You don't have to enter the authorization token, It will be automatically fetched and refreshed.

## Usage

To create a presentation, define the URL and number of slides in `main.py`:

   ```python
   from dotenv import load_dotenv

    load_dotenv()

    url = "https://www.theverge.com/news/622380/lenovo-thinkbook-flip-concept-laptop-foldable-mwc"

    ppt_link = main(url, num_slides=4)
    print(f"Presentation link: {ppt_link}")
   ```
