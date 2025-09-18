import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import datetime 
import sys
from resume_analyzer import ResumeAnalyzer  # Import the original class

class ResumeAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Resume Analyzer - Career Match Finder")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")  # Slightly lighter background
        
        # Initialize analyzer
        self.analyzer = ResumeAnalyzer()
        
        # Variables
        self.name_var = tk.StringVar()
        self.resume_path_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready to analyze your resume")
        
        # Apply professional color theme
        self.apply_theme()
        
        # Create charts directory
        self.charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
        if not os.path.exists(self.charts_dir):
            os.makedirs(self.charts_dir)
        
        # Create GUI elements
        self.create_gui()
        
        # Try to load job descriptions automatically
        self.load_job_descriptions()

    def apply_theme(self):
        """Apply professional color theme to the application"""
        # Define colors
        self.colors = {
            "primary": "#2c3e50",      # Dark blue-gray for main elements
            "secondary": "#ecf0f1",    # Light gray for backgrounds
            "accent": "#3498db",       # Blue for highlights
            "text_dark": "#2c3e50",    # Dark text color
            "text_light": "#ffffff",   # Light text color
            "input_bg": "#ffffff",     # White background for input fields
            "success": "#2ecc71",      # Green for success messages
            "warning": "#f39c12",      # Orange for warnings
            "frame_bg": "#e8eef1"      # Light blue-gray for frames
        }
        
        # Create custom styles
        style = ttk.Style()
        
        # Configure the main styles
        style.configure("TFrame", background=self.colors["secondary"])
        style.configure("TLabel", background=self.colors["secondary"], foreground=self.colors["text_dark"])
        style.configure("TButton", background=self.colors["primary"], foreground=self.colors["text_dark"])
        
        # Custom styles for specific elements
        style.configure("Header.TLabel", 
                       font=("Arial", 18, "bold"), 
                       background=self.colors["secondary"], 
                       foreground=self.colors["primary"])
        
        style.configure("Title.TLabel", 
                       font=("Arial", 14, "bold"), 
                       background=self.colors["primary"], 
                       foreground=self.colors["text_light"],
                       padding=10)
        
        style.configure("Accent.TButton", 
                       background=self.colors["accent"], 
                       foreground=self.colors["text_dark"])
        
        style.map("Accent.TButton",
                 background=[("active", self.colors["primary"])])
        
        # Create custom frame styles
        style.configure("Primary.TLabelframe", 
                       background=self.colors["primary"],
                       foreground=self.colors["text_light"])
        
        style.configure("Primary.TLabelframe.Label", 
                       background=self.colors["primary"],
                       foreground=self.colors["text_light"],
                       font=("Arial", 12, "bold"))
        
        style.configure("Secondary.TLabelframe", 
                       background=self.colors["frame_bg"])
        
        style.configure("Secondary.TLabelframe.Label", 
                       background=self.colors["primary"],
                       foreground=self.colors["text_light"],
                       font=("Arial", 12, "bold"))
        
        style.configure("Results.TFrame", 
                       background=self.colors["frame_bg"])
        
        style.configure("Chart.TFrame", 
                       background="#f8f9fa")  # Light gray for chart background

    def create_gui(self):
        """Create all GUI elements"""
        # Main frame with custom background
        main_frame = ttk.Frame(self.root, padding=20, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with custom style
        title_frame = ttk.Frame(main_frame, style="TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame, 
            text="Resume Analyzer - Career Match Finder",
            style="Header.TLabel"
        )
        title_label.pack(pady=(0, 10))
        
        # Input section with primary color theme
        input_frame = ttk.LabelFrame(
            main_frame, 
            text="Input Details", 
            padding=15,
            style="Primary.TLabelframe"
        )
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Custom frame inside for the content with different background
        input_content = ttk.Frame(input_frame, style="TFrame")
        input_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Name input
        name_label = ttk.Label(input_content, text="Your Name:")
        name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        name_entry = ttk.Entry(input_content, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Resume file selection
        resume_label = ttk.Label(input_content, text="Resume File:")
        resume_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        resume_entry = ttk.Entry(input_content, textvariable=self.resume_path_var, width=50)
        resume_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        browse_button = ttk.Button(
            input_content, 
            text="Browse", 
            command=self.browse_resume
        )
        browse_button.grid(row=1, column=2, padx=5, pady=5)
        
        # Analyze button
        analyze_button = ttk.Button(
            input_content,
            text="Analyze Resume",
            command=self.run_analysis,
            style="Accent.TButton"
        )
        analyze_button.grid(row=2, column=1, pady=15)
        
        # Status bar
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5, 2),
            background=self.colors["primary"],
            foreground=self.colors["text_light"]
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Results section - Create but don't pack yet
        self.results_frame = ttk.LabelFrame(
            main_frame, 
            text="Analysis Results", 
            padding=15,
            style="Secondary.TLabelframe"
        )
        
    def browse_resume(self):
        """Open file dialog to select resume file"""
        filetypes = (
            ("Document files", "*.docx *.pdf"),
            ("Word documents", "*.docx"),
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            title="Select Resume File",
            initialdir="./resumes",
            filetypes=filetypes
        )
        
        if filename:
            self.resume_path_var.set(filename)
            
    def load_job_descriptions(self):
        """Load job descriptions and update status"""
        self.status_var.set("Loading job descriptions...")
        self.root.update_idletasks()
        
        result = self.analyzer.load_job_descriptions()
        
        if result:
            self.status_var.set(f"Loaded {len(self.analyzer.job_descriptions)} job descriptions")
        else:
            self.status_var.set("Error: Could not load job descriptions")
            messagebox.showerror(
                "Error",
                "Could not load job descriptions. Please make sure 'job_description.txt' file exists."
            )
            
    def run_analysis(self):
        """Run the resume analysis and display results"""
        # Check if inputs are valid
        name = self.name_var.get().strip()
        resume_path = self.resume_path_var.get().strip()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter your name")
            return
            
        if not resume_path or not os.path.exists(resume_path):
            messagebox.showwarning("Warning", "Please select a valid resume file")
            return
            
        # Set values in analyzer
        self.analyzer.name = name
        self.analyzer.resume_file = resume_path
        
        # Update status
        self.status_var.set("Analyzing resume...")
        self.root.update_idletasks()
        
        # Extract text from resume
        if not self.analyzer.extract_text_from_file():
            self.status_var.set("Error: Could not extract text from resume")
            messagebox.showerror("Error", "Could not extract text from the resume file")
            return
            
        # Calculate similarities
        if not self.analyzer.calculate_similarities():
            self.status_var.set("Error: Could not analyze resume")
            messagebox.showerror("Error", "Could not analyze the resume")
            return
            
        # Show results
        self.display_results()
        
    def display_results(self):
        """Display analysis results in the GUI with horizontal layout"""
        # Update status
        self.status_var.set("Analysis complete")
        
        # Clear and recreate results frame to avoid stacking issues
        if hasattr(self, 'results_frame') and self.results_frame.winfo_ismapped():
            self.results_frame.pack_forget()
            
        # Recreate results frame with secondary style
        main_frame = self.root.winfo_children()[0]  # Get the main frame
        self.results_frame = ttk.LabelFrame(
            main_frame, 
            text="Analysis Results", 
            padding=15,
            style="Secondary.TLabelframe"
        )
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Create a horizontal layout with two frames side by side
        horizontal_frame = ttk.Frame(self.results_frame, style="Results.TFrame")
        horizontal_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns to give more space to text and less to chart
        horizontal_frame.columnconfigure(0, weight=3)  # More space for text
        horizontal_frame.columnconfigure(1, weight=2)  # Less space for chart
        
        # Left side for text results
        text_frame = ttk.Frame(horizontal_frame, style="Results.TFrame")
        text_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        # Create text widget with custom background
        self.results_text = tk.Text(
            text_frame, 
            wrap=tk.WORD, 
            width=40, 
            height=20,
            bg=self.colors["input_bg"],
            fg=self.colors["text_dark"],
            borderwidth=1,
            relief="solid"
        )
        self.results_text.grid(row=0, column=0, sticky="nsew")
        
        # Create scrollbar and attach to text widget
        text_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.results_text.yview)
        text_scroll.grid(row=0, column=1, sticky="ns")
        
        # Connect scrollbar to text widget
        self.results_text.config(yscrollcommand=text_scroll.set)
        
        # Configure text tags for formatting
        self.results_text.tag_configure("header", font=("Arial", 12, "bold"), justify="center")
        self.results_text.tag_configure("subheader", font=("Arial", 11, "bold"))
        self.results_text.tag_configure("normal", font=("Arial", 10))
        self.results_text.tag_configure("highlight", font=("Arial", 10, "bold"), foreground=self.colors["accent"])
        self.results_text.tag_configure("warning", foreground=self.colors["warning"])
        self.results_text.tag_configure("success", foreground=self.colors["success"])
        self.results_text.tag_configure("emphasis", font=("Arial", 10, "bold"), foreground="#8e44ad") # Purple
        
        # Insert header with formatting
        self.results_text.insert(tk.END, f"📊 RESUME ANALYSIS RESULTS FOR {self.analyzer.name.upper()} 📊\n_____________________________________________________\n", "header")
        
        # Insert match percentages with formatting
        self.results_text.insert(tk.END, "Career match percentages (normalized to 100%):\n", "subheader")
        for role, score in sorted(self.analyzer.normalized_job_matches.items(), key=lambda x: x[1], reverse=True):
            self.results_text.insert(tk.END, f"🔹 {role}: ", "normal")
            self.results_text.insert(tk.END, f"{score}%\n", "highlight")
            
        # Insert best match with formatting
        self.results_text.insert(tk.END, f"\n_________________________________________________________\n✨ BEST CAREER MATCH: ", "subheader")
        self.results_text.insert(tk.END, f"{self.analyzer.best_match} ", "emphasis")
        self.results_text.insert(tk.END, f"({self.analyzer.normalized_job_matches[self.analyzer.best_match]}%)", "highlight")
        self.results_text.insert(tk.END, " ✨\n\n", "subheader")
        
        # Insert feedback with appropriate formatting
        normalized_score = self.analyzer.normalized_job_matches[self.analyzer.best_match]
        if normalized_score < 40:
            self.results_text.insert(tk.END, "⚠️ Your resume has a relatively low match with this role.\n\n", "warning")
            self.results_text.insert(tk.END, "Suggestions to improve your match:\n", "subheader")
            self.results_text.insert(tk.END, "1. Add more keywords relevant to the job description\n", "normal")
            self.results_text.insert(tk.END, "2. Highlight projects and experiences related to the role\n", "normal")
            self.results_text.insert(tk.END, "3. Quantify your achievements with specific metrics\n", "normal")
            self.results_text.insert(tk.END, "4. Consider acquiring additional skills mentioned in the job description\n", "normal")
        elif normalized_score < 60:
            self.results_text.insert(tk.END, "👍 Your resume has a good match, but could be improved.\n\n", "warning")
            self.results_text.insert(tk.END, "Suggestions to strengthen your application:\n", "subheader")
            self.results_text.insert(tk.END, "1. Emphasize your most relevant experiences for this role\n", "normal")
            self.results_text.insert(tk.END, "2. Add more industry-specific terminology\n", "normal")
            self.results_text.insert(tk.END, "3. Tailor your resume objective/summary to this specific position\n", "normal")
        else:
            self.results_text.insert(tk.END, "🎉 Excellent match! Your resume is well-aligned with this role.\n\n", "success")
            self.results_text.insert(tk.END, "Next steps:\n", "subheader")
            self.results_text.insert(tk.END, "1. Prepare for interviews by researching the company\n", "normal")
            self.results_text.insert(tk.END, "2. Practice explaining how your experience relates to the role's requirements\n", "normal")
            self.results_text.insert(tk.END, "3. Consider preparing a portfolio of relevant work samples\n", "normal")
            
        # Add additional content to make scrollbar necessary
        self.results_text.insert(tk.END, "\n" + "_" * 50 + "\n\n", "normal")
        self.results_text.insert(tk.END, "ANALYSIS DETAILS:\n", "subheader")
        self.results_text.insert(tk.END, "We analyzed your resume against multiple job descriptions to find the best matches.\n\n", "normal")
        self.results_text.insert(tk.END, "The analysis considers:\n", "normal")
        self.results_text.insert(tk.END, "• Key skills and technologies mentioned\n", "normal")
        self.results_text.insert(tk.END, "• Experience level and qualifications\n", "normal")
        self.results_text.insert(tk.END, "• Education and certifications\n", "normal")
        self.results_text.insert(tk.END, "• Industry-specific terminology\n\n", "normal")
        
        # Ensure scrollbar is visible by adding enough content
        self.results_text.insert(tk.END, "TIPS FOR IMPROVING YOUR RESUME:\n", "subheader")
        self.results_text.insert(tk.END, "1. Use industry-specific keywords\n", "normal")
        self.results_text.insert(tk.END, "2. Quantify achievements when possible\n", "normal")
        self.results_text.insert(tk.END, "3. Tailor your resume for each application\n", "normal")
        self.results_text.insert(tk.END, "4. Highlight relevant projects and experiences\n", "normal")
        self.results_text.insert(tk.END, "5. Keep formatting clean and consistent\n", "normal")
        self.results_text.insert(tk.END, "6. Include a professional summary\n", "normal")
        self.results_text.insert(tk.END, "7. List technical skills separately\n", "normal")
        self.results_text.insert(tk.END, "8. Proofread carefully\n", "normal")
        
        # Right side for chart with a different background color - MODIFIED WITH SCROLLBARS
        chart_container = ttk.Frame(horizontal_frame, style="Chart.TFrame")
        chart_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Make chart container responsive
        chart_container.columnconfigure(0, weight=1)
        chart_container.rowconfigure(0, weight=1)
        
        # Create a canvas with scrollbars for the chart
        chart_canvas = tk.Canvas(chart_container, bg=self.colors["frame_bg"], highlightthickness=0)
        chart_canvas.grid(row=0, column=0, sticky="nsew")
        
        # Add vertical scrollbar
        chart_v_scroll = ttk.Scrollbar(chart_container, orient="vertical", command=chart_canvas.yview)
        chart_v_scroll.grid(row=0, column=1, sticky="ns")
        
        # Add horizontal scrollbar
        chart_h_scroll = ttk.Scrollbar(chart_container, orient="horizontal", command=chart_canvas.xview)
        chart_h_scroll.grid(row=1, column=0, sticky="ew")
        
        # Configure canvas scrolling
        chart_canvas.configure(xscrollcommand=chart_h_scroll.set, yscrollcommand=chart_v_scroll.set)
        
        # Create a frame inside the canvas to hold the chart
        chart_frame = ttk.Frame(chart_canvas, style="Chart.TFrame")
        
        # Create a window inside the canvas to display the frame
        chart_canvas_window = chart_canvas.create_window((0, 0), window=chart_frame, anchor="nw")
        
        # Create and display chart in the scrollable frame
        self.create_chart(chart_frame)
        
        # Make sure the chart frame resizes with the canvas
        def configure_chart_frame(event):
            # Update the scrollregion to encompass the inner frame
            chart_canvas.configure(scrollregion=chart_canvas.bbox("all"))
            
            # Update the size of the window to match the canvas width
            width = event.width
            chart_canvas.itemconfig(chart_canvas_window, width=width)
        
        # Make the chart frame responsive to canvas resizing
        chart_frame.bind("<Configure>", configure_chart_frame)
        chart_canvas.bind("<Configure>", lambda e: chart_canvas.itemconfig(chart_canvas_window, width=e.width))
        
        # Auto-save chart
        chart_path = self.auto_save_chart()
        if chart_path:
            self.results_text.insert(tk.END, f"\n📷 Chart saved as: {os.path.basename(chart_path)}\n", "normal")
            self.results_text.insert(tk.END, f"📁 Location: {self.charts_dir}\n", "normal")
        
    def create_chart(self, frame):
        """Create and display the pie chart in the provided frame"""
        # Get data
        roles = list(self.analyzer.normalized_job_matches.keys())
        scores = list(self.analyzer.normalized_job_matches.values())
    
        # Create figure with larger size to support scrolling
        fig = plt.figure(figsize=(7, 6), tight_layout=True)  # Increased size for better visibility with scrollbars
        ax = fig.add_subplot(111)
    
        # Use the same colors for the pie chart as requested
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
        # Create pie chart with improved styling
        wedges, texts, autotexts = ax.pie(
            scores, 
            labels=None,  # Remove labels from pie to avoid overlap
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            colors=colors,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1, 'antialiased': True},
            textprops={'fontsize': 9}  # Slightly larger for better visibility
        )
    
        # Customize text appearance
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        
        # Add title with proper formatting
        ax.set_title('Resume Match Analysis', 
                     fontsize=12,  # Slightly larger
                     fontweight='bold',
                     pad=10)
                 
        # Add legend outside the pie for better positioning
        plt.legend(wedges, roles, title="Career Roles", 
                  loc="center left", 
                  bbox_to_anchor=(1, 0.5),
                  fontsize=8,  # Slightly larger
                  title_fontsize=9)
    
        # Adjust subplot to give more room for the legend
        plt.subplots_adjust(right=0.65)
        
        # Set background color of the chart
        fig.patch.set_facecolor(self.colors["frame_bg"])
        ax.set_facecolor(self.colors["frame_bg"])
                 
        # Remove any existing canvas
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Create canvas with appropriate size
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
        # Store the figure for saving later
        self.chart_figure = fig
        
    def auto_save_chart(self):
        """Automatically save the chart when analysis is complete"""
        if not hasattr(self, 'chart_figure'):
            return None
            
        try:
            # Create a filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            name = self.analyzer.name.lower().replace(" ", "_")
            filename = f"{self.charts_dir}/resume_analysis_{name}_{timestamp}.png"
            
            # Save the chart
            self.chart_figure.savefig(filename, dpi=300, bbox_inches='tight')
            self.status_var.set(f"Analysis complete. Chart saved as {os.path.basename(filename)}")
            
            return filename
        except Exception as e:
            self.status_var.set(f"Error saving chart: {str(e)}")
            messagebox.showwarning("Warning", f"Could not auto-save chart: {str(e)}")
            return None
        
    def save_chart(self):
        """Save the chart as an image file (manual save)"""
        filetypes = (
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("All files", "*.*")
        )
        
        filename = filedialog.asksaveasfilename(
            title="Save Chart",
            defaultextension=".png",
            filetypes=filetypes,
            initialdir=self.charts_dir
        )
        
        if filename and hasattr(self, 'chart_figure'):
            try:
                self.chart_figure.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Chart saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save chart: {str(e)}")

# Create a main function to run the GUI
def main():
    # Check if resumes directory exists
    if not os.path.exists("resumes"):
        os.makedirs("resumes")
        messagebox.showinfo(
            "Information",
            "Created 'resumes' directory. Please add your resume files there."
        )
        
    # Create charts directory if it doesn't exist
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
        
    # Create and run the GUI
    root = tk.Tk()
    app = ResumeAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()