import os
import re
import docx2txt
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import PyPDF2
import glob

# Download necessary NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

class ResumeAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.job_descriptions = {}
        self.resume_text = ""
        self.name = ""
        self.job_matches = {}
        self.normalized_job_matches = {}
        self.best_match = ""
        self.best_score = 0
        self.best_normalized_score = 0
        self.resume_file = ""

    def clean_text(self, text):
        """Clean and preprocess text data"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove stopwords
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)

    def load_job_descriptions(self):
        """Load job descriptions from a single file"""
        job_file = "job_description.txt"
        
        if not os.path.exists(job_file):
            print(f"Job description file '{job_file}' not found! Please create this file.")
            return False
            
        try:
            with open(job_file, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Split content by section headers (===== ROLE =====)
            sections = re.split(r'={5}\s+(.*?)\s+={5}', content)
            
            # First section is empty (before first header)
            sections = sections[1:]  
            
            # Process sections in pairs (header, content)
            for i in range(0, len(sections), 2):
                if i+1 < len(sections):
                    role_name = sections[i].strip()
                    job_text = sections[i+1].strip()
                    self.job_descriptions[role_name] = self.clean_text(job_text)
                    print(f"Loaded '{role_name}' job description")
            
            if not self.job_descriptions:
                print("No job descriptions found in the file!")
                return False
                
            print(f"Found {len(self.job_descriptions)} job descriptions.")
            return True
                
        except Exception as e:
            print(f"Error loading job descriptions: {e}")
            return False

    def get_user_input(self):
        """Get user name and target job role"""
        print("\n" + "="*50)
        print("🚀 RESUME ANALYZER - CAREER MATCH FINDER 🚀")
        print("="*50)
        
        self.name = input("\nWhat's your name? ")
        print(f"\nHello {self.name}! Let's analyze your resume and find your best career match.")
        
        # List available resume files
        resume_files = []
        for extension in ['*.docx', '*.pdf']:
            resume_files.extend(glob.glob(os.path.join("resumes", extension)))
            
        if not resume_files:
            print("\nNo resume files found in the 'resumes' folder!")
            print("Please add a .docx or .pdf file to the 'resumes' folder and try again.")
            return False
            
        print("\nAvailable resume files:")
        for i, file in enumerate(resume_files, 1):
            print(f"{i}. {os.path.basename(file)}")
            
        while True:
            try:
                selection = int(input("\nEnter the number of your resume file: "))
                if 1 <= selection <= len(resume_files):
                    self.resume_file = resume_files[selection-1]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a number.")
                
        return True

    def extract_text_from_file(self):
        """Extract text from resume file (PDF or DOCX)"""
        filename = self.resume_file.lower()
        try:
            if filename.endswith('.pdf'):
                with open(self.resume_file, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()
            elif filename.endswith('.docx'):
                text = docx2txt.process(self.resume_file)
            else:
                print(f"Unsupported file format: {self.resume_file}")
                return False
                
            if not text:
                print(f"Could not extract text from {self.resume_file}")
                return False
                
            self.resume_text = self.clean_text(text)
            return True
            
        except Exception as e:
            print(f"Error processing {self.resume_file}: {e}")
            return False

    def calculate_similarities(self):
        """Calculate similarity between resume and all job descriptions"""
        if not self.resume_text:
            return False
            
        for role, job_text in self.job_descriptions.items():
            # Create a TF-IDF Vectorizer
            vectorizer = TfidfVectorizer()
            
            # Transform documents to TF-IDF matrix
            tfidf_matrix = vectorizer.fit_transform([self.resume_text, job_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            # Round to nearest integer (whole number)
            match_percentage = round(similarity * 100)
            
            self.job_matches[role] = match_percentage
        
        # Normalize job matches right away
        self.normalize_job_matches()
        
        # Set best match based on normalized scores
        for role, score in self.normalized_job_matches.items():
            if score > self.best_normalized_score:
                self.best_normalized_score = score
                self.best_match = role
                self.best_score = self.job_matches[role]  # Keep original score for reference
                
        return len(self.job_matches) > 0

    def normalize_job_matches(self):
        """Normalize job match percentages to sum to 100%"""
        total_match = sum(self.job_matches.values())
        if total_match > 0:
            for role, score in self.job_matches.items():
                self.normalized_job_matches[role] = round((score / total_match) * 100)

    def display_results(self):
        """Display analysis results and visualization"""
        if not self.job_matches:
            return
            
        print("\n" + "="*50)
        print(f"📊 RESUME ANALYSIS RESULTS FOR {self.name.upper()} 📊")
        print("="*50)
        
        # Display only normalized percentages
        print("\nCareer match percentages (normalized to 100%):")
        for role, score in sorted(self.normalized_job_matches.items(), key=lambda x: x[1], reverse=True):
            print(f"🔹 {role}: {score}%")
    
        print("\n" + "-"*50)
        print(f"✨ BEST CAREER MATCH: {self.best_match} ({self.normalized_job_matches[self.best_match]}%) ✨")
        
        # Provide feedback based on normalized match percentage
        normalized_score = self.normalized_job_matches[self.best_match]
        if normalized_score < 40:  # Adjusted thresholds for normalized scores
            print("\n⚠️ Your resume has a relatively low match with this role.")
            print("Suggestions to improve your match:")
            print("1. Add more keywords relevant to the job description")
            print("2. Highlight projects and experiences related to the role")
            print("3. Quantify your achievements with specific metrics")
            print("4. Consider acquiring additional skills mentioned in the job description")
        elif normalized_score < 60:  # Adjusted threshold
            print("\n👍 Your resume has a good match, but could be improved.")
            print("Suggestions to strengthen your application:")
            print("1. Emphasize your most relevant experiences for this role")
            print("2. Add more industry-specific terminology")
            print("3. Tailor your resume objective/summary to this specific position")
        else:
            print("\n🎉 Excellent match! Your resume is well-aligned with this role.")
            print("Next steps:")
            print("1. Prepare for interviews by researching the company")
            print("2. Practice explaining how your experience relates to the role's requirements")
            print("3. Consider preparing a portfolio of relevant work samples")
        
        # Create visualization of results
        self.create_visualization()

    def create_visualization(self):
        """Create a pie chart showing normalized match percentages"""
        roles = list(self.normalized_job_matches.keys())
        scores = list(self.normalized_job_matches.values())
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            scores, 
            labels=roles,
            autopct='%1.0f%%',
            startangle=90,
            shadow=True,
            wedgeprops={'edgecolor': 'black'}
        )
        
        # Customize text appearance
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
            
        for text in texts:
            text.set_fontsize(9)
        
        # Add title
        ax.set_title(f'Resume Match Analysis for {self.name}', fontsize=14, fontweight='bold')
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the figure
        plt.savefig('resume_match_analysis.png')
        print("\n📈 Visualization saved as 'resume_match_analysis.png'")
        
        # Show the chart
        plt.show()

    def run(self):
        """Run the complete resume analysis process"""
        # Check for resumes directory
        if not os.path.exists("resumes"):
            print("'resumes' directory not found. Creating it now...")
            os.makedirs("resumes")
            print("Please add your resume files to the 'resumes' folder and run the program again.")
            return
            
        # Load job descriptions
        if not self.load_job_descriptions():
            return
            
        # Get user input
        if not self.get_user_input():
            return
            
        # Extract text from resume
        if not self.extract_text_from_file():
            return
            
        # Calculate similarities
        if not self.calculate_similarities():
            return
            
        # Display results
        self.display_results()
        

if __name__ == "__main__":
    analyzer = ResumeAnalyzer()
    analyzer.run()