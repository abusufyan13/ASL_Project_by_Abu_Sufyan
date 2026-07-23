ASL Recognition System

A Deep Learning based American Sign Language (ASL) Recognition System that classifies hand gesture images into ASL alphabet letters (A-Z) using a 4-layer Neural Network. The project is developed using Python and deployed as an interactive web application with Streamlit.

Project Overview

Communication barriers can make it difficult for deaf and hard-of-hearing individuals to interact with others. This project aims to provide an AI-based solution that recognizes American Sign Language alphabet gestures from images and converts them into readable alphabet predictions.

The system uses a trained deep learning model to analyze hand gesture images and predict the corresponding ASL alphabet character.

Features
Recognition of ASL alphabets from A-Z
Deep Learning based image classification
4-layer Neural Network architecture
Real-time prediction through Streamlit web application
Image upload functionality
Fast and user-friendly interface
Prediction of hand gesture classes
Technologies Used
Python
Streamlit
TensorFlow / Keras
NumPy
OpenCV
PIL (Python Imaging Library)
Neural Networks
Computer Vision
Model Details
Model Type: Artificial Neural Network
Architecture: 4-Layer Neural Network
Task: Multi-class Image Classification
Classes: 26 ASL Alphabet Letters (A-Z)
Input: Hand gesture images
Output: Predicted ASL alphabet character
Project Structure
ASL_Project_by_Abu_Sufyan/
1. Clone the Repository
git clone https://github.com/abusufyan13/ASL_Project_by_Abu_Sufyan.git
2. Navigate to Project Folder
cd ASL_Project_by_Abu_Sufyan
3. Install Required Libraries
pip install -r requirements.txt
4. Run the Streamlit Application
streamlit run app.py

The application will open in your browser.

How to Use
Open the ASL Recognition web application.
Upload an image containing an ASL hand gesture.
The deep learning model processes the image.
The system predicts the corresponding alphabet letter.
Deployment

The application can be deployed using:

Streamlit Cloud
GitHub Repository Integration

After deployment, the application can be accessed through a public URL and shared with users.

Future Improvements
Add real-time webcam gesture recognition
Improve accuracy using CNN architectures
Support complete ASL word and sentence recognition
Add mobile application support
Expand dataset for better generalization
Applications
Educational tools for learning ASL
Communication assistance systems
Accessibility-focused AI applications
Human-computer interaction systems
Author

Abu Sufyan

Computer Science Student
Deep Learning | Machine Learning | Artificial Intelligence

License

This project is licensed under the MIT License. You are free to use, modify, and distribute this project with proper attribution.

