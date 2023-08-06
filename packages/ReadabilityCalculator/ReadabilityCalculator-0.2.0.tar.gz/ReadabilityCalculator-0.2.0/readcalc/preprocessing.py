# To clean html
import justext
from bs4 import BeautifulSoup
#from boilerpipe.extract import Extractor

def preprocess_html(text, preprocessor):
    if not preprocessor:
        return text

    elif preprocessor == "bs4":
        soup = BeautifulSoup(text, "html.parser")
        tags_to_remove = ["script"]
        for tag in tags_to_remove:
            for x in soup.body(tag):
                x.decompose()
        return soup.body.get_text()

    elif preprocessor == "justext":
        paragraphs = justext.justext(text, justext.get_stoplist('English'))
        text = "\n"
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate: # and not paragraph.is_header:
                text = text + paragraph.text + "\n"
        return text

    # At the moment that this code was updated, boilerpipe was not available for download via pip.
    #elif preprocessor == "boilerpipe":
    #    extractor = Extractor(extractor='ArticleExtractor', html=content)
    #    return extractor.getText()

    else:
        print "PRE PROCESSING OPTION NOT FOUND. IGNORING PRE PROCESSING."
        return text


