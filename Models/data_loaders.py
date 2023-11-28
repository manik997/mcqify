from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import YoutubeLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader



def load_html(file_path):
    loader = UnstructuredHTMLLoader(file_path)
    data = loader.load()
    data = [item.page_content for item in data]
    data = " \n  \n".join(data)
    return data


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    data = [item.page_content for item in pages]
    data = " \n new record in a csv \n".join(data)
    return data

def load_doc(file_path):
    loader = Docx2txtLoader(file_path)
    data = loader.load()
    data = [item.page_content for item in data]
    data = " \n  \n".join(data)
    return data

def load_csv(file_path):
    loader = CSVLoader(file_path=file_path)
    data = loader.load()
    data = [item.page_content for item in data]
    data = " \n new record in a csv \n".join(data)
    return data

def load_text(file_path):
    loader = TextLoader(file_path)
    data = loader.load()
    data = [item.page_content for item in data]
    data = " \n \n".join(data)
    return data

def load_youtubeurl(url):
    loader = YoutubeLoader.from_youtube_url(
        url, add_video_info=True
    )
    data = loader.load()
    data = [item.page_content for item in data]
    data = " \n  \n".join(data)
    return data





