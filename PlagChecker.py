import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary resources
nltk.download('punkt', download_dir='.\\venv\\nltk_data')

def calculate_similarity(block1, block2):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([block1, block2])
    similarity_score = cosine_similarity(tfidf_matrix)
    return similarity_score[0, 1]

def clean_code(code_snippet):
    # Preprocess code by splitting lines, converting to lowercase, and removing punctuation
    code_lines = code_snippet.splitlines()
    cleaned_lines = []
    for line in code_lines:
        line = line.strip().lower()
        line = line.translate(str.maketrans('', '', string.punctuation))
        if line:  # Add only non-empty lines
            cleaned_lines.append(line)
    return cleaned_lines

def assess_plagiarism(source_code_blocks, target_code_blocks):
    cumulative_similarity = 0.0
    matched_segments = []

    for source_block in source_code_blocks:
        highest_similarity = 0.0
        best_matched_block = None
        
        for target_block in target_code_blocks:
            similarity = calculate_similarity(source_block, target_block)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_matched_block = target_block
        
        matched_segments.append((source_block, best_matched_block, highest_similarity))
        cumulative_similarity += highest_similarity

    # Compute the average similarity as the plagiarism score
    average_similarity = cumulative_similarity / len(source_code_blocks) if source_code_blocks else 0
    return average_similarity, matched_segments

# Example execution
source_code_example = """
for target_segment in target_segments:
            similarity = compute_similarity(source_segment, target_segment)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = target_segment
        
        matches.append((source_segment, best_match, best_similarity))
        total_similarity += best_similarity
"""

target_code_example = """
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(code1, code2):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([code1, code2])
    return cosine_similarity(tfidf_matrix)[0, 1]
"""

source_code_blocks = clean_code(source_code_example)
target_code_blocks = clean_code(target_code_example)

print("Source Code Blocks:", source_code_blocks)
print("Target Code Blocks:", target_code_blocks)

# Compute the plagiarism score
plagiarism_rating, matches = assess_plagiarism(source_code_blocks, target_code_blocks)

print(f"Plagiarism Score: {plagiarism_rating:.2f}\n")

# Display the comparison results
for source_block, target_block, similarity in matches:
    print(f"Source Block: '{source_block}'")
    print(f"Best Match in Target: '{target_block}'")
    print(f"Similarity Score: {similarity:.2f}\n")
