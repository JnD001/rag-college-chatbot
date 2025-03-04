from colorama import Fore

from src.scraping import BaseScraper, preprocess_text
from src.utils import logger


class ProgramScraper(BaseScraper):
    def __init__(self, url):
        super().__init__(category="program", sitemap_url=url)

    def scrape(self):
        """Fetches all links from sitemap and scrapes each page."""
        urls = self.fetch_sitemap_links()
        try:
            for index, url in enumerate(urls, start=1):
                soup = self.fetch_content(url)
                program_content = soup.find(class_="program")
                if program_content:
                    logger.info(
                        f"{Fore.YELLOW}successfully scraped {index}/{len(urls)}{Fore.GREEN} {self.category} {Fore.RESET}{url}"
                    )
                    text = program_content.get_text(separator="\n", strip=True)
                    word_count = len(text.split())
                    num_paragraphs = text.count("\n")

                    self.save_data(content=preprocess_text(text), index=index)
                    self.save_metadata(
                        id=index,
                        url=url,
                        word_count=word_count,
                        num_paragraphs=num_paragraphs,
                        title="none",
                        summary="none",
                        keywords=["none", "noone"],
                    )
            else:
                logger.error("there is no class such as 'program', scraping failed.")
        except Exception as e:
            logger.exception(f"something went wrong as : {e}")
