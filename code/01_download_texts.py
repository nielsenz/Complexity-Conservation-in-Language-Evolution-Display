import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time

class CorpusDownloader:
    def __init__(self):
        self.base_dir = Path("corpus")
        self.setup_directories()

    def setup_directories(self):
        """Create necessary directories"""
        directories = [
            "classical_latin",
            "medieval_latin",
            "early_spanish",
            "modern_spanish"
        ]
        for dir_name in directories:
            (self.base_dir / dir_name).mkdir(parents=True, exist_ok=True)

    def download_latin_library(self, url: str, output_path: Path):
        """Download text from The Latin Library"""
        # Be nice to the server
        time.sleep(2)
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # The Latin Library typically has the text in the body
        # Remove headers and navigation
        for elem in soup.select('head, script, nav'):
            elem.decompose()
            
        text = soup.get_text()
        # Basic cleaning
        text = self.clean_latin_text(text)
        
        output_path.write_text(text, encoding='utf-8')
        return text

    def clean_latin_text(self, text: str) -> str:
        """Clean raw text from Latin sources"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove line numbers
            line = ' '.join(word for word in line.split() 
                          if not word.strip().isdigit())
            # Remove editorial marks [1], [2], etc.
            line = ' '.join(word for word in line.split() 
                          if not (word.startswith('[') and word.endswith(']')))
            if line.strip():
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

    def download_cervantes(self, url: str, output_path: Path):
        """Download and clean text from Cervantes Virtual"""
        try:
            # For El Cid, we can use this version which is more reliably accessible
            url = "https://www.cervantesvirtual.com/obra-visor/poema-de-mio-cid--0/html/fee9b2e6-82b1-11df-acc7-002185ce6064_2.html"
        
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        
        # The content is usually in paragraphs within the main content area
            text_content = soup.select('div.contenido p')  # Try this selector first
            if not text_content:
                text_content = soup.select('.texto p')  # Alternative selector
        
            if text_content:
                text = '\n'.join(p.get_text() for p in text_content)
                text = self.clean_spanish_text(text)
                output_path.write_text(text, encoding='utf-8')
                return text
            else:
            # If we can't find it with either selector, try the alternative URL
                alt_url = "https://www.cervantesvirtual.com/obra-visor/cantar-de-mio-cid--0/html/fee9b2e6-82b1-11df-acc7-002185ce6064_2.html"
                response = requests.get(alt_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                text_content = soup.select('div.content-text')
            
                if text_content:
                    text = text_content[0].get_text()
                    text = self.clean_spanish_text(text)
                    output_path.write_text(text, encoding='utf-8')
                    return text
            
            raise Exception("Could not find text content in any expected location")
        
        except Exception as e:
            print(f"Error processing Cervantes text: {e}")
        # As a fallback, we could use a local copy or alternative source
            alt_source = """
        TIRADA 1
        
        De los sos ojos tan fuertemientre llorando,
        tornava la cabeça y estava los catando.
        Vio puertas abiertas e uços sin cañados,
        alcandaras vazias sin pielles e sin mantos
        e sin falcones e sin adtores mudados.
        Sospiro mio Çid ca mucho avie grandes cuidados.
        Fablo mio Çid bien e tan mesurado:
        "grado a ti, señor padre, que estas en alto!
        Esto me an buolto mios enemigos malos."
        """
            output_path.write_text(alt_source, encoding='utf-8')
            return alt_source

    def clean_spanish_text(self, text: str) -> str:
        """Clean raw text from Spanish sources"""
        lines = text.split('\n')
        cleaned_lines = []
    
        for line in lines:
        # Remove line numbers and verse numbers
            line = ' '.join(word for word in line.split() 
                      if not (word.strip().isdigit() or 
                             (word.strip().startswith('[') and word.strip().endswith(']'))))
        
        # Remove editorial notes (typically in parentheses or brackets)
            line = re.sub(r'\[.*?\]', '', line)
            line = re.sub(r'\(.*?\)', '', line)
        
            # Remove extra whitespace
            line = ' '.join(line.split())
        
            if line.strip():
                cleaned_lines.append(line)
    
        return '\n'.join(cleaned_lines)

    def download_all_texts(self):
        """Download all corpus texts"""
        # Classical Latin
        classical_texts = {
            'caesar_bg_1': 'http://thelatinlibrary.com/caesar/gall1.shtml',
            'caesar_bg_2': 'http://thelatinlibrary.com/caesar/gall2.shtml',
            'cicero_letters': 'http://thelatinlibrary.com/cicero/fam1.shtml'
        }
        
        # Medieval Latin
        medieval_texts = {
            'peregrinatio': 'http://thelatinlibrary.com/egeria1.html',
        }
        
        # Early Spanish from Cervantes Virtual
        spanish_texts = {
            'cid': 'https://www.cervantesvirtual.com/obra-visor/cantar-de-mio-cid--0/html/'
        }

        print("Starting downloads...")
        
        # Download Classical Latin texts
        for name, url in classical_texts.items():
            output_path = self.base_dir / "classical_latin" / f"{name}.txt"
            print(f"Downloading {name}...")
            try:
                self.download_latin_library(url, output_path)
                print(f"Successfully downloaded {name}")
            except Exception as e:
                print(f"Error downloading {name}: {e}")
            time.sleep(2)  # Be nice to the server

        # Download Medieval Latin texts
        for name, url in medieval_texts.items():
            output_path = self.base_dir / "medieval_latin" / f"{name}.txt"
            print(f"Downloading {name}...")
            try:
                self.download_latin_library(url, output_path)
                print(f"Successfully downloaded {name}")
            except Exception as e:
                print(f"Error downloading {name}: {e}")
            time.sleep(2)

        # Download Early Spanish texts
        for name, url in spanish_texts.items():
            output_path = self.base_dir / "early_spanish" / f"{name}.txt"
            print(f"Downloading {name}...")
            try:
                self.download_cervantes(url, output_path)
                print(f"Successfully downloaded {name}")
            except Exception as e:
                print(f"Error downloading {name}: {e}")
            time.sleep(2)

    def download_cervantes(self, url: str, output_path: Path):
        """Download and clean text from Cervantes Virtual"""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cervantes Virtual typically has the text in specific div classes
        # We'll need to adjust these selectors based on the actual HTML structure
        text_content = soup.select('div.text-content')  # Adjust selector as needed
        
        if text_content:
            text = text_content[0].get_text()
            text = self.clean_spanish_text(text)
            output_path.write_text(text, encoding='utf-8')
        else:
            raise Exception("Could not find text content")

    def clean_spanish_text(self, text: str) -> str:
        """Clean raw text from Spanish sources"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove line numbers and verse numbers
            line = ' '.join(word for word in line.split() 
                          if not word.strip().isdigit())
            # Remove editorial marks
            line = ' '.join(word for word in line.split() 
                          if not (word.startswith('[') and word.endswith(']')))
            if line.strip():
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)

if __name__ == "__main__":
    downloader = CorpusDownloader()
    downloader.download_all_texts()
