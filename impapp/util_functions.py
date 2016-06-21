__author__ = 'Abdul'
from django.core.validators import validate_email as v_email, URLValidator
from django.core.exceptions import ValidationError
from impapp.app.models import Emailtemplates
import traceback
from django.core.mail import EmailMultiAlternatives
import string
import random


def check_email(email):
    try:
        v_email(email)
        return True
    except:
        return False


def validate_age(age):
    try:
        age = int(age)
        return 18 <= age < 100
    except Exception:
        return False

def validate_url(url):
    try:
        validate = URLValidator()
        validate(url)
        return True
    except ValidationError:
        return False


def validate_float(num):
    try:
        num = float(num)
        return 0 < num <= 5
    except Exception:
        return False



def send_email_extended(title, to_list=[], cc_list=[], bcc_list=[], email_words_dict={}, request='', attachment=''):
    try:
        template_obj = Emailtemplates.objects.get(title=title)
        if template_obj.is_active:
            if not to_list:
                to_list = str(template_obj.to_list).split(',')
            if not cc_list:
                cc_list = str(template_obj.cc_list).split(',')
            if not bcc_list:
                bcc_list = str(template_obj.bcc_list).split(',')

            body = str(template_obj.description)

            from_email = extractTLDfromHost(str(template_obj.from_email), '[DOMAIN]', 'email_sender',  request)

            subject = template_obj.subject

            subject = evariableReplace(subject, email_words_dict)
            email_text = evariableReplace(body, email_words_dict)
            # from_email = 'support@dincloud.com'
            msg = EmailMultiAlternatives(subject, email_text, from_email, to=to_list,cc=cc_list, bcc=bcc_list)
            if attachment:
                msg.attach(attachment['title'], attachment['file'] , attachment['type'])
            msg.content_subtype = "html"
            msg.send()

        if email_words_dict:
            template_obj.placeholders = '\n'.join([k for k in email_words_dict.keys()])
            template_obj.save()

    except Exception,ex:
        print traceback.print_exc(5)
        print str(ex)


# support@lesprovocatrices.com
def extractTLDfromHost(body_txt, find_val, act, request):
    if request:
        import tldextract
        ext = tldextract.extract(request.session["HOSTNAME"])
        if ext.tld:
            if act == "email_sender":
                parentdomain_url = '.'.join(ext[1:3])   # parentdomainurl.tld
                body_txt = body_txt.replace(find_val, parentdomain_url)
        else:
            body_txt = body_txt.replace(find_val, "lesprovocatrices.com")
    else:
        body_txt = body_txt.replace(find_val, "lesprovocatrices.com")

    return body_txt



def evariableReplace(txt, varDic):
    for k, v in varDic.iteritems():
        txt = txt.replace(k, v)
    return txt


def generate_password(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))