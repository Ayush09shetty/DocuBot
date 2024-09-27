import tkinter as tk
from tkinter import filedialog, messagebox
import pdfplumber
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from customtkinter import *
from CTkListbox import *
import mysql.connector
from mysql.connector import Error
import string
import time

# Define important words and their synonyms
important_words = {
    "Hahnemann’s Chronic Diseases": ["Hahnemann’s Chronic Conditions", "Hahnemann’s Chronic Ailments"],
    "C. L. Swift": ["Dr. C. L. Swift", "Swift"],
    "Central New York Homoeopathic Medical Society": ["CNYHM Society", "Central NY Homeo. Med. Society"],
    "Chronic Diseases": ["Persistent Conditions", "Long-term Ailments"],
    "Causes": ["Origins", "Reasons"],
    "Acute": ["Sudden", "Severe"],
    "Death": ["Demise", "Passing"],
    "Organism": ["Body", "Organic Structure"],
    "Remedies": ["Treatments", "Solutions"],
    "Syphilis": ["Venereal Disease", "Pox"],
    "Sycosis": ["Fig-wart Disease", "Molluscum Contagiosum"],
    "Psora": ["Scabies", "Itch"],
    "Miasms": ["Infections", "Pathogens"],
    "Symptoms": ["Indications", "Manifestations"],
    "Homoeopathic treatment": ["Homeopathic Therapy", "Alternative Medicine"],
    "Patients": ["Individuals", "Subjects"],
    "Failures": ["Lapses", "Shortcomings"],
    "Treatment": ["Therapy", "Management"],
    "Views": ["Perspectives", "Opinions"],
    "Hartmann": ["Dr. Hartmann", "Hartmann's"],
    "Introduction": ["Prelude", "Preface"],
    "Psoric eruption": ["Psoriatic Rash", "Skin Outbreak"],
    "Itch": ["Scratchiness", "Pruritus"],
    "Chronic contagion": ["Persistent Infection", "Long-term Transmission"],
    "Transactions": ["Proceedings", "Meetings"],
    "State of New York": ["New York State", "NY"],
    "Psoric miasm": ["Psoric Infection", "Psoric Condition"],
    "Hereditary": ["Inherited", "Genetic"],
    "Morbific miasm": ["Disease-causing Infection", "Pathogenic Condition"],
    "Drunkard’s itch": ["Alcoholic Dermatitis", "Brewer's Itch"],
    "Psoriasis": ["Psoriatic Disease", "Psoriatic Condition"],
    "Eczema": ["Dermatitis", "Skin Irritation"],
    "Doctrine": ["Belief", "Teaching"],
    "Original sin": ["Inherited Sin", "Ancestral Sin"],
    "Pathology": ["Disease Process", "Study of Disease"],
    "Cutaneous affections": ["Skin Disorders", "Dermatological Conditions"],
    "Psoric dyscrasia": ["Psoric Imbalance", "Psoric Disturbance"],
    "Philosophical": ["Thoughtful", "Reflective"],
    "Eradication": ["Elimination", "Removal"],
    "Sin-poisoned race": ["Sin-infected Population", "Corrupted Humanity"],
    "Psoric theory": ["Psoric Hypothesis", "Psoric Concept"],
    "Organs": ["Body Parts", "Anatomy"],
    "Oppression": ["Suppression", "Persecution"],
    "Hypocrisy": ["Deceit", "Insincerity"],
    "DBA Tools": ["DBA Tools", "Database Administration Tools"],
    "Summary": ["Summary"],
    "Practice 2 Overview": ["Practice 2 Overview", "Practice Overview 2"],
    "Managing an Oracle Instance": ["Managing an Oracle Instance"],
    "Objectives": ["Objectives"],
    "Initialization Parameter Files": ["Initialization Parameter Files"],
    "PFILE": ["PFILE"],
    "initSID.ora": ["initSID.ora"],
    "PFILEExample": ["PFILEExample"],
    "SPFILE": ["SPFILE"],
    "spfileSID.ora": ["spfileSID.ora"],
    "Creating an SPFILE": ["Creating an SPFILE"],
    "Oracle Managed Files": ["Oracle Managed Files"],
    "Oracle Managed File Example": ["Oracle Managed File Example"],
    "Starting UP a Database": ["Starting UP a Database"],
    "STARTUP Command": ["STARTUP Command"],
    "The ALTER DATABASE Command": ["The ALTER DATABASE Command"],
    "Opening a Database in Restricted Mode": ["Opening a Database in Restricted Mode"],
    "Opening a Database in Read-Only Mode": ["Opening a Database in Read-Only Mode"],
    "Shutting Down the Database": ["Shutting Down the Database"],
    "Shutdown Options": ["Shutdown Options"],
    "Managing an Instance by Monitoring Diagnostic Files": ["Managing an Instance by Monitoring Diagnostic Files"],
    "Alert Log File": ["Alert Log File"],
    "Background Trace Files": ["Background Trace Files"],
    "User Trace File": ["User Trace File"],
    "Enabling or Disabling User Tracing": ["Enabling or Disabling User Tracing"],
    "Summary 3": ["Summary 3"],
    "Practice 3 Overview": ["Practice 3 Overview", "Practice Overview 3"],
    "Creating a Database": ["Creating a Database"],
    "Objectives 4": ["Objectives 4"],
    "Managing and Organizing a Database": ["Managing and Organizing a Database"],
    "Creation Prerequisites": ["Creation Prerequisites"],
    "Planning Database Files Locations": ["Planning Database Files Locations"],
    "Operating System Environment": ["Operating System Environment"],
    "Using the Database Configuration Assistant": ["Using the Database Configuration Assistant"],
    "Create a Database": ["Create a Database"],
    "Database Information": ["Database Information"],
    "Typical or Custom Install": ["Typical or Custom Install"],
    "Other Parameters": ["Other Parameters"],
    "Complete Database Creation": ["Complete Database Creation"],
    "Creating a Database Manually": ["Creating a Database Manually"],
    "Preparing the Parameter File": ["Preparing the Parameter File"],
    "Creating SPFILE": ["Creating SPFILE"],
    "Starting the Instance": ["Starting the Instance"],
    "Creating the Database": ["Creating the Database"],
    "Creating a Database Using OMF": ["Creating a Database Using OMF"],
    "Troubleshooting": ["Troubleshooting"],
    "After Database Creation": ["After Database Creation"],
    "Summary 4": ["Summary 4"],
    "Data Dictionary Contents and Usage": ["Data Dictionary Contents and Usage"],
    "Objectives 5": ["Objectives 5"],
    "Data Dictionary": ["Data Dictionary"],
    "Data Dictionary Contents": ["Data Dictionary Contents"],
    "How the Data Dictionary Is Used": ["How the Data Dictionary Is Used"],
    "Data Dictionary View Categories": ["Data Dictionary View Categories"],
    "Dynamic Performance Tables": ["Dynamic Performance Tables"],
    "Querying the Data Dictionary and Dynamic Performance Views": ["Querying the Data Dictionary and Dynamic Performance Views"],
    "Data Dictionary Examples": ["Data Dictionary Examples"],
    "Summary 5": ["Summary 5"],
    "Practice 5 Overview": ["Practice 5 Overview", "Practice Overview 5"],
    "Maintaining the Control File": ["Maintaining the Control File"],
    "Objectives 6": ["Objectives 6"],
    "Control File": ["Control File"],
    "Control File Contents": ["Control File Contents"],
    "Multiplexing the Control File Using SPFILE": ["Multiplexing the Control File Using SPFILE"],
    "Multiplexing the Control File Using init.ora": ["Multiplexing the Control File Using init.ora"],
    "Managing Control Files with OMF": ["Managing Control Files with OMF"],
    "Obtaining Control File Information": ["Obtaining Control File Information"],
    "Summary 6": ["Summary 6"],
    "Practice 6 Overview": ["Practice 6 Overview", "Practice Overview 6"],
    "Maintaining Redo Log Files": ["Maintaining Redo Log Files"],
    "Objectives 7": ["Objectives 7"],
    "Using Redo Log Files": ["Using Redo Log Files"],
    "Structure of Redo Log Files": ["Structure of Redo Log Files"],
    "How Redo Logs Work": ["How Redo Logs Work"],
    "Forcing Log Switches and Checkpoints": ["Forcing Log Switches and Checkpoints"],
    "Adding Online Redo Log Groups": ["Adding Online Redo Log Groups"],
    "Adding Online Redo Log Members": ["Adding Online Redo Log Members"],
    "Dropping Online Redo Log Groups": ["Dropping Online Redo Log Groups"],
    "Dropping Online Redo Log Members": ["Dropping Online Redo Log Members"],
    "Clearing, Relocating, or Renaming Online Redo Log Files": ["Clearing, Relocating, or Renaming Online Redo Log Files"],
    "Online Redo Log Configuration": ["Online Redo Log Configuration"],
    "Managing Online Redo Logs with OMF": ["Managing Online Redo Logs with OMF"],
    "Obtaining Group and Member Information": ["Obtaining Group and Member Information"],
    "Archived Redo Log Files": ["Archived Redo Log Files"],
    "Summary 7": ["Summary 7"],
    "Practice 7 Overview": ["Practice 7 Overview", "Practice Overview 7"],
    "Managing Tablespaces and Data files": ["Managing Tablespaces and Data files"],
    "Objectives 8": ["Objectives 8"],
    "Overview 8": ["Overview 8"],
    "Database Storage Hierarchy": ["Database Storage Hierarchy"],
    "SYSTEM and Non-SYSTEM Tablespaces": ["SYSTEM and Non-SYSTEM Tablespaces"],
    "Creating Tablespaces": ["Creating Tablespaces"],
    "Space Management in Tablespaces": ["Space Management in Tablespaces"],
    "Locally Managed Tablespaces": ["Locally Managed Tablespaces"],
    "Dictionary Managed Tablespaces": ["Dictionary Managed Tablespaces"],
    "Changing the Storage Settings": ["Changing the Storage Settings"],
    "Undo Tablespace": ["Undo Tablespace"],
    "Temporary Tablespace": ["Temporary Tablespace"],
    "Default Temporary Tablespace": ["Default Temporary Tablespace"],
    "Restrictions on Default Temporary Tablespace": ["Restrictions on Default Temporary Tablespace"],
    "Offline Status": ["Offline Status"],
    "Read-Only Tablespaces": ["Read-Only Tablespaces"],
    "Dropping Tablespaces": ["Dropping Tablespaces"],
    "Resizing a Tablespace": ["Resizing a Tablespace"],
    "Enabling Automatic Extension of Data Files": ["Enabling Automatic Extension of Data"],
    "database": ["DB", "data repository", "data storage"],
    "query": ["SQL query", "database query", "data retrieval"],
    "backup": ["data backup", "database backup", "data protection"],
    "restore": ["data restoration", "database recovery", "data recovery"],
    "index": ["database index", "data indexing", "search optimization"],
    "performance": ["database performance", "data efficiency", "system optimization"],
    "security": ["database security", "data protection", "access control"],
    "table": ["database table", "data structure", "record set"],
    "query optimization": ["SQL optimization", "database query tuning", "performance improvement"],
    "replication": ["data replication", "database synchronization", "data duplication"],
    "bitmap": ["bitmaps", "bitmap index", "bit array"],
}

