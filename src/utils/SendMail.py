import yaml
# Packages required for send mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def readYamlForCredentails():
    """
    Reading the Yaml file for the credantails
    :return: userid and password
    """
    # Configure db
    db = yaml.load(open('../db.yaml'))
    user_id = db['email']["sender_id"]
    password = db['email']["password"]

    # Returning the information
    return user_id, password


def sendMail(receiver_address):
    """
    This function is used for sending mail to the particular email address
    :param receiver_address: receiver mail address
    :return: true when mail send successfully and false when it has error
    """
    try:
        # Creating the link for gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)

        # Enabling the E SMTP server
        server.ehlo()

        # Starting the TLS mode
        server.starttls()

        # Reading the data form the yaml configuration
        sender_address, password = readYamlForCredentails()

        # Next, log in to the server
        server.login(sender_address, password)

        # Send the mail with subject
        # you == the recipient's email address
        msg = MIMEMultipart()
        msg['Subject'] = 'The contents of Rajanikant'
        msg['From'] = sender_address
        msg['To'] = receiver_address
        message = "Hello RK"

        # Adding the message in MIME
        part_message = MIMEText(message, 'plain')
        msg.attach(part_message)

        # Sending the mail
        server.sendmail(sender_address, receiver_address, msg.as_string())

        # Returning the success messages
        return True, "meaage send successfully"

    except Exception as e:
        # Sending the error messages
        return False, "Error while sending mail"

    finally:
        # Closing the server connection
        server.close()


if __name__ == '__main__':
    status, message = sendMail("rajanikant.prodevans@gmail.com")
    if status:
        print("Success")
    else:
        print("Error", message)
