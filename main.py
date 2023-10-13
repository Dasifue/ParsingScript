from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import time

from parser import get_html, get_links, parse_data
from save import SaveData

URL = "https://www.house.kg/snyat-kvartiru?rooms=1&page={}"

def main():
    
    start = time.perf_counter()

    with ThreadPoolExecutor() as executor:
        urls = (URL.format(page) for page in range(1, 3))
        htmls = executor.map(get_html, urls)

    print("\nПоиск ссылок...\n")
    with ThreadPoolExecutor() as executor:
        page_links = executor.map(get_links, htmls)
        
    links = []
    for generator in page_links:
        links.extend(generator)

    print(f"Всего найдено ссылок: {len(links)}\n")
        
    with ThreadPoolExecutor() as executor:
        htmls = (get_html(link) for link in links)
        data = executor.map(parse_data, htmls)

    save_data = SaveData(path="/home/dasifue/Desktop", echo=True)

    threads = (Thread(target=save_data.save_in_csv, args=("apartments.csv", d)) for d in data)
    # threads = (Thread(target=save_data.save_in_txt, args=("apartments.txt", d)) for d in data)
    # threads = (Thread(target=save_data.save_in_json, args=("apartments.json", d)) for d in data)

    for task in threads:
        task.start()

    for task in threads:
        task.join()
    
    finish = time.perf_counter()

    print(f"Завершено за: {finish - start} секунд.")


if __name__ == "__main__":
    main()