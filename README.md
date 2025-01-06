

 **Blend.ai**:

---

# Blend.ai - Dish Specific Answer Engine  

### 🥘 Overview  
**Blend.ai** is an application designed to provide detailed insights into restaurant dishes by aggregating reviews from platforms like Yelp and Reddit. The app leverages user-generated content to help diners make informed decisions when faced with unfamiliar menu items.  

---

### 🎯 Core Idea  
Ever found yourself at a restaurant staring at an unknown dish on the menu, unsure if it will suit your taste? **Blend.ai** solves this by:  
1. Capturing the restaurant location and dish name.  
2. Fetching user reviews from Yelp and Reddit.  
3. Analyzing and structuring the data into actionable insights.  
4. Generating personalized responses to user queries with customization options and additional helpful information.  

---

### 🚀 Features  

#### **Frontend**  
- **Tech Stack**: Next.js + Tailwind CSS + TypeScript  
- **Real-time Application** – Immediate feedback and dynamic interactions.  
- **Query History with URLs** – Each query generates a unique URL, allowing users to revisit or share past queries. This feature was inspired by a need for enhanced query navigation, similar to how Perplexity operates.  
- **Interactive User Prompts** – Jump directly to specific query results or follow-up questions by selecting from previous prompts.  

#### **Backend**  
- **Architecture**: Refer to the architecture diagram for detailed structure.  
- **Key Components**:  
  - **Retrieval-Augmented Generation (RAG) Pipeline** – Fetches and analyzes relevant data from review platforms.  
  - **Follow-ups** – Supports additional user questions related to previous queries.  
  - **LLM Integration** – Powered by Llama and other large language models to enhance the quality of generated responses.  

---

### ⚙️ How it Works  
1. **User Input** – The user enters the dish name and restaurant location.  
2. **Data Collection** – The app pulls relevant reviews from Yelp and Reddit.  
3. **Analysis & Summarization** – The backend processes the data through the RAG pipeline, distilling insights into concise, user-friendly outputs.  
4. **Customization** – Users can refine their queries or request additional recommendations, adjusting preferences as needed.  

---

### 🛠️ Tech Stack  
- **Frontend**:  
  - Next.js  
  - Tailwind CSS  
  - TypeScript  
- **Backend**:  
  - FastAPI  
  - GraphQL  
  - MongoDB  
  - Llama (Meta) for LLM Integration  
- **APIs**: Yelp API, Reddit API  

---

### 📄 Future Enhancements  
- **Expanded Dish Recommendations** – Broaden review sources and integrate with other platforms.  
- **Gen AI Customization** – Fine-tune Llama to improve response quality.  
- **Visual Review Summaries** – Implement graphs and visual data representations.  
- **Enhanced Personalization** – Allow users to save dish preferences for future visits.  

---

### 📌 Getting Started  
1. Clone the repository.  
2. Install dependencies:  
   ```bash
   npm install
   ```  
3. Start the development server:  
   ```bash
   npm run dev
   ```  
4. Configure backend API and database connections in `.env` file.  

---

Let me know if you want to add sections like **Contributing**, **License**, or **FAQ**!