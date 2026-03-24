import RPi.GPIO as GPIO
import smtplib
import time
from email.mime.text import MIMEText

GMAIL_ADDRESS  = "yourgmail@gmail.com"
GMAIL_APP_PASS = "yoursixteencharacterpassword"
NOTIFY_EMAIL   = "whereyouwantalerts@gmail.com"
BUTTON_PIN     = 17
COOLDOWN_SECS  = 10

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
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