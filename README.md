# Ai-based_resume_analyzer

**📌PROJECT OVERVIEW**
The AI-Based Resume Analyzer is a Python application designed to help match resumes with job descriptions using Natural Language Processing (NLP). 
It extracts text from resumes, compares them with job requirements, and generates a similarity score to suggest the best career match. 
A simple GUI (Tkinter) is provided for interaction, along with graphical results (matplotlib).

**🛠 Features**
- Extracts text from PDF/DOCX resumes.
- Uses TF-IDF and cosine similarity to calculate relevance with job descriptions.
- Displays match percentage using pie charts.
- Provides a simple Tkinter-based GUI.
- Handles images and documents with Pillow library.
- Saves the score in PNG format in "charts" folder

**📂 Project Structure**

Resume_Analyzer/

├── charts/                 
│   └── saved_charts.png    
├── resumes/                
│   └── sample_resume.pdf   
├── job_description.txt     
├── resume_analyzer.py      
└── resume_analyzer_gui.py  


**🚀 Future Scope**
- Integration with online job portals.
- Support for large-scale recruiter dashboards.
- Advanced NLP techniques (transformers, BERT).

<img width="1366" height="729" alt="Capture-rsa" src="https://github.com/user-attachments/assets/338aacfb-d769-4fba-80a9-1b4d1a60273c" />
