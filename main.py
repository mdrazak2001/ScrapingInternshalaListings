from bs4 import BeautifulSoup
import requests

internshalaDone = False


def get_page(page):
    page_res = []
    html_text = requests.get(f'https://internshala.com/internships/computer-science-internship/page-{page}').text
    soup = BeautifulSoup(html_text, 'html.parser')
    pgDiv = soup.find("div", {"id": "pagination"})
    lastPg = pgDiv.find('input', {"id": "isLastPage"})
    if lastPg['value'] == '1':
        global internshalaDone
        internshalaDone = True
    myDiv = soup.find_all("div", {"class": "container-fluid individual_internship visibilityTrackerItem"})
    for jobDiv in myDiv:
        try:
            detail = 'NA' if jobDiv.find('a', class_='view_detail_button') is None else jobDiv.find('a',
                                                                                                    class_='view_detail_button').text
            name = 'NA' if jobDiv.find('a',
                                       class_='link_display_like_text view_detail_button') is None else jobDiv.find('a',
                                                                                                                    class_='link_display_like_text view_detail_button').text
            stipend = 'NA' if jobDiv.find('span', class_='stipend') is None else jobDiv.find('span',
                                                                                             class_='stipend').text
            published_date = 'NA' if jobDiv.find('div',
                                                 class_="status status-small status-success") is None else jobDiv.find(
                'div', class_="status status-small status-success").text
            linkDesc = jobDiv.find('div', class_='cta_container')
            applyLink = linkDesc.find('a', class_='view_detail_button')
            applyLink = "https://internshala.com" + applyLink['href']
            page_res.append([name.strip(), detail.strip(), stipend.strip(), published_date.strip(), applyLink.strip()])
        except Exception as E:
            print(E)
    return page_res


def internshalaListings():
    res = []
    page = 1
    while True:
        temp = get_page(page)
        page = page + 1
        res.extend(temp)
        if internshalaDone:
            break
    with open('internshalaListings.txt', 'w') as file:
        for job in res:
            file.write(f'Name: {job[0]}\nDetail: {job[1]}\nStipend: {job[2]}\nPublished Date: {job[3]}\nApply Link: {job[4]}\n')
            file.write('-----------------------------------------------\n')
    return res


if __name__ == '__main__':
    res = internshalaListings()
