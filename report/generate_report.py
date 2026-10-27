from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "report" / "Movie_ETL_Internship_Report.pdf"
OUTPUT.parent.mkdir(exist_ok=True)

PAGE_W, PAGE_H = A4
LEFT = 1.5 * inch
RIGHT = 1 * inch
TOP = 1 * inch
BOTTOM = 1 * inch


def register_fonts():
    candidates = [
        ("/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf", "TNR"),
        ("/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.ttf", "TNR-Bold"),
        ("/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Italic.ttf", "TNR-Italic"),
    ]
    found = {}
    for path, name in candidates:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont(name, path))
            found[name] = True
    return found


FONT = "Times-Roman"
BOLD = "Times-Bold"
ITALIC = "Times-Italic"
fonts = register_fonts()
if "TNR" in fonts:
    FONT, BOLD, ITALIC = "TNR", "TNR-Bold", "TNR-Italic"


class NumberedCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(page_count)
            Canvas.showPage(self)
        Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber > 1:
            self.setFont(FONT, 10)
            self.drawCentredString(PAGE_W / 2, 0.55 * inch, str(self._pageNumber - 1))


def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(HexColor("#666666"))
        canvas.setLineWidth(0.35)
        canvas.line(LEFT, PAGE_H - 0.68 * inch, PAGE_W - RIGHT, PAGE_H - 0.68 * inch)
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["Normal"], fontName=FONT, fontSize=12,
    leading=18, alignment=TA_JUSTIFY, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Chapter", parent=styles["Heading1"], fontName=BOLD, fontSize=16,
    leading=22, alignment=TA_CENTER, textTransform="uppercase", spaceBefore=6,
    spaceAfter=20,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading2"], fontName=BOLD, fontSize=14,
    leading=19, alignment=TA_LEFT, spaceBefore=10, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Subsection", parent=styles["Heading3"], fontName=BOLD, fontSize=12,
    leading=17, alignment=TA_LEFT, spaceBefore=8, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Normal"], fontName=BOLD, fontSize=20,
    leading=28, alignment=TA_CENTER, spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="CoverSmall", parent=styles["Normal"], fontName=FONT, fontSize=13,
    leading=20, alignment=TA_CENTER, spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Center", parent=styles["Normal"], fontName=FONT, fontSize=12,
    leading=18, alignment=TA_CENTER, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Caption", parent=styles["Normal"], fontName=BOLD, fontSize=12,
    leading=17, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="CodeCustom", parent=styles["Normal"], fontName="Courier", fontSize=8.5,
    leading=11, leftIndent=10, rightIndent=10, backColor=HexColor("#F3F3F3"),
    borderColor=HexColor("#CCCCCC"), borderWidth=0.5, borderPadding=6,
    spaceBefore=5, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="TOC", parent=styles["Normal"], fontName=FONT, fontSize=12,
    leading=20, leftIndent=12, spaceAfter=2,
))


def P(text, style="BodyCustom"):
    return Paragraph(text, styles[style])


def bullet(text):
    return Paragraph(f"&bull;&nbsp;&nbsp;{text}", styles["BodyCustom"])


