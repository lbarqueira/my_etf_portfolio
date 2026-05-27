import smtplib
import glob
import os
import sys
from email.message import EmailMessage

EMAIL    = "luis.barqueira@gmail.com"
PASSWORD = os.environ.get("GMAIL_PASSWORD")

# The notebook creates a directory named etf_portfolio_<PERIOD>_<timestamp>/
# and puts the PDF inside it with the same name. We find the most recent one.
pattern = "etf_portfolio_*/*.pdf"
matches = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)

if not matches:
    print("ERROR: No report PDF found matching pattern:", pattern)
    sys.exit(1)

pdf_path     = matches[0]
pdf_filename = os.path.basename(pdf_path)

# Extract PERIOD from folder name, e.g. "etf_portfolio_YTD_2026-05-17_07h00m"
folder_name  = os.path.basename(os.path.dirname(pdf_path))
period       = folder_name.split("_")[2]   # e.g. "YTD", "1M", "1Y"

print(f"Attaching: {pdf_path}")

msg = EmailMessage()
msg["Subject"] = f"ETF Portfolio Report — {period} — {folder_name.split('_', 3)[3].replace('_', ' at ')}"
msg["From"]    = EMAIL
msg["To"]      = EMAIL
msg.set_content(
    f"Hi Luis,\n\n"
    f"Please find attached your latest ETF portfolio report ({period}).\n\n"
    f"Report: {pdf_filename}\n\n"
    f"This report was generated automatically.\n"
)

with open(pdf_path, "rb") as f:
    msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=pdf_filename)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL, PASSWORD)
    smtp.send_message(msg)

print("Email sent successfully.")
