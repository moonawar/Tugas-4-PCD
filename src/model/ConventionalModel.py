import cv2
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import joblib


# Fungsi untuk ekstraksi fitur HOG
def extract_hog_features(image):
    # Parameter HOG
    winSize = (64,64)
    blockSize = (16,16)
    blockStride = (8,8)
    cellSize = (8,8)
    nbins = 9
    derivAperture = 1
    winSigma = -1.
    histogramNormType = 0
    L2HysThreshold = 0.2
    gammaCorrection = 1
    nlevels = 64
    signedGradient = True

    # Ekstraksi fitur HOG
    hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,histogramNormType,L2HysThreshold,gammaCorrection,nlevels, signedGradient)
    features = hog.compute(image)

    return features.flatten()


# Fungsi untuk memuat dan mengekstrak fitur hog citra dari semua subfolder dalam direktori dataset
def load_and_extract_images(directory):
    images = []
    labels = []
    
    # Iterasi setiap subfolder (kelas) di dalam folder dataset
    for class_label in os.listdir(directory):
        class_folder = os.path.join(directory, class_label)
        if os.path.isdir(class_folder):
            for filename in os.listdir(class_folder):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    img_path = os.path.join(class_folder, filename)
                    img = cv2.imread(img_path)

                    # Pre-processing citra
                    img = cv2.resize(img, (64, 64)) # Resize ke ukuran tetap
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Konversi ke grayscale

                    # Ekstraksi fitur HOG
                    features = extract_hog_features(img)
                    images.append(features)
                    labels.append(class_label)
    
    return images, labels


# Fungsi untuk melatih model SVM dan menyimpannya ke file .joblib
def train_model(model_name='conventional_model.joblib'):
    directory = f"../model/{model_name}"
    dataset_directory = '../dataset'
    images, labels = load_and_extract_images(dataset_directory)

    # Mengonversi data ke format numpy array untuk digunakan oleh SVM
    X = np.array(images)
    y = np.array(labels)

    # Membagi dataset menjadi data latih dan data uji (80% latih, 20% uji)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Membuat dan melatih model SVM dengan kernel RBF
    svm_model = svm.SVC(kernel='rbf', C=1.0)
    svm_model.fit(X_train, y_train)

    # Evaluasi model menggunakan data uji
    y_pred = svm_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Akurasi model: {accuracy * 100:.2f}%")

    # Menyimpan model yang telah dilatih ke directory dengan ekstensi .joblib
    joblib.dump(svm_model, directory)

    print(f"Model SVM telah dilatih dan disimpan sebagai '{model_name}' di folder 'model'")


# Fungsi untuk mengklasifikasikan citra menggunakan model SVM yang telah dilatih
def classify_image(image_path, model_path):
    # Memuat model SVM yang telah dilatih
    svm_model = joblib.load(model_path)
    
    # Memuat dan memproses citra input
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found at {image_path}")
    
    img = cv2.resize(img, (64, 64))  # Resize ke ukuran tetap
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Konversi ke grayscale
    
    # Ekstraksi fitur HOG dari citra input
    features = extract_hog_features(img).reshape(1, -1)
    
    # Prediksi kelas menggunakan model SVM
    prediction = svm_model.predict(features)
    
    return prediction[0].capitalize()