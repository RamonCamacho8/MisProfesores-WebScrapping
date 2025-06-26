
# MisProferos's Web Scrapping

As part of the Machine Learning knowledge development for my Master's degree in Computer Science I developed a set of Python scripts and a notebook for scraping, cleaning and translating student comments from the website “misprofesores.com”. The workflow includes obtaining the URLs of the teachers, retrieving the comments, cleaning the corpus and translating the comments from Spanish to English.

## Install dependencies via pip:

```bash
pip install -r requirements.txt
````

## Pipeline Overview

The end-to-end workflow consists of the following stages:

1. **Professor URL Collection**

   - Configure the `schools` list in **get_professors.py** with target universities and their pages on misprofesores.com.
   - Run the script to launch a headless browser via Selenium.
   - Extract all professor profile links and save them as `Universidades/<UniversityName>.txt` files.

2. **Folder Preparation**

   - Execute **folder_creation.py**, pointing it at the `Universidades/` directory.
   - Automatically create a `Corpus/` folder structure where each subdirectory corresponds to a university and initially contains its raw `.txt` file.

3. **Comment Scraping**

   - Feed each `Universidades/<UniversityName>.txt` into the `getCommentsFromProfessors` function in **get_comments.py**.
   - Iterate through each professor URL, handling pagination to collect:
   - **Comment text**, **tags**, **ratings** (quality/easiness), **course names**, **received grades**, and **dates**.
   - Assemble a single pandas DataFrame and export it as `Corpus/<UniversityName>/MP_<UniversityName>.csv`.

4. **Corpus Cleaning**

   - Load the raw CSV into **corpus_cleaning.py** and call `limpiarCorpus`.
   - Rename columns to consistent field names, remove empty or blocked entries, strip punctuation, and drop overly short comments.
   - Write the cleaned dataset to `Corpus/<UniversityName>/L_MP_<UniversityName>.csv`.

5. **Translation to English**

   - Use **translation.py**’s `TraduccionClass` to load a MarianMT model or opt for the DeepL API.
   - Apply the translation pipeline to the `comentario_esp` column, producing `comentario_eng`.
   - Save the final bilingual corpus as `Corpus/<UniversityName>/Final_<UniversityName>.csv`.

6. **Orchestration**

   - For exploratory use, open **Main.ipynb** to step through each phase with visual checkpoints and data previews.
   - For automated batch processing, run **Main.py**, which sequentially invokes professor gathering, folder setup, scraping, cleaning, and translation.

This pipeline ensures reproducible, modular scraping and processing of student review data from Spanish to English, ready for downstream analysis or machine learning tasks.

## File Descriptions

- **folder_creation.py**: Creates output folders mirroring input filenames and optionally copies files into them.
- **get_professors.py**: Automates browser navigation via Selenium to collect professor profile URLs and saves them as text files.
- **get_comments.py**: Parses each professor page (and paginated comments) using BeautifulSoup, collects comments, ratings, tags, dates, and returns a DataFrame.
- **corpus_cleaning.py**: Renames columns, removes punctuation, filters out empty or too-short comments, and resets the index.
- **translation.py**: Defines translation pipelines using either DeepL API or MarianMT models, and applies them to the cleaned DataFrame.
- **Main.ipynb**: Jupyter notebook demonstrating the end-to-end workflow with checkpoints and sample outputs.
- **Main.py**: Non-interactive version of the pipeline for production or batch runs.

## Output Structure

After running the pipeline, the `Corpus/` folder will contain subfolders for each university, each holding CSV files:

- `MP_<UniversityName>.csv`: Raw scraped data
- `L_MP_<UniversityName>.csv`: Cleaned corpus
- `Final_<UniversityName>.csv`: Translated comments
