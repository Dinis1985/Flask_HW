# Написать программу, которая скачивает изображения с заданных URL-адресов и
# сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
# файле, название которого соответствует названию изображения в URL-адресе.
# Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
# image1.jpg
# Программа должна использовать многопоточный, многопроцессорный и
# асинхронный подходы.
# Программа должна иметь возможность задавать список URL-адресов через
# аргументы командной строки.
# Программа должна выводить в консоль информацию о времени скачивания
# каждого изображения и общем времени выполнения программы.

import asyncio
import os
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import aiohttp
import aiofiles


async def download_image(session, url, output_folder):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                filename = os.path.basename(url)
                output_path = os.path.join(output_folder, filename)
                os.makedirs(output_folder, exist_ok=True)
                start_time1 = time.time()
                async with aiofiles.open(output_path, 'wb') as f:
                    await f.write(content)
                end_time1 = time.time()
                total_time1 = end_time1 - start_time1
                print(f"Image {filename} downloaded successfully. Time: {total_time1:.3f}")
            else:
                print(f"Failed to download image from {url}")
    except Exception as epr_1:
        print(f"An error occurred while downloading image from {url}: {epr_1}")


# функция асинхронная
async def download_images_async(urls, output_folder):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, url, output_folder) for url in urls]
        await asyncio.gather(*tasks)


# функция для работы с потоками
def download_images_thread(urls, output_folder):
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_images_async(urls, output_folder))


# функция для многопроцессорного подхода
def download_images_process(urls, output_folder):
    with ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(download_images_async(urls, output_folder))


def main():
    # парсим командную строку
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs='+')
    parser.add_argument("--output_folder", default="images")
    args = parser.parse_args()
    url = args.urls[0]
    urls = []
    # генерируем урлы с картинками
    for i in range(16):
        first = url.split('jpg')
        second = first[0].strip('.1')
        urls.append(''.join(second + str(i+1) + '.jpg'))

    start_time = time.time()

    # многопоточный подход
    download_images_thread(urls, args.output_folder)
    # многопроцессорный подход
    download_images_process(urls, args.output_folder)
    # асинхронный подход
    asyncio.run(download_images_async(urls, args.output_folder))

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time:.2f} seconds")


if __name__ == "__main__":
    main()
