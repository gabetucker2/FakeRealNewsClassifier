###########################################
# imports
###########################################

# import functions from helper scripts
import debug
import params
import funcs

# import libraries
import os

import kagglehub
import pandas as pd
import random

import pyspark
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, LongType, DoubleType, StringType

###########################################
debug.log.section(f"DOWNLOADING DATA")
# download data and give an overview of it
###########################################

# Download latest version to csv
path = kagglehub.dataset_download("clmentbisaillon/fake-and-real-news-dataset")
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

if params.debugSection_download:

    # Print information section
    debug.log.downloading(f"Path to dataset files: {path}")
    debug.log.downloading(f"CSV files found: {csv_files}")

    for csv in csv_files:
        
        debug.log.header(f"Overview of {csv}")

        debug.log.indent_level += 1

        df = pd.read_csv(os.path.join(path, csv))
        
        debug.log.downloading(f"Columns: {df.columns.tolist()}")
        debug.log.downloading(f"Num rows: {len(df)}")

        debug.log.lineBreak()

        debug.log.downloading(f"Previewing first {params.numRowsToManuallyVerify} rows:")

        debug.log.indent_level += 1

        for i in range(params.numRowsToManuallyVerify):

            row = df.iloc[i]
            debug.log.downloading(f"Article `{row[df.columns[0]]}`")

            debug.log.indent_level += 1
            for col in df.columns[1:]:
                value = row[col]
                if col == "text" and isinstance(value, str):
                    value = value[:params.numPreviewChars] + ("..." if len(value) > params.numPreviewChars else "")
                debug.log.downloading(f"{col}: {value}")
            debug.log.indent_level -= 1

        debug.log.indent_level -= 1

        debug.log.lineBreak()

        debug.log.indent_level -= 1

###########################################
debug.log.section(f"PREPROCESSING DATA")
# pack data into dimensional vectors
###########################################

# Unified list of article records as dicts (struct-like)
articles = []

# Iterate through files again to populate the list
for csv in csv_files:

    df = pd.read_csv(os.path.join(path, csv))

    for _, row in df.iterrows():
        text = row.get('text', "")
        title = row.get('title', "")
        subject = row.get('subject', "")
        date_str = row.get('date', "")

        # Word count and avg word length
        words = text.split()
        word_count = len(words)
        avg_word_len = sum(len(w) for w in words) / word_count if word_count else 0

        weekday_int = funcs.monthStrToWeekdayNum(date_str)

        if weekday_int == -1:
            debug.log.warning(f"Invalid date {date_str}, skipping article")
        else:
            # Append structured article record
            articles.append({
                "trueNotFake": (csv == "True.csv"),
                "word_count": word_count,
                "avg_word_len": float(avg_word_len),
                "title": str(title),
                "subject": str(subject),
                "text": str(text),
                "weekday": weekday_int
            })

# Shuffle article order
random.shuffle(articles)

# if params.debugSection_preprocessing:
#     debug.log.preprocessing([article["weekday"] for article in articles])

    # print(article_wordCount)
    # print(article_avgWordLen)
    # print(article_titles)
    # print(article_subjects)
    # print(article_texts)
    # print(article_weekdays)
