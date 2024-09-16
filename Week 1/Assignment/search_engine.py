import os

# Function to index both titles and document content
def index_documents(doc_folder):
    index = {}  # Inverted index for content search
    doc_titles = {}  # Store document titles and their content

    for filename in os.listdir(doc_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(doc_folder, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                title = filename.split('.')[0]  # Treat filename as the title
                doc_titles[title] = content  # Store the title and content
                
                # Tokenize the document content
                words = content.lower().split()
                for word in words:
                    if word not in index:
                        index[word] = []
                    index[word].append(title)  # Map words to titles
    return index, doc_titles

# Function for content search
def search_by_content(query, index):
    query = query.lower().split()
    results = set()
    
    for word in query:
        if word in index:
            results.update(index[word])
    
    return results

# Function for title search
def search_by_title(query, doc_titles):
    query = query.lower()
    results = []
    
    for title in doc_titles.keys():
        if query in title.lower():  # Match the title
            results.append(title)
    
    return results

# Function to display results
def display_results(results, doc_titles):
    if not results:
        print("No documents found.")
    else:
        for title in results:
            print(f"Title: {title}")
            print(f"Snippet: {doc_titles[title][:200]}...")  # Display first 200 characters of content

if __name__ == "__main__":
    # Index the documents
    doc_folder = "documents/"
    index, doc_titles = index_documents(doc_folder)
    
    # Ask the user how they want to search
    search_type = input("Search by (1) Title or (2) Content? Enter 1 or 2: ")
    
    if search_type == "1":
        # Search by title
        query = input("Enter your search query (Title): ")
        results = search_by_title(query, doc_titles)
    elif search_type == "2":
        # Search by content
        query = input("Enter your search query (Content): ")
        results = search_by_content(query, index)
    else:
        print("Invalid choice.")
        results = []
    
    # Display the search results
    display_results(results, doc_titles)


