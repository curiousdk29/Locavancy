# AI Job Search with Contextual Places

This project helps users search for jobs and discover nearby contextual places (cafés, work spots, etc.) around company locations using **Gemini**, **Nominatim**, and **Foursquare APIs**.  

Built for the Hackathon under the theme **Unlocking Contextual Place Information**.

---

## 🚀 Features
- Extract job role & location from natural language prompts using **Gemini API**.
- Fetch job listings via **RapidAPI**.
- Get company coordinates using **Nominatim API**.
- Discover nearby places (cafés, co-working spots, etc.) using **Foursquare Places API**.
- Interactive frontend with instant job results while nearby place data loads asynchronously.

---

## 🛠 Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript (AJAX for async updates)
- **APIs**: Gemini, RapidAPI, Nominatim, Foursquare
- **Database**: SQLite (default Django)

---

## 📂 Setup Instructions

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
1.git clone https://github.com/your-username/your-repo.git
cd your-repo
2. Create a `.env` file in the root folder
3. Add the following variables (replace with your own keys):
   - GEMINI_API_KEY
   - RAPIDAPI_KEY
   - FSQ_API_KEY
4. python -m venv venv for creating a virtual environment
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py runserver

