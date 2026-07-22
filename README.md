##ASL Recognition System

A Deep Learning based American Sign Language (ASL) Recognition System that classifies hand gesture images into ASL alphabet letters (A-Z) using a 4-layer Neural Network. The project is developed using Python and deployed as an interactive web application with Streamlit.

#Project Overview

Communication barriers can make it difficult for deaf and hard-of-hearing individuals to interact with others. This project aims to provide an AI-based solution that recognizes American Sign Language alphabet gestures from images and converts them into readable alphabet predictions.

The system uses a trained deep learning model to analyze hand gesture images and predict the corresponding ASL alphabet character.

#Features
Recognition of ASL alphabets from A-Z
Deep Learning based image classification
4-layer Neural Network architecture
Real-time prediction through Streamlit web application
Image upload functionality
Fast and user-friendly interface
Prediction of hand gesture classes
#Technologies Used
Python
Streamlit
TensorFlow / Keras
NumPy
OpenCV
PIL (Python Imaging Library)
Neural Networks
Computer Vision
#Model Details
Model Type: Artificial Neural Network
Architecture: 4-Layer Neural Network
Task: Multi-class Image Classification
Classes: 26 ASL Alphabet Letters (A-Z)
Input: Hand gesture images
Output: Predicted ASL alphabet character
#Project Structure
ASL_Project_by_Abu_Sufyan/

│
├── app.py                  # Streamlit application
├── classes.json            # Class labels mapping
├── requirements.txt        # Required Python libraries
├── image.png               # Project image/sample image
│
├── ASL_weight files        # Trained model weights
│
├── README.md               # Project documentation
└── LICENSE                 # MIT License
#Installation and Setup