i = 0
input_files = []

# Function to replace user query words with dictionary keys
def replace_query_words_with_keys(user_input):
    for key, values in important_words.items():
        for value in values:
            user_input = user_input.replace(value, key)
    return user_input

# Function to check login credentials
def check_login(username, password):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='exampledb',
            user='root',
            password=''
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT password FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            record = cursor.fetchone()
            if record:
                db_password = record[0]
                if db_password == password:
                    return True, "Login successful"
                else:
                    return False, "Login failed: Incorrect password"
            else:
                return False, "Login failed: Username not found"
    except Error as e:
        return False, f"Error: {str(e)}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to handle login button click event
def login():
    email = login_email_entry.get()
    password = login_password_entry.get()
    success, message = check_login(email, password)
    login_error_label.configure(text=message)
    if success:
        login_error_label.configure(text_color="green")
        # Destroy the login window after successful login
        login_window.after(2000, lambda: [login_window.destroy(), start_file_upload()])
    else:
        login_error_label.configure(text_color="red")

# Function to handle file upload process
def start_file_upload():
    root = CTk()
    root.title("Multiple PDF File Upload")
    set_appearance_mode("dark")
    root.geometry("1920x1080")

    browse_button = CTkButton(root, text="Upload PDF Files", command=browse_files, fg_color="#C850C0", hover_color="#4158D0")
    browse_button.pack(pady=10)

    global file_listbox
    file_listbox = CTkListbox(root, width=400, height=350)
    file_listbox.pack(pady=10)
    file_listbox.insert(0, "File Name")

    delete_button = CTkButton(root, text="Delete", command=delete_file, fg_color="#C850C0", hover_color="#4158D0")
    delete_button.pack(pady=10)

    submit_button = CTkButton(root, text="Submit", command=sub, fg_color="#C850C0", hover_color="#4158D0")
    submit_button.pack(pady=10)

    root.mainloop()

