import streamlit as st
import numpy as np
import pickle  # model loading
from PIL import Image

# Function to predict crop and season using Naive Bayes model
def predict_crop_and_season(N, P, K, temperature, humidity, ph, rainfall):
    data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    prediction = RandomForest.predict(data)

    # Determine season based on all factors
    if (temperature > 30) and (humidity > 70) and (rainfall > 200) and (N > 100) and (P > 20) and (K > 30):
        season = 'Monsoon'
    elif (temperature > 25) and (humidity > 50) and (rainfall < 100) and (N < 50) and (P < 15) and (K < 25):
        season = 'Summer'
    elif (temperature < 20) and (humidity < 40) and (rainfall < 100) and (N < 80) and (P > 10) and (K > 20):
        season = 'Winter'
    else:
        season = 'Fall'  # Uncertain

    return prediction[0], season

def load_randomForest_model():
    # Load the RandomForest model
    with open('models/RandomForest.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

# Load the Naive Bayes model
RandomForest = load_randomForest_model()

# Dictionary mapping crops to recommended fertilizers
fertilizer_recommendations = {
    'rice': ['NPK 15-15-15', 'Urea', 'Potassium sulfate'],
    'maize': ['NPK 20-10-10', 'Urea', 'Ammonium nitrate'],
    'chickpea': ['NPK 10-20-10', 'Urea', 'Superphosphate'],
    'kidneybeans': ['NPK 10-10-10', 'Urea', 'DAP'],
    'pigeonpeas': ['NPK 15-15-15', 'Urea', 'Potassium sulfate'],
    'mothbeans': ['NPK 20-10-10', 'Urea', 'Ammonium nitrate'],
    'mungbean': ['NPK 10-20-10', 'Urea', 'Superphosphate'],
    'blackgram': ['NPK 10-10-10', 'Urea', 'DAP'],
    'lentil': ['NPK 15-15-15', 'Urea', 'Potassium sulfate'],
    'pomegranate': ['NPK 20-10-10', 'Urea', 'Ammonium nitrate'],
    'banana': ['NPK 10-20-10', 'Urea', 'Superphosphate'],
    'mango': ['NPK 10-10-10', 'Urea', 'DAP'],
    'grapes': ['NPK 15-15-15', 'Urea', 'Potassium sulfate'],
    'watermelon': ['NPK 20-10-10', 'Urea', 'Ammonium nitrate'],
    'muskmelon': ['NPK 10-20-10', 'Urea', 'Superphosphate'],
    'apple': ['NPK 10-10-10', 'Urea', 'DAP'],
    'orange': ['NPK 15-15-15', 'Urea', 'Potassium sulfate'],
    'papaya': ['NPK 20-10-10', 'Urea', 'Ammonium nitrate'],
    'coconut': ['NPK 10-20-10', 'Urea', 'Superphosphate'],
    'cotton': ['NPK 10-10-10', 'Urea', 'DAP'],
    'jute': ['NPK 15-15-15', 'Urea', 'Potassium sulfate'],
    'coffee': ['NPK 20-10-10', 'Urea', 'Ammonium nitrate']
}

# Function to display image based on the predicted crop
def display_crop_image(crop):
    # Define the directory where the images are stored
    image_dir = "Crop_Images/"
    # Define a dictionary mapping crop names to image file names
    crop_images = {
        'rice': 'rice.jpeg',
        'maize': 'maize.jpeg',
        'chickpea': 'chickpea.jpeg',
        'kidneybeans': 'kidneybeans.jpeg',
        'pigeonpeas': 'pigeonpeas.jpeg',
        'mothbeans': 'mothbeans.jpeg',
        'mungbean': 'mungbean.jpeg',
        'blackgram': 'blackgram.jpeg',
        'lentil': 'lentil.jpeg',
        'pomegranate': 'pomegranate.jpeg',
        'banana': 'banana.jpeg',
        'mango': 'mango.jpeg',
        'grapes': 'grapes.jpeg',
        'watermelon': 'watermelon.jpeg',
        'muskmelon': 'muskmelon.jpeg',
        'apple': 'apple.jpeg',
        'orange': 'orange.jpeg',
        'papaya': 'papaya.jpeg',
        'coconut': 'coconut.jpeg',
        'cotton': 'cotton.jpeg',
        'jute': 'jute.jpeg',
        'coffee': 'coffee.jpeg'
    }
    
    # Check if the predicted crop exists in the dictionary
    if crop.lower() in crop_images:
        image_path = image_dir + crop_images[crop.lower()]
        image = Image.open(image_path)
        st.image(image, caption='Predicted Crop: ' + crop, use_column_width=True)
    else:
        st.warning("No image available for the predicted crop.")

def main():
    # Specific threshold values for temperature, humidity, rainfall, N, P, and K
    N = st.slider("Ratio of Nitrogen content in soil (kg/ha)", min_value=0, max_value=200, step=1)
    P = st.slider("Ratio of Phosphorous content in soil (kg/ha)", min_value=0, max_value=200, step=1)
    K = st.slider("Ratio of Potassium content in soil (kg/ha)", min_value=0, max_value=200, step=1)
    temperature = st.slider("Temperature (°C)", min_value=0, max_value=40, step=1)
    humidity = st.slider("Relative Humidity (%)", min_value=0, max_value=100, step=1)
    ph = st.slider("Soil pH", min_value=0, max_value=14, step=1)  # Adjusted step to 1
    rainfall = st.slider("Rainfall (mm)", min_value=0, max_value=500, step=1)

    # Make a prediction using Naive Bayes model
    if st.button("Predict"):
        crop, season = predict_crop_and_season(N, P, K, temperature, humidity, ph, rainfall)
        st.success(f"The predicted crop is: {crop}")
        if season:
            st.info(f"Suggested season for planting: {season}")
        else:
            st.warning("Conditions do not match any specific season.")

        # Display recommended fertilizers based on predicted crop
        if crop.lower() in fertilizer_recommendations:
            st.subheader("Recommended Fertilizers:")
            for fertilizer in fertilizer_recommendations[crop.lower()]:
                st.write(f"- {fertilizer}")
        else:
            st.warning("No fertilizer recommendations available for the predicted crop.")
        
        # Display the image of the predicted crop
        display_crop_image(crop)

# Login system
def login():
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    st.title("PrecisionPlantAI: Crop Prediction")
    st.image("crops.jpg")
    if username == "admin" and password == "admin":
        st.sidebar.success("Logged in as admin")
        main()
    else:
        st.sidebar.error("Invalid credentials")



if __name__ == "__main__":
    login()
    
