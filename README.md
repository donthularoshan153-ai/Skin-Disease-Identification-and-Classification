# Skin Disease Prediction System

## Overview

This project is a **Skin Disease Prediction Web Application** built using **Django** and **Deep Learning**. It allows users to upload an image of a skin condition and predicts the disease using a trained EfficientNet model.

The web interface is developed in **VS Code**, and the **Machine Learning model was trained in Google Colab** due to high GPU and RAM requirements.

Because the trained model files are very large, the **model training notebook is provided instead of uploading the full model to GitHub**.

---

## Features

• Upload skin image
• Predict skin disease using Deep Learning
• Display prediction result on web page
• Simple and user-friendly interface

---

## Technologies Used

• Python
• Django
• TensorFlow / Keras
• EfficientNet
• HTML, CSS, JavaScript
• Google Colab (for model training)

---

## Important Note About Model File

The trained model file is very large and may not upload to GitHub due to size limits.

So instead:

• The **Google Colab notebook is provided**
• You must run the notebook to generate the model file

After training, download the model and place it inside:

```
prediction/
```

Example:

```
prediction/skin_disease_model.h5
```

OR

```
efficientnet_skin_model_final.keras
```

---

## Project Structure

```
skin disease prediction/
│
├── manage.py
├── db.sqlite3
├── skindisease/        → Main Django Project
├── prediction/         → Django App
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── static/
│   ├── skin_disease_model.h5
│
├── media/
```

---

## Requirements

Install these first:

Python 3.10 or above

Then install dependencies:

```
pip install django
pip install tensorflow
pip install pillow
pip install numpy
```

---

## How to Run This Project

### Step 1: Clone Repository

```
git clone https://github.com/yourusername/yourrepositoryname.git
```

### Step 2: Go into folder

```
cd "skin disease prediction"
```

### Step 3: Run Server

```
python manage.py runserver
```

---

### Step 4: Open Browser

Go to:

```
http://127.0.0.1:8000/
```

---

## How to Use

1. Open website
2. Upload skin image
3. Click Predict
4. View Result

---

## How Model Was Created

The model was trained using:

Google Colab

Reason:

• Large dataset
• GPU required
• Faster training

You can open the Colab notebook and run all cells to recreate the model.

---

## Future Improvements

• Deploy on cloud
• Improve accuracy
• Add more diseases
• Add user login system

---

## Author

Developed by: Donthula Roshan

---
