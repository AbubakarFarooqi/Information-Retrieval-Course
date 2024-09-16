import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

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

# Function to display results in a scrolled text box
def display_results(results, doc_titles, text_widget):
    text_widget.delete(1.0, tk.END)  # Clear previous results
    if not results:
        text_widget.insert(tk.END, "No documents found.\n")
    else:
        for title in results:
            text_widget.insert(tk.END, f"Title: {title}\n")
            text_widget.insert(tk.END, f"Snippet: {doc_titles[title][:200]}...\n\n")  # Display first 200 characters

# Search button functionality
def on_search():
    query = query_entry.get()
    if search_type.get() == "title":
        results = search_by_title(query, doc_titles)
    else:
        results = search_by_content(query, index)
    
    display_results(results, doc_titles, result_text)

# Tkinter GUI setup
root = tk.Tk()
root.title("Simple Document Search Engine")
root.geometry("600x400")

# Search type selection
search_type = tk.StringVar(value="title")

tk.Label(root, text="Search Type:").pack(pady=5)
tk.Radiobutton(root, text="Title", variable=search_type, value="title").pack()
tk.Radiobutton(root, text="Content", variable=search_type, value="content").pack()

# Query input
tk.Label(root, text="Enter your search query:").pack(pady=5)
query_entry = tk.Entry(root, width=50) # TextBox
query_entry.pack(pady=5)

# Search button
search_button = tk.Button(root, text="Search", command=on_search)
search_button.pack(pady=10)

# Results display
result_text = scrolledtext.ScrolledText(root, height=10, width=70)
result_text.pack(pady=10)

# Index the documents before starting the search
doc_folder = "documents/"
index, doc_titles = index_documents(doc_folder)

# Run the Tkinter event loop
root.mainloop()
