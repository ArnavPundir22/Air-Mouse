
# 🖱️ Virtual Mouse using Computer Vision

This project implements a **Virtual Mouse** system that allows users to control their computer mouse using only hand gestures captured via webcam. It utilizes **computer vision techniques** with the help of **OpenCV** and **MediaPipe** for real-time hand tracking and gesture recognition.

## 💡 Features

- Move mouse pointer using index finger.
- Left click by bringing thumb and index finger close.
- Right click by bringing thumb and middle finger close.
- Scroll control using finger distance.
- Real-time hand tracking with webcam.
- Smooth cursor movement using interpolation.

## 🛠️ Technologies Used

- **Python 3.x**
- **OpenCV** – for video processing.
- **MediaPipe** – for hand tracking and gesture detection.
- **PyAutoGUI** – for controlling the mouse programmatically.
- **NumPy** – for array operations and calculations.

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/virtual-mouse.git
   cd virtual-mouse
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the project**
   ```bash
   python virtual_mouse.py
   ```

## 🧠 How It Works

1. Captures real-time video stream from webcam.
2. Uses MediaPipe to detect hand landmarks.
3. Identifies specific fingers and gestures.
4. Maps hand coordinates to screen resolution using interpolation.
5. Executes mouse movements and actions based on gestures.


## 🧩 Requirements

- Webcam
- Python 3.6+
- A steady hand 😄

## ✍️ Author

**Arnav Pundir**  
[GitHub](https://github.com/ArnavPundir22) • [LinkedIn](https://www.linkedin.com/in/arnav-pundir12)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