# Function to browse and select PDF files
def browse_files():
    global i
    filenames = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if filenames:
        for filename in filenames:
            file_listbox.insert(i+1, filename)
            i += 1
        update_path_file()

# Function to delete selected file
def delete_file():
    selected_index = file_listbox.curselection()
    if selected_index:
        print(selected_index)
        file_listbox.delete(selected_index) 
        update_path_file()

# Function to update the path file
def update_path_file():
    with open("path.txt", "w") as file:
        for index in range(file_listbox.size()):
            file.write(file_listbox.get(index) + "\n")

# Function to convert PDF to text
def pdf_to_text(input_pdf_path, output_text_path):
    with pdfplumber.open(input_pdf_path) as pdf:
        text_content = ""
        for page in pdf.pages:
            text_content += page.extract_text()
            text_content += "\n"  # Add a newline to separate pages

    # Write the extracted text to a text file
    with open(output_text_path, "w", encoding="utf-8") as text_file:
        text_file.write(text_content)

# Function to handle form submission
def sub():
    global i
    input_files.clear()  # Clear the list of input files
    for index in range(1, file_listbox.size()):  # Start from index 1, skipping the header
        input_pdf_path = file_listbox.get(index)
        path = input_pdf_path
        filename_match = re.search(r'[^/\\]*?(?=\.[^.]+$|$)', path)
        if filename_match:
            filename = filename_match.group()
        else:
            print("No filename found in the path.")
        output_text_path = filename + ".txt"
        input_files.append(output_text_path)
        pdf_to_text(input_pdf_path, output_text_path)
    if input_files:
        merge_text_files(input_files)


