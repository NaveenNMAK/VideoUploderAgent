import os
import sys
import time
import json
import threading
import tempfile
import smtplib
from datetime import date
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from email.mime.text import MIMEText

# ----------------------------------
# 🚀 CONFIGURATION (leave as‑is unless your paths / defaults change)
EXPORT_FOLDER = r"*"
GOOGLE_DRIVE_FOLDER_ID = "*"
SENDER_EMAIL = "*"
SENDER_PASSWORD = "*"
# Default, static recipient:
DEFAULT_RECIPIENT = "*"
# ----------------------------------

# ── Embed your Web‑app OAuth2 client credentials here:
CREDENTIALS_DICT = {
    "web": {
        "client_id": "*",
        "project_id": "*",
        "auth_uri": "*",
        "token_uri": "*",
        "auth_provider_x509_cert_url": "*",
        "client_secret": "*",
        "redirect_uris": ["*"]
    }
}

cancel_flag = False
root = None

def get_drive_with_embedded_credentials(update_status):
    try:
        update_status("🔐 Preparing Drive authentication...")
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".json") as tf:
            json.dump(CREDENTIALS_DICT, tf)
            temp_path = tf.name

        gauth = GoogleAuth()
        gauth.LoadClientConfigFile(temp_path)
        update_status("🌐 Opening browser for Google login...")
        gauth.LocalWebserverAuth()              # uses http://localhost:8080/
        drive = GoogleDrive(gauth)
        os.remove(temp_path)
        update_status("🔑 Drive authentication successful.")
        return drive
    except Exception as e:
        update_status(f"❌ Drive auth error: {e}")
        return None

def wait_for_export_gui(export_path, filename, update_status):
    global cancel_flag
    fp = os.path.join(export_path, filename)
    last_size = -1
    stable_count = 0

    update_status(f"📁 Monitoring for '{filename}'…")
    while not cancel_flag:
        if os.path.exists(fp):
            size = os.path.getsize(fp)
            update_status(f"⏳ Export in progress: {size//(1024*1024)} MB")
            if size == last_size:
                stable_count += 1
            else:
                stable_count = 0
            last_size = size
            if stable_count >= 3:            # ~30 s stable = done
                update_status("✅ Export finalized.")
                return fp
        else:
            update_status("⌛ Waiting for file to appear…")
        time.sleep(10)

    update_status("❌ Export monitoring cancelled.")
    return None

def upload_to_drive_gui(filepath, folder_id, update_status):
    drive = get_drive_with_embedded_credentials(update_status)
    if not drive:
        return None
    try:
        update_status("📤 Uploading to Drive…")
        f = drive.CreateFile({
            'title': os.path.basename(filepath),
            'parents': [{'id': folder_id}]
        })
        f.SetContentFile(filepath)
        f.Upload()
        f.InsertPermission({'type':'anyone','value':'anyone','role':'reader'})
        link = f['alternateLink']
        update_status("✅ Upload complete.")
        return link
    except Exception as e:
        update_status(f"❌ Drive upload error: {e}")
        return None

def send_email_gui(recipient, link, update_status):
    try:
        today = date.today().isoformat()
        subject = f"Edited video with {today}"
        body = f"Hi,\n\nYour edited video is ready.\n🔗 {link}\n\nBest regards,"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient

        update_status(f"📨 Sending email to {recipient}…")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as srv:
            srv.login(SENDER_EMAIL, SENDER_PASSWORD)
            srv.send_message(msg)
        update_status(f"✅ Email sent to {recipient}.")
    except Exception as e:
        update_status(f"❌ Email error for {recipient}: {e}")

def start_process(filename, dynamic_email, update_status):
    global cancel_flag, root
    cancel_flag = False

    # 1) Monitor export
    path = wait_for_export_gui(EXPORT_FOLDER, filename, update_status)
    if not path: return

    # 2) Upload and get link
    link = upload_to_drive_gui(path, GOOGLE_DRIVE_FOLDER_ID, update_status)
    if not link: return

    # 3) Send to dynamic + default recipients
    send_email_gui(dynamic_email, link, update_status)
    send_email_gui(DEFAULT_RECIPIENT, link, update_status)

    update_status("🎉 All tasks completed successfully!")
    messagebox.showinfo("Done", "All tasks completed successfully!")
    root.after(1000, root.destroy)

def build_gui():
    global root
    root = Tk()
    root.title("🎬 Export & Upload Tool")
    root.geometry("600x380")

    Label(root, text="Enter Exported Video Filename:").pack(pady=6)
    file_var = StringVar()
    Entry(root, textvariable=file_var, width=50).pack()

    Label(root, text="Enter Recipient Email:").pack(pady=6)
    email_var = StringVar()
    Entry(root, textvariable=email_var, width=50).pack()

    status_var = StringVar(value="Awaiting input…")
    Label(root, textvariable=status_var, wraplength=550, fg="blue").pack(pady=20)

    def on_start():
        fn = file_var.get().strip()
        em = email_var.get().strip()
        if not fn or not em:
            messagebox.showwarning("Missing input", "Please enter both filename and recipient email.")
            return
        threading.Thread(target=start_process, args=(fn, em, status_var.set), daemon=True).start()

    def on_cancel():
        global cancel_flag
        cancel_flag = True
        status_var.set("⚠ Cancellation requested…")

    Button(root, text="Start", command=on_start, bg="green", fg="white").pack(pady=4)
    Button(root, text="Cancel", command=on_cancel, bg="red", fg="white").pack(pady=4)

    root.mainloop()

if __name__ == "__main__":
    build_gui()