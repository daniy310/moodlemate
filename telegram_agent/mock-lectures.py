from mongo_handler import MongoHandler

# Initialize MongoHandler for the lectures collection
lectures_handler = MongoHandler("lectures")

# Sample data for two courses: CSIT110 and CSIT115
courses = [
    {
        "course_id": "CSIT110 (Introduction to Python)",
        "lectures": [
            {
                "lecture_title": "Introduction to Python",
                "lecture_id": "1",
                "lecture_text": "In this introductory lecture, we will cover the basics of the Python programming language. Python is a high-level, interpreted programming language that is easy to learn and versatile for many different applications. We will discuss the fundamental concepts of Python, including syntax, variables, data types, operators, and control structures such as loops and conditionals. By the end of this lecture, you will understand how Python syntax works and how to write simple Python programs that perform basic computations."
            },
            {
                "lecture_title": "Control Flow",
                "lecture_id": "2",
                "lecture_text": "Control flow is an essential concept in any programming language. In this lecture, we will dive deeper into Python's control flow mechanisms, including conditional statements like 'if', 'else', and 'elif', which help you execute specific code blocks based on conditions. We will also explore Python's looping structures, such as 'for' loops and 'while' loops, that allow repetitive execution of code. We will examine examples of each control flow construct and learn how to create more complex decision-making logic and loops in Python programs."
            },
            {
                "lecture_title": "Data Structures",
                "lecture_id": "3",
                "lecture_text": "Data structures are a fundamental part of programming, as they enable us to organize, store, and manipulate data efficiently. In this lecture, we will explore Python's built-in data structures, including lists, tuples, sets, and dictionaries. We will discuss the characteristics and use cases for each data structure, and demonstrate how to create, access, and modify them. Additionally, we will cover operations such as indexing, slicing, and looping through these data structures, helping you understand how to handle different types of data in Python."
            },
            {
                "lecture_title": "File I/O",
                "lecture_id": "4",
                "lecture_text": "File input/output (I/O) is an essential aspect of any programming language that allows you to read from and write to external files. In this lecture, we will cover Python's built-in methods for working with files. We will demonstrate how to open, read, and write to text files using Python, and discuss how to handle file exceptions. You will also learn how to read files line by line, how to append to existing files, and how to close files properly. This lecture will help you work with external data sources effectively and automate repetitive tasks involving files."
            },
            {
                "lecture_title": "Libraries and Modules",
                "lecture_id": "5",
                "lecture_text": "Python provides a vast collection of libraries and modules that allow you to perform specialized tasks without needing to write all the code from scratch. In this lecture, we will introduce you to Python's standard library and demonstrate how to import and use built-in modules. We will also discuss how to create your own modules to encapsulate functionality and reuse code across different programs. This lecture will teach you the importance of modular programming and how to use Python's libraries to work with mathematical functions, file operations, and more."
            }
        ]
    },
    {
        "course_id": "CSIT115 (Databases)",
        "lectures": [
            {
                "lecture_title": "Introduction to Databases",
                "lecture_id": "1",
                "lecture_text": "This lecture will introduce you to the concept of databases and their importance in the modern world. Databases are systems used to store, manage, and retrieve data efficiently. We will explore the basics of relational databases, including tables, rows, and columns, as well as the concept of a primary key. Additionally, we will look into the differences between relational and non-relational databases, and the advantages of using databases over traditional file systems. By the end of this lecture, you will have a foundational understanding of how databases work and why they are crucial for managing large sets of data."
            },
            {
                "lecture_title": "SQL Basics",
                "lecture_id": "2",
                "lecture_text": "SQL (Structured Query Language) is the standard language used to interact with relational databases. In this lecture, we will cover the basics of SQL, starting with simple SELECT queries to retrieve data from a database. We will discuss how to filter results using WHERE clauses, how to sort data with ORDER BY, and how to limit results with the LIMIT keyword. Additionally, we will introduce other basic SQL operations like INSERT, UPDATE, and DELETE, which allow you to modify the data stored in a database. This lecture will give you the essential tools to start working with databases using SQL."
            },
            {
                "lecture_title": "Normalization",
                "lecture_id": "3",
                "lecture_text": "Normalization is a critical concept in database design that helps eliminate redundancy and ensure data integrity. In this lecture, we will explain the process of normalization and introduce the different normal forms (1NF, 2NF, 3NF) that are used to design well-structured relational databases. We will show how to apply normalization to real-world examples and identify when a database schema needs to be normalized. By the end of this lecture, you will understand the benefits of normalization, including reducing the risk of data anomalies and improving database performance."
            },
            {
                "lecture_title": "Database Design",
                "lecture_id": "4",
                "lecture_text": "Database design is a crucial step in creating efficient and effective databases. In this lecture, we will cover the principles of designing databases, starting with the creation of an Entity-Relationship (ER) diagram. We will learn how to translate real-world scenarios into ER models, identify entities, relationships, and attributes, and define the keys needed to ensure data integrity. Additionally, we will discuss the process of converting an ER diagram into a relational schema that can be implemented in a relational database management system (RDBMS). This lecture will provide you with the knowledge to design your own databases for a variety of applications."
            },
            {
                "lecture_title": "Advanced SQL Queries",
                "lecture_id": "5",
                "lecture_text": "In this advanced SQL lecture, we will explore more complex querying techniques to manipulate and analyze data in a relational database. We will cover SQL joins (INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN) to combine data from multiple tables. Additionally, we will discuss GROUP BY, HAVING, and aggregate functions (COUNT, AVG, SUM, MIN, MAX) to perform data analysis and generate summary reports. We will also look into subqueries and nested queries, which are useful for solving more complex problems. By the end of this lecture, you will be able to write advanced SQL queries to handle real-world data analysis tasks."
            }
        ]
    }
]

def populate_lectures():
    """Populate the MongoDB lectures collection with mock data."""
    for course in courses:
        course_id = course["course_id"]
        for lecture in course["lectures"]:
            # Create a dictionary for each lecture and insert it into MongoDB
            lecture_data = {
                "course_id": course_id,
                "lecture_title": lecture["lecture_title"],
                "lecture_id": lecture["lecture_id"],
                "lecture_text": lecture["lecture_text"]
            }

            # Save the lecture into the database
            lectures_handler.save(lecture_data)
            print(f"Added lecture: {lecture_data['lecture_title']} for course: {course_id}")

if __name__ == "__main__":
    # Run the population script
    populate_lectures()
    print("🎉 Lectures database populated successfully!")