# Function to merge text files
def merge_text_files(input_files):
    output_file = 'merged_output.txt'  # Output file name
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for input_file in input_files:
            with open(input_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
    messagebox.showinfo("Successful", "You have successfully uploaded the Pdf.")

    # Start the chatbot
    start_chatbot()

# Function to start the chatbot
def start_chatbot():
    chatbot_window = tk.Tk()
    chatbot_window.title("AI Chatbot")
    chatbot_window.geometry("1920x1080")

    main_frame = tk.Frame(chatbot_window, height=1000, width=1000, bg="#1E1E1E", borderwidth=0)  # Set frame background color to dark and remove border
    main_frame.pack()
    chat_history = tk.Text(main_frame, width=100, height=20, bg="#333333", fg="#FFFFFF")
    chat_history.pack(pady=20)

    user_input = tk.Entry(main_frame, width=50, bg="#333333", fg="#FFFFFF")
    user_input.pack(pady=20)

    send_button = tk.Button(main_frame, text="Send", command=lambda: send_message(user_input, chat_history, corpus), bg="#C850C0", fg="#FFFFFF")
    send_button.pack(pady=20)

    # Load corpus from merged_output.txt
    with open("merged_output.txt", "r", encoding="utf-8") as file:
        corpus = learn_from_text(file.read())

    chatbot_window.mainloop()

# Function to send message in chatbot
def send_message(user_input, chat_history, corpus):
    user_text = user_input.get().strip()  # Strip leading and trailing whitespaces
    if user_text:
        user_text = replace_query_words_with_keys(user_text)  # Replace user query words with dictionary keys
        display_message(chat_history, "You: " + user_text)
        response_text = generate_response(user_text, corpus)
        display_message(chat_history, "AI Bot: " + response_text)
    else:
        display_message(chat_history, "AI Bot: Unable to understand your prompt")  # Display "Unable to fetch" if user input is empty

    user_input.delete(0, "end")  # Clear user input field after sending message

# Function to display message in chat history
def display_message(chat_history, message):
    chat_history.insert("end", message + "\n")
    chat_history.see("end")

# Function to learn from text
def learn_from_text(text):
    return text

# Function to generate response in chatbot
def lem_normalize(text):
    return nltk.word_tokenize(text.lower().translate(str.maketrans('', '', string.punctuation)))

def generate_response(user_input, corpus):
    # Remove punctuation from user input
    user_input = user_input.translate(str.maketrans('', '', string.punctuation))

    # Tokenization
    sent_tokens = nltk.sent_tokenize(corpus)

    # TF-IDF Vectorization
    tfidf_vectorizer = TfidfVectorizer(tokenizer=lem_normalize, stop_words='english', token_pattern=None)
    tfidf_matrix = tfidf_vectorizer.fit_transform(sent_tokens)

    # User input processing
    user_input_tfidf = tfidf_vectorizer.transform([user_input])

    # Cosine similarity calculation
    cosine_similarities = cosine_similarity(user_input_tfidf, tfidf_matrix)

    # Fetch indices of sentences with the highest cosine similarities
    top_indices = cosine_similarities.argsort()[0][-5:]
    top_sentences = [sent_tokens[i] for i in reversed(top_indices)]

    # Filter out sentences with question marks
    top_sentences = [sentence for sentence in top_sentences if '?' not in sentence]

    if not top_sentences or max(cosine_similarities[0]) < 0.1:  # Set a threshold for cosine similarity
        return "Unable to understand your prompt"
    else:
        return " ".join(top_sentences)

# Function to create login page
def login_page():
    # Create the main window for login
    if 'signup_window' in globals():
        signup_window.destroy()
    global login_window
    login_window = CTk()
    login_window.title("Login Page")
    login_window.geometry("1920x1080")
    set_appearance_mode("dark")

    login_frame = CTkFrame(master=login_window, width=1000, height=500, bg_color="transparent")
    login_frame.pack(anchor="center", pady=200)

    # Welcome label
    custom_font = ("Times New Roman", 32)
    label = CTkLabel(master=login_frame, text="Welcome Back!", fg_color="transparent", font=custom_font)
    label.pack(pady=(30, 20))

    # Email Textbox
    global login_email_entry
    login_email_entry = CTkEntry(master=login_frame, width=220, placeholder_text="Email")
    login_email_entry.pack(padx=(50,), pady=(5,0))

    # Password Textbox
    global login_password_entry
    login_password_entry = CTkEntry(master=login_frame, width=220, show="*", placeholder_text="Password")
    login_password_entry.pack(pady=(14,0))

    # Error Label for displaying login messages
    global login_error_label
    login_error_label = CTkLabel(master=login_frame, text="", width=220, font=("", 15))
    login_error_label.pack(pady=(10,5))
    login_error_label.configure(text_color="red")

    # Login Button
    login_btn = CTkButton(master=login_frame, text="Login", corner_radius=15, fg_color="#C850C0", hover_color="#4158D0", width=100, command=login)
    login_btn.pack(pady=(10, 10))

    # Sign Up Button
    signup_btn = CTkButton(master=login_frame, text="Don't have an account? Sign Up here", text_color="#0080FE", fg_color="transparent", command=signup_page)
    signup_btn.pack(pady=(10, 20))

    login_window.mainloop()

# Function to create signup page
def signup_page():
    # Create the main window for signup
    global signup_window
    signup_window = CTk()
    signup_window.title("Sign Up Page")
    signup_window.geometry("1920x1080")
    set_appearance_mode("dark")

    signup_frame = CTkFrame(master=signup_window, width=1000, height=500, bg_color="transparent")
    signup_frame.pack(anchor="center", pady=200)

    # Welcome label
    custom_font = ("Times New Roman", 32)
    label = CTkLabel(master=signup_frame, text="Sign Up Here!", fg_color="transparent", font=custom_font)
    label.pack(pady=(30, 20))

    # Email Textbox
    global signup_email_entry
    signup_email_entry = CTkEntry(master=signup_frame, width=220, placeholder_text="Email")
    signup_email_entry.pack(padx=(50,), pady=(5,0))

    # Password Textbox
    global signup_password_entry
    signup_password_entry = CTkEntry(master=signup_frame, width=220, show="*", placeholder_text="Password")
    signup_password_entry.pack(pady=(14,0))

    # Error Label for displaying signup messages
    global signup_error_label
    signup_error_label = CTkLabel(master=signup_frame, text="", width=220, font=("", 15))
    signup_error_label.pack(pady=(10,5))
    signup_error_label.configure(text_color="red")

    # Signup Button
    signup_btn = CTkButton(master=signup_frame, text="Sign Up", corner_radius=15, fg_color="#C850C0", hover_color="#4158D0", width=100, command=signup)
    signup_btn.pack(pady=(10, 10))

    # Login Button
    login_btn = CTkButton(master=signup_frame, text="Already have an account? Login here", text_color="#0080FE", fg_color="transparent", command=login_page)
    login_btn.pack(pady=(10, 20))

    signup_window.mainloop()

# Function to add a new user to the database
def add_user(username, password):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            database='exampledb',
            user='root',
            password=''
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Check if the username already exists
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            record = cursor.fetchone()
            if record:
                return False, "Username already exists"
            else:
                # Insert new user into the database
                insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(insert_query, (username, password))
                connection.commit()
                return True, "User added successfully"
    except Error as e:
        return False, f"Error: {str(e)}"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to handle signup button click event
def signup():
    email = signup_email_entry.get()
    password = signup_password_entry.get()
    success, message = add_user(email, password)
    signup_error_label.configure(text=message)
    if success:
        signup_error_label.configure(text_color="green")
    else:
        signup_error_label.configure(text_color="red")

# Start with the signup page
signup_page()
