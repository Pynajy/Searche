from date import search_engin
from date.urls import list_urls_1, list_urls_2, list_urls_3, list_urls_4

main_search = search_engin.Search()

# main_search.search(list_urls_1)
# main_search.search_yandex(list_urls_2)
main_search.search_google(list_urls_4)
main_search.close_driver()
