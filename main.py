import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values
import random
import smtplib
import lxml

config = {
    **dotenv_values('.env')
}


def get_ua():
    ua_strings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 "
        "Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 "
        "Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 "
        "Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
    ]

    return random.choice(ua_strings)


headers = {
    "User-Agent": get_ua(),
    "Accept-Language": "en,en-US;q=0.9,bn;q=0.8"
}

data = requests.get(
    url="https://www.amazon.com/beyerdynamic-770-PRO-Studio-Headphone/dp/B0016MNAAI/ref=sr_1_6?keywords=Beyerdynamic%2Bdt%2B770%2Bpro&qid=1691130533&sr=8-6&th=1",
    headers=headers).text

soup = BeautifulSoup(data, "lxml")

# extracting data
p_title = soup.select_one("#productTitle").get_text().rstrip()[0:31]
price = soup.select_one("span.a-offscreen")
price_without_currency = price.get_text().split("$")[1]
price_in_float = float(price_without_currency)


def send_mail():
    # authenticating with smtp
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(config['my_email'], config['my_pass'])
        connection.sendmail(from_addr=config['my_email'], to_addrs=config['receiver_email'],
                            msg=f"Subject:{p_title} Price Alert!\n\n This product price is now {price_without_currency}"
                                f",below your target price.Buy Now!")


# if price lower than the target price send mail
if price_in_float < 150.00:
    send_mail()
