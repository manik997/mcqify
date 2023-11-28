from langchain.document_loaders import UnstructuredURLLoader

def mcqs_from_URL(url):
    urls = [url]
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()
    text = data[0].page_content
    return text

# print(mcqs_from_URL("https://python.langchain.com/docs/integrations/document_loaders/youtube_transcript"))