def table(data, widths, header=True):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    commands = [
        ("FONTNAME", (0, 0), (-1, -1), FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LEADING", (0, 0), (-1, -1), 14),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        commands += [
            ("FONTNAME", (0, 0), (-1, 0), BOLD),
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#E6E6E6")),
        ]
    t.setStyle(TableStyle(commands))
    return t


def code(text):
    return P(text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>"), "CodeCustom")


story = []

# Cover page
story += [
    Spacer(1, 0.65 * inch),
    P("INTERNSHIP PROJECT REPORT", "CoverTitle"),
    P("ON", "CoverSmall"),
    P("MOVIE DATASET ETL PIPELINE AND SQL ANALYTICS", "CoverTitle"),
    Spacer(1, 0.35 * inch),
    P("A report submitted in partial fulfillment of the requirements for the completion of a 45-day internship", "CoverSmall"),
    Spacer(1, 0.5 * inch),
    P("Submitted By", "CoverSmall"),
    P("[STUDENT NAME]", "CoverTitle"),
    P("Enrollment No.: [ENROLLMENT NUMBER]", "CoverSmall"),
    P("Course / Semester: [COURSE AND SEMESTER]", "CoverSmall"),
    Spacer(1, 0.35 * inch),
    P("Under the Guidance of", "CoverSmall"),
    P("[GUIDE / SUPERVISOR NAME]", "CoverTitle"),
    Spacer(1, 0.45 * inch),
    P("[COLLEGE / UNIVERSITY NAME]", "CoverSmall"),
    P("[DEPARTMENT NAME]", "CoverSmall"),
    P("Internship Duration: 45 Days", "CoverSmall"),
    P("[MONTH YEAR]", "CoverSmall"),
    PageBreak(),
]

# Certificate
story += [
    P("CERTIFICATE", "Chapter"),
    Spacer(1, 0.2 * inch),
    P("This is to certify that <b>[STUDENT NAME]</b>, Enrollment No. <b>[ENROLLMENT NUMBER]</b>, student of <b>[COURSE / DEPARTMENT]</b> at <b>[COLLEGE / UNIVERSITY NAME]</b>, has successfully completed a 45-day internship project entitled <b>“Movie Dataset ETL Pipeline and SQL Analytics”</b> under my guidance and supervision."),
    P("The work presented in this report is based on the practical activities carried out during the internship. The project involved data extraction, data cleaning, relational table design, Snowflake data loading, and SQL-based analysis of a movie dataset."),
    Spacer(1, 0.5 * inch),
    table([
        [P("Internship Supervisor", "Center"), P("Head of Department", "Center")],
        [P("Signature: ____________________", "Center"), P("Signature: ____________________", "Center")],
        [P("Name: [SUPERVISOR NAME]", "Center"), P("Name: [HOD NAME]", "Center")],
        [P("Date: _________________________", "Center"), P("Date: _________________________", "Center")],
    ], [3.1 * inch, 3.1 * inch], header=False),
    PageBreak(),
]

# Declaration
story += [
    P("DECLARATION", "Chapter"),
    P("I hereby declare that the internship report entitled <b>“Movie Dataset ETL Pipeline and SQL Analytics”</b> is an original record of the work carried out by me during the 45-day internship period. The project work, analysis, SQL queries, and documentation included in this report were prepared for academic submission."),
    P("I further declare that this report has not been submitted previously, in whole or in part, for the award of any other qualification. Wherever external tools, libraries, documentation, or datasets were used, they have been acknowledged appropriately."),
    Spacer(1, 0.65 * inch),
    P("Place: [CITY]", "BodyCustom"),
    P("Date: [DATE]", "BodyCustom"),
    Spacer(1, 0.25 * inch),
    P("Signature of Student: __________________________", "BodyCustom"),
    P("Name: [STUDENT NAME]", "BodyCustom"),
    PageBreak(),
]

# Acknowledgement
story += [
    P("ACKNOWLEDGEMENT", "Chapter"),
    P("I express my sincere gratitude to my internship supervisor, <b>[SUPERVISOR NAME]</b>, for providing guidance, feedback, and encouragement throughout the internship. Their support helped me understand the practical application of SQL, data warehousing, and ETL processes."),
    P("I am thankful to the faculty members of <b>[DEPARTMENT NAME]</b> and <b>[COLLEGE / UNIVERSITY NAME]</b> for providing the academic support and resources required to complete this project."),
    P("I also acknowledge the open-source community and the documentation of Python, pandas, Airbyte, Snowflake, and SQL, which were useful during the development and testing of the pipeline."),
    Spacer(1, 0.6 * inch),
    P(" [STUDENT NAME]", "Center"),
    PageBreak(),
]

# Abstract
story += [
    P("ABSTRACT", "Chapter"),
    P("This report presents the design and implementation of a movie dataset ETL pipeline developed during a 45-day internship focused on SQL and data engineering. The project starts with a raw CSV file containing approximately 4,000 movie records and transforms the data into structured relational tables suitable for analysis."),
    P("The pipeline uses Python and pandas for extraction and transformation, Airbyte for source-to-warehouse ingestion, Snowflake as the cloud data warehouse, and SQL for table creation, joins, filtering, grouping, and aggregation. The original denormalized dataset is divided into four related tables: MOVIES, RATINGS, FINANCIALS, and PEOPLE. A generated MOVIE_ID connects the tables and enables meaningful relational queries."),
    P("The SQL analysis produces insights such as the highest-rated movies, profitable movies, average rating by genre, yearly financial performance, active directors, and highly voted movies. The project demonstrates the complete flow from raw data to analytical results and provides a foundation for future improvements such as data quality testing, incremental loading, scheduling, and dashboard integration."),
    PageBreak(),
]

# TOC
story += [
    P("TABLE OF CONTENTS", "Chapter"),
    P("1. Introduction", "TOC"),
    P("2. Internship Objectives", "TOC"),
    P("3. Background and Technologies Used", "TOC"),
    P("4. System Analysis and Requirements", "TOC"),
    P("5. Methodology and Pipeline Design", "TOC"),
    P("6. Implementation", "TOC"),
    P("7. SQL Analysis and Results", "TOC"),
    P("8. Testing and Validation", "TOC"),
    P("9. Learning Outcomes", "TOC"),
    P("10. Limitations and Future Scope", "TOC"),
    P("11. Conclusion", "TOC"),
    P("References", "TOC"),
    PageBreak(),
]

# Chapter 1
story += [
    P("CHAPTER 1: INTRODUCTION", "Chapter"),
    P("1.1 Project Overview", "Section"),
    P("The Movie Dataset ETL Pipeline is a data engineering and SQL analytics project. Its primary purpose is to convert a raw movie dataset into clean, structured, and queryable data. Instead of keeping all information in one flat file, the project separates movie details, ratings, financial information, and people involved in the movie into related tables."),
    P("The project was developed as an internship assignment over 45 days. The major focus of the internship was SQL, including relational table design, joins, filtering, aggregation, and analytical query writing. Python and pandas were used to prepare the data, while Snowflake was used as the target data warehouse."),
    P("1.2 Problem Statement", "Section"),
    P("A raw CSV file is convenient for collection but is not ideal for repeated analysis. It may contain missing values, inconsistent data types, repeated information, and multiple business concepts in the same row. The problem addressed in this project is to build a repeatable process that cleans the raw data, organizes it into related tables, loads it into a warehouse, and supports analytical SQL queries."),
    P("1.3 Scope of the Project", "Section"),
    bullet("Read a semicolon-separated movie CSV file using the correct encoding."),
    bullet("Remove records that do not contain a movie name."),
    bullet("Convert numeric fields such as year, score, votes, budget, and gross."),
    bullet("Generate a unique movie_id for relational connections."),
    bullet("Split the source into four subject-oriented tables."),
    bullet("Create Snowflake tables and load processed data."),
    bullet("Use SQL joins, filters, GROUP BY, HAVING, ORDER BY, and aggregate functions."),
    PageBreak(),
]

# Chapter 2
story += [
    P("CHAPTER 2: INTERNSHIP OBJECTIVES", "Chapter"),
    P("2.1 Main Objectives", "Section"),
    bullet("Understand the complete ETL lifecycle: extract, transform, and load."),
    bullet("Develop practical skills in SQL query writing and relational data analysis."),
    bullet("Learn how a cloud data warehouse such as Snowflake stores analytical data."),
    bullet("Use pandas to clean and reshape a real-world dataset."),
    bullet("Understand how Airbyte can automate source-to-destination data movement."),
    bullet("Design tables that can be joined using a common key."),
    bullet("Document the workflow so that the pipeline can be reproduced."),
    P("2.2 Internship Work Plan", "Section"),
    table([
        ["Period", "Major Activities"],
        ["Days 1-5", "Project understanding, dataset inspection, requirements, and environment setup."],
        ["Days 6-12", "CSV extraction, delimiter and encoding handling, and raw data profiling."],
        ["Days 13-22", "Pandas transformation, data type conversion, missing-value handling, and movie_id generation."],
        ["Days 23-30", "Relational table design and creation of MOVIES, RATINGS, FINANCIALS, and PEOPLE tables."],
        ["Days 31-37", "Snowflake loading, Airbyte configuration, and connection verification."],
        ["Days 38-43", "SQL joins, filters, aggregations, and result validation."],
        ["Days 44-45", "Documentation, report preparation, review, and final presentation."],
    ], [1.1 * inch, 5.1 * inch]),
    PageBreak(),
]

# Chapter 3
story += [
    P("CHAPTER 3: BACKGROUND AND TECHNOLOGIES USED", "Chapter"),
    P("3.1 Python and pandas", "Section"),
    P("Python is used as the programming language for the local ETL workflow. The pandas library reads the CSV file into a DataFrame, removes unusable records, converts columns to numeric types, generates movie identifiers, and creates the four output tables."),
    P("3.2 SQL", "Section"),
    P("SQL is the central analytical technology used in the internship. It is used to create tables, join related data, filter records, group data, calculate averages and totals, and order analytical results. The project includes separate SQL files for table creation, joins, aggregations, and filters."),
    P("3.3 Snowflake", "Section"),
    P("Snowflake is used as the cloud data warehouse. It stores the processed tables and provides an environment in which SQL queries can be executed. The Python Snowflake connector and write_pandas utility support programmatic loading."),
    P("3.4 Airbyte", "Section"),
    P("Airbyte is used for data ingestion from a File/CSV source to Snowflake. The configured source uses a semicolon delimiter and ISO-8859-1 encoding. The connection is documented as a full-refresh, overwrite sync because the dataset is static."),
    P("3.5 Supporting Tools", "Section"),
    table([
        ["Technology", "Purpose"],
        ["Python", "ETL orchestration and scripting"],
        ["pandas", "Data cleaning and transformation"],
        ["SQL", "Schema creation and analytical queries"],
        ["Snowflake", "Cloud data warehouse"],
        ["Airbyte", "Data ingestion and synchronization"],
        ["python-dotenv", "Reading environment variables"],
        ["Git", "Source-code version control"],
    ], [1.7 * inch, 4.5 * inch]),
    PageBreak(),
]

# Chapter 4
story += [
    P("CHAPTER 4: SYSTEM ANALYSIS AND REQUIREMENTS", "Chapter"),
    P("4.1 Existing System", "Section"),
    P("In the existing form, the dataset is maintained as one denormalized CSV file. Movie details, ratings, financial values, and information about directors and stars occur in the same row. While this format is easy to open, it is less suitable for warehouse-style analysis and makes the data structure difficult to extend."),
    P("4.2 Proposed System", "Section"),
    P("The proposed system creates a repeatable ETL pipeline. The raw file is read with the required delimiter and encoding, cleaned with pandas, split into four subject-oriented tables, and loaded to Snowflake. SQL queries then combine the tables when a complete movie-level view is required."),
    P("4.3 Functional Requirements", "Section"),
    bullet("The system shall read the raw movie CSV file."),
    bullet("The system shall remove rows without a movie name."),
    bullet("The system shall convert relevant columns to numeric data types."),
    bullet("The system shall create a unique identifier for each movie record."),
    bullet("The system shall generate four processed tables."),
    bullet("The system shall create corresponding Snowflake tables."),
    bullet("The system shall support analytical SQL queries."),
    P("4.4 Non-Functional Requirements", "Section"),
    bullet("The pipeline should be repeatable from the project root."),
    bullet("Credentials should be supplied through environment variables."),
    bullet("The output tables should have consistent column names."),
    bullet("The SQL should be readable and separated by analytical purpose."),
    PageBreak(),
]

# Chapter 5
story += [
    P("CHAPTER 5: METHODOLOGY AND PIPELINE DESIGN", "Chapter"),
    P("5.1 ETL Architecture", "Section"),
    code("Raw movies.csv\n        |\n        v\nExtract: etl/extract.py\n        |\n        v\nTransform: etl/transform.py\n        |\n        +--> movies.csv\n        +--> ratings.csv\n        +--> financials.csv\n        +--> people.csv\n        |\n        v\nLoad: etl/load.py / Airbyte\n        |\n        v\nSnowflake tables\n        |\n        v\nSQL analysis"),
    P("Figure 5.1: Overall Architecture of the Movie ETL Pipeline", "Caption"),
    P("5.2 Extraction", "Section"),
    P("The extraction step reads data/raw/movies.csv with pandas. The source file is semicolon-separated and encoded using ISO-8859-1. Handling these settings is important because using the default comma delimiter or UTF-8 encoding can result in incorrect columns or character errors."),
    code('df = pd.read_csv(\n    "data/raw/movies.csv",\n    sep=";",\n    quotechar=\'"\',\n    encoding="ISO-8859-1"\n)'),
    P("5.3 Transformation", "Section"),
    P("The transformation step removes rows without a name, resets the index, and creates movie_id values beginning from 1. Numeric columns are converted with errors coerced to missing values. The cleaned DataFrame is projected into four tables."),
    P("5.4 Loading", "Section"),
    P("The loading step reads the processed CSV files, creates Snowflake tables from the schema SQL, converts column names to uppercase, and uses write_pandas to upload each table. Environment variables are used for credentials and connection settings."),
    P("5.5 Data Model", "Section"),
    table([
        ["Table", "Main Columns", "Relationship"],
        ["MOVIES", "MOVIE_ID, NAME, GENRE, YEAR, RUNTIME, COUNTRY, COMPANY", "Central movie information"],
        ["RATINGS", "MOVIE_ID, SCORE, VOTES, RATING", "Connected through MOVIE_ID"],
        ["FINANCIALS", "MOVIE_ID, BUDGET, GROSS", "Connected through MOVIE_ID"],
        ["PEOPLE", "MOVIE_ID, DIRECTOR, WRITER, STAR", "Connected through MOVIE_ID"],
    ], [1.2 * inch, 3.6 * inch, 1.4 * inch]),
    PageBreak(),
]

# Chapter 6
story += [
    P("CHAPTER 6: IMPLEMENTATION", "Chapter"),
    P("6.1 Project Structure", "Section"),
    code("movie-etl-pipeline/\n|-- data/raw/movies.csv\n|-- data/processed/\n|   |-- movies.csv\n|   |-- ratings.csv\n|   |-- financials.csv\n|   `-- people.csv\n|-- etl/\n|   |-- extract.py\n|   |-- transform.py\n|   `-- load.py\n|-- sql/\n|   |-- 01_create_tables.sql\n|   |-- 02_joins.sql\n|   |-- 03_aggregations.sql\n|   `-- 04_filters.sql\n|-- airbyte/airbyte_setup.md\n|-- main.py\n`-- requirements.txt"),
    P("Figure 6.1: Project Folder Structure", "Caption"),
    P("6.2 Transformation Implementation", "Section"),
    code('df = df.dropna(subset=["name"])\ndf = df.reset_index(drop=True)\ndf.insert(0, "movie_id", df.index + 1)\n\ndf["budget"] = pd.to_numeric(df["budget"], errors="coerce")\ndf["gross"] = pd.to_numeric(df["gross"], errors="coerce")\ndf["score"] = pd.to_numeric(df["score"], errors="coerce")'),
    P("The transformation produces four tables containing the same number of movie-level records. The common movie_id preserves the relationship between the tables and supports SQL joins."),
    P("6.3 Snowflake Schema", "Section"),
    P("The Snowflake schema SQL creates the MOVIES, RATINGS, FINANCIALS, and PEOPLE tables. The current schema is intentionally simple for an internship project and can later be strengthened with constraints, data types, and staging tables."),
    P("6.4 Pipeline Execution", "Section"),
    code("pip install -r requirements.txt\npython etl/transform.py\npython main.py"),
    PageBreak(),
]

# Chapter 7
story += [
    P("CHAPTER 7: SQL ANALYSIS AND RESULTS", "Chapter"),
    P("7.1 Join Queries", "Section"),
    P("The join queries reconstruct a complete movie view by combining MOVIES, RATINGS, FINANCIALS, and PEOPLE using MOVIE_ID. This demonstrates how normalized tables can be used together without storing all attributes repeatedly in one table."),
    code("SELECT m.NAME, m.GENRE, r.SCORE, r.RATING,\n       f.BUDGET, f.GROSS, p.DIRECTOR\nFROM MOVIES m\nJOIN RATINGS r ON m.MOVIE_ID = r.MOVIE_ID\nJOIN FINANCIALS f ON m.MOVIE_ID = f.MOVIE_ID\nJOIN PEOPLE p ON m.MOVIE_ID = p.MOVIE_ID\nORDER BY r.SCORE DESC\nLIMIT 20;"),
    P("7.2 Aggregation Queries", "Section"),
    P("Aggregation queries calculate average rating and movie count by genre, total budget and gross by year, the number of movies associated with each director, and average runtime by decade. These queries use COUNT, AVG, SUM, ROUND, GROUP BY, and HAVING."),
    code("SELECT m.GENRE,\n       COUNT(*) AS TOTAL_MOVIES,\n       ROUND(AVG(r.SCORE), 2) AS AVG_SCORE\nFROM MOVIES m\nJOIN RATINGS r ON m.MOVIE_ID = r.MOVIE_ID\nGROUP BY m.GENRE\nORDER BY AVG_SCORE DESC;"),
    P("7.3 Filter Queries", "Section"),
    P("Filtering queries identify movies released after 2010 with ratings above 7.5, big-budget movies that earned less than their budget, movies from a selected country and genre, and highly voted R-rated movies."),
    P("7.4 Key Analytical Questions", "Section"),
    table([
        ["Question", "SQL Concept Used"],
        ["Which movies have the highest scores?", "JOIN, ORDER BY, LIMIT"],
        ["Which movies made a profit?", "JOIN, arithmetic expression, WHERE"],
        ["What is the average score per genre?", "AVG, COUNT, GROUP BY"],
        ["Which directors have made the most movies?", "COUNT, GROUP BY, HAVING"],
        ["Which high-budget movies failed commercially?", "WHERE and comparison"],
    ], [3.8 * inch, 2.4 * inch]),
    P("Table 7.1: SQL Analysis Covered in the Project", "Caption"),
    PageBreak(),
]

# Chapter 8
story += [
    P("CHAPTER 8: TESTING AND VALIDATION", "Chapter"),
    P("8.1 File and Schema Validation", "Section"),
    bullet("The raw CSV contains approximately 4,000 movie records."),
    bullet("The processed output contains four CSV files."),
    bullet("Each processed table contains a movie_id column."),
    bullet("The four tables preserve movie-level row relationships."),
    bullet("Column names match the Snowflake schema after loading."),
    P("8.2 Transformation Validation", "Section"),
    bullet("Rows without a movie name are removed."),
    bullet("Numeric fields are converted using pandas to_numeric."),
    bullet("movie_id values are generated after resetting the index."),
    bullet("The data is split without losing the movie-level key."),
    P("8.3 SQL Validation", "Section"),
    P("SQL queries were organized into separate files so that schema creation, joins, aggregations, and filters could be tested independently. The query design uses explicit table aliases and join conditions based on MOVIE_ID."),
    P("8.4 Current Validation Limitations", "Section"),
    P("The repository does not yet include a formal automated test suite or a complete data-quality framework. In a production implementation, assertions and test cases should verify uniqueness, null rules, valid score ranges, referential integrity, and successful load counts."),
    PageBreak(),
]

# Chapter 9
story += [
    P("CHAPTER 9: LEARNING OUTCOMES", "Chapter"),
    P("During the internship, the following practical skills were developed:"),
    bullet("Understanding the difference between raw, transformed, and warehouse data."),
    bullet("Reading CSV files with custom delimiters and character encodings."),
    bullet("Cleaning missing and incorrectly typed values using pandas."),
    bullet("Designing related tables from a denormalized dataset."),
    bullet("Using primary business keys and generated identifiers for joins."),
    bullet("Writing SQL queries with JOIN, WHERE, GROUP BY, HAVING, ORDER BY, and LIMIT."),
    bullet("Using aggregate functions such as SUM, AVG, COUNT, and ROUND."),
    bullet("Understanding cloud warehouse loading through Snowflake."),
    bullet("Documenting an ETL process for reproducibility."),
    P("The most important learning outcome was understanding that SQL analysis becomes more reliable when the data model is designed before queries are written. Separating movie attributes, ratings, financials, and people made the analytical questions clearer and made joins meaningful."),
    PageBreak(),
]

# Chapter 10
story += [
    P("CHAPTER 10: LIMITATIONS AND FUTURE SCOPE", "Chapter"),
    P("10.1 Current Limitations", "Section"),
    bullet("The source dataset is static and the current Airbyte setup uses full refresh."),
    bullet("The pipeline is manually executed and has no scheduler."),
    bullet("Formal automated tests and data quality checks are not yet included."),
    bullet("Snowflake schema constraints and staging-table merge logic can be improved."),
    bullet("The project currently provides SQL analysis but not a visual dashboard."),
    P("10.2 Future Enhancements", "Section"),
    bullet("Add incremental synchronization using an update timestamp."),
    bullet("Use staging tables and MERGE statements to prevent duplicate records."),
    bullet("Add dbt models, tests, and documentation for warehouse transformations."),
    bullet("Schedule the pipeline with Airflow, Prefect, or GitHub Actions."),
    bullet("Add Great Expectations or custom validation checks."),
    bullet("Connect Snowflake to Power BI or Tableau for interactive dashboards."),
    bullet("Add monitoring, structured logs, alerts, and row-count reconciliation."),
    PageBreak(),
]

# Chapter 11
story += [
    P("CHAPTER 11: CONCLUSION", "Chapter"),
    P("The Movie Dataset ETL Pipeline successfully demonstrates an end-to-end data engineering workflow developed during a 45-day SQL-focused internship. A raw movie CSV file was extracted, cleaned, transformed, divided into four related tables, and prepared for loading into Snowflake."),
    P("The SQL component of the project provides practical experience with relational data analysis. Joins combine subject-oriented tables, filters isolate relevant records, and aggregation queries produce summarized business insights. The project therefore connects database concepts with a realistic analytical use case."),
    P("Although the current implementation is primarily an educational and demonstrative pipeline, it provides a strong foundation for a production-grade solution. Incremental loading, automated tests, scheduling, monitoring, and dashboard integration are the natural next steps."),
    P("The internship helped develop a practical understanding of SQL, ETL design, cloud data warehousing, data cleaning, and technical documentation."),
    PageBreak(),
]

# References
story += [
    P("REFERENCES", "Chapter"),
    bullet("Python Documentation: https://docs.python.org/3/"),
    bullet("pandas Documentation: https://pandas.pydata.org/docs/"),
    bullet("Snowflake Documentation: https://docs.snowflake.com/"),
    bullet("Airbyte Documentation: https://docs.airbyte.com/"),
    bullet("Project source files: README.md, etl/, sql/, and airbyte/airbyte_setup.md"),
    Spacer(1, 0.3 * inch),
    P("APPENDIX A: PROJECT FILES", "Section"),
    table([
        ["File", "Purpose"],
        ["main.py", "Runs extraction, transformation, saving, and loading in sequence."],
        ["etl/extract.py", "Reads the raw movie CSV."],
        ["etl/transform.py", "Cleans data and splits it into four tables."],
        ["etl/load.py", "Creates Snowflake tables and loads processed CSV files."],
        ["sql/01_create_tables.sql", "Creates the warehouse tables."],
        ["sql/02_joins.sql", "Contains relational join analysis."],
        ["sql/03_aggregations.sql", "Contains grouped and summarized analysis."],
        ["sql/04_filters.sql", "Contains filtered analytical queries."],
    ], [2.4 * inch, 3.8 * inch]),
]


doc = BaseDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=LEFT,
    rightMargin=RIGHT,
    topMargin=TOP,
    bottomMargin=BOTTOM,
    title="Movie Dataset ETL Pipeline and SQL Analytics - Internship Report",
    author="[STUDENT NAME]",
)
frame = Frame(LEFT, BOTTOM, PAGE_W - LEFT - RIGHT, PAGE_H - TOP - BOTTOM, id="normal")
doc.addPageTemplates([PageTemplate(id="main", frames=frame, onPage=on_page)])
doc.build(story, canvasmaker=NumberedCanvas)
print(OUTPUT)
