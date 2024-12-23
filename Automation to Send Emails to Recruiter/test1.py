import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders

# Email configuration
sender_email = "faheemshaikh1210@gmail.com"
app_password = "zslpfnifzehciika"
subject = "Application for DevOps Engineer"
resume_filename = "Faheem Shaikh.pdf"  # Name of the resume PDF file

# Read CSV file
def read_emails_from_csv(filename):
    emails = []
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            emails.append(row['email'])  # Assuming CSV has an 'email' column
    return emails

# Send email function
def send_email(recipient_email):
    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = "faheemshaikh1210@gmail.com"
    msg['To'] = recipient_email
    msg['Subject'] = "Application For DevOps Engineer"

    # Customize the email body
    body = f""" 
    \nHello,
    \nI hope this email finds you well. 
    \nMy name is Faheem Shaikh, and I am writing to express my interest in the DevOps Engineer position. 
    \nWith over 2 years of experience in DevOps engineering, I have developed a strong background in continuous integration and continuous deployment (CI/CD), automation, and cloud infrastructure management. 
    \nPlease find my resume attached for your review. I am confident that my skills and experiences make me a suitable candidate for this role. 
    \nI would be thrilled to further discuss how I can contribute to your team.

    \nThank you for considering my application. 
    
    \nBest regards, 
    \nFaheem Shaikh 
    \n+91 7020669045
    """
    msg.attach(MIMEText(body, 'plain'))

    # Attach the resume PDF
    with open(resume_filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {resume_filename}')

        msg.attach(part)



    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)

# Main function
def main():
    emails = read_emails_from_csv('email_list.csv')
    count = 0  # Counter for successful email sends
    for email in emails:
        try:
            send_email(email)
            count += 1
            print(f"Email sent to {email}")
        except Exception as e:
            print(f"Failed to send email to {email}. Error: {str(e)}")
    print(f"Total number of emails sent successfully: {count}")

if __name__ == "__main__":
    main()
