import cv2
import winsound  # For beep sound (Windows only)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials (replace these with your credentials)
sender_email = "surbhigoswami13062007@gmail.com"
sender_password = "vtvl decn uxyw omul"
receiver_email = "yadavapkesha@gmail.com"

# Load pre-trained face detection model (Haar Cascade)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to send email alert
def send_email_alert():
    msg = MIMEText("Alert! A person has been detected in the camera feed.")
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Human Intrusion Alert"

    # Set up the server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email alert sent.")

# Function to detect faces in the frame
def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        print("Face(s) detected!")
        return faces
    return []

# Start video capture from webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Define the codec and create a VideoWriter object to save video
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # You can also use 'MJPG', 'MP4V', etc.
out = cv2.VideoWriter('output_video.avi', fourcc, 20.0, (640, 480))  # Save as output_video.avi

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect faces in the frame
    faces = detect_faces(frame)
    if len(faces) > 0:
        winsound.Beep(1000, 600)  # Beep when a face is detected
        send_email_alert()        # Send email alert

        # Draw rectangle around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Write the frame to the video file
    out.write(frame)

    # Show the video feed with detected faces
    cv2.imshow('Video Feed', frame)
    cv2.imwrite('frame.jpg', frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture, writer, and close windows
cap.release()
out.release()
cv2.destroyAllWindows()