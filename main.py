from src.scraper import run_scraper
from src.analysis import run_analysis


def main():
    try:
        print("Starting scraper...")
        run_scraper()

        print("Running analysis...")
        run_analysis()

        print("Pipeline completed successfully.")

    except Exception as e:
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()