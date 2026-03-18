from src.scraper import run_scraper
from src.analysis import run_analysis


def main():
    print("Starting scraper...")
    run_scraper()

    print("Running analysis...")
    run_analysis()


if __name__ == "__main__":
    main()