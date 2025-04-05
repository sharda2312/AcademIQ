# 🎓 AcademiQ

AcademiQ is a smart, cloud-based quiz platform built with Django and powered by AI. It allows users to create and attempt quizzes — for themselves or others — and even generate quizzes using state-of-the-art AI models like DeepSeek and LLaMA.

## 🚀 Features

- 🔐 **User Authentication**: Register, log in, and manage your account securely.
- 🧠 **AI Quiz Generator**: Generate quizzes using models like DeepSeek and LLaMA.
- 📝 **Self & Public Quizzes**: Create personal quizzes or public ones with a shareable quiz code.
- 📊 **Dashboard**: View all created and attempted quizzes in one place.
- ☁️ **Cloud Ready**: Deployed on [Render](https://render.com/) with infrastructure support via CloudClever.
  
## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Database**: MySQL
- **Deployment**: Render + CloudClever
- **AI Integration**: DeepSeek, LLaMA (LLM-based quiz generation)

## 🧪 Getting Started (Local Development)

```bash
# Clone the repository
git clone https://github.com/sharda2312/academiq.git
cd academiq

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your MySQL DB and apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```
## 🌐 Live Demo
Check out the live version here: https://academiq-t5k5.onrender.com

## 🤖 AI Quiz Generation
Users can choose from supported models when generating AI-based quizzes:

- 🧠 **DeepSeek**

- 🔍 **LLaMA**

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.