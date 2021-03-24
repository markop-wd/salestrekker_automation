"""
This is what will read the new account e-mail and extract username and password from it.

I used a st.receive@gmail.com that I made it has nothing important on except those accounts that are all in separate organizations that have no access to others orgs.
"""
import email
import imaplib
import re
from datetime import date


# TODO - To create a function that checks each X for the email
class Mailer:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def mail_get(ent: str) -> dict:

    user_email = "st.receive@gmail.com"
    user_password = "yalk8kut4HUH*psuw"
    server = "imap.gmail.com"

    mail = imaplib.IMAP4_SSL(server)
    mail.login(user_email, user_password)
    mail.select()

    all_ents = {
        'ynet': 'ynet',
        'vownet': 'vownet',
        'gem': 'gem',
        'gemnz': 'gem nz',
        'platform': 'platform connect',
        'nlgconnect': 'nlg connect',
        'app': 'salestrekker',
        'ioutsource': 'ioutsource',
        'chief': 'chief',
        'sfg': 'sfg connect',
        'dev': 'DEV'
    }

    # The below two variables create a date of the following format 02-Dec-2020
    current_month = date.today().strftime("%B")[:3]
    current_date = date.today().strftime("%d-" + current_month + "-%Y")

    try:
        status, id_list = mail.search(
            None,
            f'ALL UNSEEN SUBJECT "Your {all_ents[ent]} account" '
            f'FROM "no-reply@eml.salestrekker.com" '
            f'ON "{current_date}"')
    except KeyError:
        raise KeyError(f'No enterprise found for: {ent}')
    else:
        try:
            last_email_id = id_list[0].split()[-1]
        except IndexError:
            # No emails with the given parameters
            return_dict = {'email': None, 'password': None}
            return return_dict
        else:
            typ, data = mail.fetch(last_email_id, 'BODY[1]')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(
                        response_part[1].decode('utf-8'))

                    re_email = re.search('Account email:.+>(.+?)</.+\n',
                                         str(msg))
                    re_pass = re.search('Account password:.+>(.+?)</.+\n',
                                        str(msg))

                    re_pass = re_pass.group(1)
                    re_email = re_email.group(1)

                    return_dict = {"email": re_email, "password": re_pass}

                    if re_pass is not None:
                        return return_dict
                    else:
                        return_dict = {'email': None, 'password': None}
                        return return_dict


if __name__ == '__main__':
    print(mail_get('dev'))
