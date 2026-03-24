import RPi.GPIO as GPIO
import smtplib
import time
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_ADDRESS  = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASS = os.getenv("GMAIL_APP_PASS")
NOTIFY_EMAIL   = os.getenv("NOTIFY_EMAIL")

# ── CONFIG — edit these 4 lines ──────────────────
# GMAIL_ADDRESS  = "yourgmail@gmail.com"
# GMAIL_APP_PASS = "abcdefghijklmnop"   # 16-char app password, no spaces
# NOTIFY_EMAIL   = "whereyouwantalerts@gmail.com"
BUTTON_PIN     = 17
# ─────────────────────────────────────────────────

COOLDOWN_SECS  = 10

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

last_sent = 0

def send_email():
    msg = MIMEText("Your button was pressed on the Raspberry Pi.")
    msg["Subject"] = "Button Alert"
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

def on_press(channel):
    global last_sent
    now = time.time()
    if now - last_sent > COOLDOWN_SECS:
        last_sent = now
        print("Button pressed — sending email...")
        send_email()
    else:
        print("Button pressed — cooldown active, skipping.")

GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING,
                      callback=on_press,
                      bouncetime=300)

print("Ready. Waiting for button press. Ctrl+C to stop.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    print("Cleaned up. Goodbye.")