import re, requests
from bs4 import BeautifulSoup


def get_lectionary_data():
    url = 'https://lectionary.anglican.ca'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        lectionary_MP = soup.find(id='lectionary_MP').get_text(strip=True)
        lectionary_HE = soup.find(id='lectionary_HE').get_text(strip=True)
        lectionary_EP = soup.find(id='lectionary_EP').get_text(strip=True)
        return (lectionary_MP, lectionary_EP)

        print("Lectionary MP:", lectionary_MP)
        print("Lectionary HE:", lectionary_HE)
        print("Lectionary EP:", lectionary_EP)
    else:
        print("Error: Unable to get webpage content")

def extract_bible_verses(text):
    pattern = r'\b(?:[1-3]\s)?[A-Za-z]+ \d{1,3}(?::\d{1,3}(?:-\d{1,3})?)?\b'
    bible_verses = re.findall(pattern, text)
    return bible_verses


def get_bible_passage(reference, version='NRSVA'):
    base_url = 'https://www.biblegateway.com/passage/'
    params = {
        'search': reference,
        'version': version
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        bible_text_element = soup.find(class_='version-{} result-text-style-normal text-html'.format(version))
        
        if bible_text_element is None:
            print("Error: Unable to find Bible passage.")
            return

        bible_text = bible_text_element.get_text(separator='\n')
        return bible_text
    else:
        print("Error: Unable to get webpage content")

if __name__ == '__main__':
    lectionary_data = get_lectionary_data()
    M_verses = extract_bible_verses(lectionary_data[0])
    E_verses = extract_bible_verses(lectionary_data[1])
    print("Morning readings")
    for verse in M_verses:
        bible_text = get_bible_passage(verse)
        print(verse)
        print(bible_text)
        print("\n")
    print("Evening readings...")
    for verse in E_verses:
        bible_text = get_bible_passage(verse)
        print(verse)
        print(bible_text)
        print("\n")
