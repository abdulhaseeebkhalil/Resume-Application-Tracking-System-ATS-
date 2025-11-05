# ATS Resume Expert

An intelligent Resume Analysis and Application Tracking System (ATS) powered by Google's Gemini AI. This application helps job seekers optimize their resumes and improve their chances of getting hired by analyzing their resume against job descriptions.

## Features

- **Resume Analysis**: Get detailed insights about your resume's strengths and weaknesses
- **Skills Improvement Suggestions**: Receive personalized recommendations for skill enhancement
- **ATS Match Percentage**: Calculate how well your resume matches the job description
- **Role Fit Assessment**: Evaluate your suitability for the position
- **Key Achievements Highlight**: Identify and emphasize your most significant accomplishments
- **Certification Recommendations**: Get suggestions for relevant certifications
- **Leadership Potential Assessment**: Evaluate your leadership qualities
- **Transferable Skills Analysis**: Identify skills that can be applied to the role
- **Resume Enhancement**: Get a professionally rewritten version of your resume
- **Cover Letter Generation**: Create a tailored cover letter for the position

## Prerequisites

- Python 3.7 or higher
- Google API Key for Gemini AI
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Resume-Application-Tracking-System-ATS-
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Upload your resume in PDF format

4. Enter the job description in the text area

5. Use the various analysis buttons to get insights about your resume

## Features in Detail

### Resume Analysis
Get a comprehensive evaluation of your resume against the job description, highlighting strengths and areas for improvement.

### Skills Improvement
Receive actionable advice on skills, certifications, and experiences to better align with job requirements.

### ATS Match Percentage
Get a percentage match of your resume with the job description, along with missing keywords and final thoughts.

### Role Fit Assessment
Detailed breakdown of how well your profile aligns with the role requirements, including a rating out of 10.

### Key Achievements
Extract and highlight your most significant accomplishments that align with the job role.

### Certification Recommendations
Get suggestions for industry-recognized certifications relevant to the position.

### Leadership Assessment
Evaluation of your leadership potential based on your experiences and achievements.

### Transferable Skills
Identification of versatile skills that can be effectively applied to the new role.

### Resume Enhancement
Get a professionally rewritten version of your resume highlighting your strengths.

### Cover Letter Generation
Create a tailored cover letter specifically designed for the job description.

## Technologies Used

- Streamlit: For the web interface
- Google Gemini AI: For intelligent analysis
- PDF2Image: For PDF processing
- Python: Backend programming language

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for providing the AI capabilities
- Streamlit for the web framework
- All contributors who have helped improve this project 