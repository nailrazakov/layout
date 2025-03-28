# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети

#  формирование абсолютного пути к файлу с Html страницей
PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "contacts_remote.html")


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def __get_contacts(self):
        try:
            with open(PATH_TO_FILE, encoding='utf-8') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return "FileNotFound"

    def do_GET(self):
        page_content = self.__get_contacts()
        """ Метод для обработки входящих GET-запросов """
        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "text/html")  # Отправка типа данных
        self.end_headers()  # Завершение формирования заголовков ответа
        self.wfile.write(bytes(page_content, "utf-8"))  # Тело ответа

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = f"Received POST data: {post_data.decode('utf-8')}"
        #  печать в консоль всех данных, которые были приняты от пользователя
        print(post_data.decode('utf-8'))
        self.wfile.write(response.encode('utf-8'))


if __name__ == "__main__":
    #  Инициализация веб-сервера, который будет по заданным параметрах в сети
    #  принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
