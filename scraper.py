from ddgs import DDGS
import json
import io

def scrape(query, max_results=10):
    # max_result implicitne = 10, standardne vyhledavaji ma prave 10 vysledku na jedne strane. 
    try:
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(query, region='cz-cz', safesearch='off')
            results = list(ddgs_gen)
            for i, r in enumerate(results):
                print(f"{i + 1}. {r['title']}")
                print(f" URL: {r['href']}")
                print(f" Popis: {r['body']}")
            return results

    except Exception as e:
        print("Chyba :" + str(e) )
        return []


def prepare_for_download(res):
    if not res:
        print("Musite prvne zadat klicova slova pred ulozenim")
        return

    try:
        json_str = json.dumps(res, ensure_ascii=False, indent=4)
        mem = io.BytesIO()
        mem.write(json_str.encode('utf-8'))
        mem.seek(0)
        return mem

    except Exception as e:
        print("Chyba při exportu:" + str(e) )
        return
