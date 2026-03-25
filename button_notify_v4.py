from gpiozero import Button, LED
from signal import pause
import smtplib
import time
import threading
from email.mime.text import MIMEText

GMAIL_ADDRESS  = "yourgmail@gmail.com"
GMAIL_APP_PASS = "yoursixteencharpass"
NOTIFY_EMAIL   = "yournotifyemail@gmail.com"
COOLDOWN_SECS  = 10
LED_PIN        = 27
BUTTON_PIN     = 17
LED_ON_SECS    = 10

last_sent = 0
button = Button(BUTTON_PIN, pull_up=False)
led    = LED(LED_PIN)

def flash_led():
    led.on()
    time.sleep(LED_ON_SECS)
    led.off()

def send_email():
    msg = MIMEText("Gram pressed the button. This is an automation powered by RaspberryPi.")
    msg["Subject"] = "Gram took her meds!"
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = NOTIFY_EMAIL
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as s:
            s.starttls()
            s.login(GMAIL_ADDRESS, GMAIL_APP_PASS)
            s.sendmail(GMAIL_ADDRESS, NOTIFY_EMAIL, msg.as_string())
        print("Email sent!")
    except Exception as e:
        print(f"Email failed: {e}")

def on_press():
    global last_sent
    now = time.time()
    if now - last_sent > COOLDOWN_SECS:
        last_sent = now
        print("Button pressed - sending email...")
        threading.Thread(target=flash_led, daemon=True).start()
        send_email()
    else:
        print("Button pressed - cooldown active, skipping.")

button.when_pressed = on_press

print("Ready. Waiting for button press. Ctrl+C to stop.")
pause()