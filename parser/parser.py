from bs4 import BeautifulSoup
import requests


def url_is_correct(url: str) -> bool:
    print(f"Проверка ссылки: {url}  ...")
    request = requests.get(url)
    if request.status_code == 200:
        print(f"Успешная ссылка: {url}!")
        return True
    print(f"Невозможно получить данные по адресу: {url}\nПроверьте правильность url!")
    return False


def get_html(url: str) -> BeautifulSoup:
    if url_is_correct(url=url):
        print(f"Получаю данные с ссылки: {url}")
        request = requests.get(url)
        html = BeautifulSoup(request.text, "html.parser")
        return html
    

def get_links(html: BeautifulSoup) -> str:
    listing = html.find("div", {"class": "listings-wrapper"})
    publications: list[BeautifulSoup] = listing.find_all("div", {"class": "listing"})

    for post in publications:
        domen = "https://www.house.kg"
        path = post.find("p", {"class": "title"}).find("a").get("href")
        url = f"{domen}{path}"
        yield url


def parse_data(html: BeautifulSoup) -> dict:
    header: BeautifulSoup = html.find("div", {"class": "main-content"}).find("div", {"class":"details-header"})

    title = header.find("h1").text.strip()
    address = header.find("div", {"class": "address"}).text.strip()
    dollar = header.find("div", {"class": "price-dollar"}).text.strip()
    som = header.find("div", {"class": "price-som"}).text.strip()

    phone = html.find("div", {"class": "phone-fixable-block"}).find("div", {"class":"number"}).text.strip()

    details: BeautifulSoup = html.find("div", {"class": "details-main"})

    description = details.find("div", {"class": "description"})

    if description is not None:
        description = description.text.strip()

    data = {
        "title": title,
        "address": address,
        "dollar": dollar,
        "som": som,
        "phone": phone,
        "description": description,
    }

    extra_fields: list[BeautifulSoup] = details.find_all("div", {"class": "info-row"})
    for field in extra_fields:
        label = field.find("div", {"class": "label"}).text.strip()
        value = field.find("div", {"class": "info"}).text.strip()

        data.update({label:value})

    return data