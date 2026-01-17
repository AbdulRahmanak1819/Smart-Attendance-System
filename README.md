# Smart Attendance System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![Dlib](https://img.shields.io/badge/Library-Dlib-red)
![Face Recognition](https://img.shields.io/badge/AI-Face%20Recognition-orange)

**Smart Attendance System** is a Python automation tool that identifies registered users via webcam and logs their attendance with timestamps directly into an Excel file, preventing duplicate entries for the same session.

---

## 🚀 Features

- **Real-time Face Recognition:** Identifies registered users via webcam.
- **Automated Logging:** Records the Name and Time of entry into a `.csv` file.
- **Smart Logic:** Prevents duplicate entries for the same person in the same session.

---

## 🛠️ Installation Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/AbdulRahmanak1819/Smart-Attendance-System.git](https://github.com/AbdulRahmanak1819/Smart-Attendance-System.git)
cd Smart-Attendance-System
```

### 2. Special Step: Installing Dlib
This project uses `dlib` for machine learning. Installing it via `pip install dlib` often fails if you don't have Visual Studio C++ compilers installed.

**The Easy Fix (Using a Wheel File):**
1. You need a pre-compiled `.whl` file that matches your Python version (e.g., `cp310` for Python 3.10).
2. Download the file (search for "dlib precompiled wheel python").
3. Place the file in this folder and install it manually:

```bash
# Example command (Replace with your actual filename)
pip install "dlib-19.22.99-cp310-cp310-win_amd64.whl"
```

### 3. Install Other Dependencies
Once dlib is installed, install the rest of the libraries:
```bash
pip install -r requirements.txt
```

---

## 📸 How to Use

### Step 1: Add Images
1. Create a folder named `images` in the project directory.
2. Add photos of the people you want to recognize.
3. **Naming:** The filename becomes the person's name (e.g., `Elon Musk.jpg` will display "Elon Musk").

### Step 2: Run the Code
```bash
python main.py
```

### Step 3: Attendance
1. The webcam window will open.
2. When a face is recognized, it logs the time in `Attendance.csv`.
3. Press **'q'** to close the program.

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | The main script for face recognition and logging. |
| `images/` | Folder containing reference photos for known faces. |
| `Attendance.csv` | The output file where attendance logs are saved. |
| `requirements.txt` | List of Python library dependencies. |

---

## 🔒 Privacy Note
The `images/` folder and `Attendance.csv` file are excluded from this repository for privacy reasons. You must add your own local images to test the system.
