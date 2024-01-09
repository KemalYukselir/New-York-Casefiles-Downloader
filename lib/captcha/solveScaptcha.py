import requests
import time

def get_captcha():
    # Constants 
    apiKey = "14f2421ec16f202efe36bdf5a47ab6c8"
    reCaptchaSiteKey = "6LdiezYUAAAAAGJqdPJPP7mAUgQUEJxyLJRUlvN6"
    siteLink = "https://iapps.courts.state.ny.us/webcivil/captcha"


    ''' Gets a ReCaptcha Token from 2captcha API '''

    captchaToken = ''
    captchaRequestURL = 'https://2captcha.com/in.php?key=%s' \
        '&method=userrecaptcha&googlekey=%s' \
        '&pageurl=%s' % (str(apiKey), str(reCaptchaSiteKey), siteLink)

    try:
        s = requests.session()
        resp = s.get(captchaRequestURL)
        id = resp.text.split('|')[1]

        captchaResponseURL = 'https://2captcha.com/res.php?key=%s&action=get&id=%s' % (str(apiKey), str(id))
        resp = s.get(captchaResponseURL)

        while resp.text == 'CAPCHA_NOT_READY':
            time.sleep(5)  # wait 5 secs accord to requirements from 2capcha
            resp = s.get(captchaResponseURL)

        if resp.text == 'ERROR_CAPTCHA_UNSOLVABLE': #in this case this attempt will not be charged
            get_captcha()
            return #Delete this line if people are experiencing issues

        try:
            captchaToken = resp.text.split('|')[1]  #actual value
            return captchaToken
        except:
            return ""

    except Exception:
        return ""
