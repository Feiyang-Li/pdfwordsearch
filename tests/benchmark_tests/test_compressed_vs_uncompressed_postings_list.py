from pathlib import Path

import matplotlib.pyplot as plt
import time
from pympler import asizeof
from pdfwordsearch.data_structures.compressed_postings_list import (
    CompressedPostingsList,
)
from pdfwordsearch.data_structures.postings_list import PostingsList
from tests.test_files import chiropterans_pdf

current_dir = Path(__file__).parent

def test_memory_usage(chiropterans_pdf):
    cpl = CompressedPostingsList(chiropterans_pdf)
    upl = PostingsList(chiropterans_pdf)

    cpl_size = asizeof.asizeof(cpl) / 1000
    upl_size = asizeof.asizeof(upl) / 1000

    plt.bar(
        ["Uncompressed Postings List", "Compressed Postings List"], [upl_size, cpl_size]
    )
    plt.title("Uncompressed vs Compressed Postings List Memory Usage")
    plt.xlabel("Postings List")
    plt.ylabel("Memory Usage (MB)")
    plt.savefig(current_dir.joinpath("Memory Usage.png"))
    plt.close()


# Create graphs comparing compressed vs uncompressed postings list performance
def test_c_vs_u_large(chiropterans_pdf):
    queries = [
        "bat",
        "the bat has large wings",
        "origami teriyaki",
        "chiroptera is an order",
        "family",
        "flower bats",
        "habitats",
        "Bats are the second largest order of mammals after rodents, making up about of all mammal species worldwide",
        "The suborders are further subdivided into clades and families, with Yangochiroptera containing fourteen families grouped into three superfamilies",
    ]

    cpl = CompressedPostingsList(chiropterans_pdf)
    upl = PostingsList(chiropterans_pdf)

    cpl_times = []
    upl_times = []

    for query in queries:
        start = time.time()
        cpl.execute_query(query)
        end = time.time()
        cpl_times.append(end - start)

        start = time.time()
        upl.execute_query(query)
        end = time.time()
        upl_times.append(end - start)

    cpl_avg = sum(cpl_times) / len(cpl_times)
    upl_avg = sum(upl_times) / len(upl_times)

    plt.title("Uncompressed vs Compressed Postings List Query Performance")
    plt.xlabel("Posting Lists")
    plt.ylabel("Average Time (s)")

    plt.bar(
        ["Uncompressed Postings List", "Compressed Postings List"], [upl_avg, cpl_avg]
    )
    plt.savefig(
        current_dir.joinpath("Uncompressed vs Compressed Postings List Performance.png")
    )
    plt.close()
