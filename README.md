# applied-ml-db-comparison
Comparative analysis of machine learning algorithms and database systems with applications to health data.

If you’re reading this as part of my application:
thanks for checking it out :)

Comparative Analysis of Machine Learning Algorithms and Database Systems  
**Random Forest vs K-Means | PostgreSQL vs MongoDB**

Hi there! My name is Yassine!
This project started as my final for UCLA Extension’s *Introduction to Data Science*, and then I kept going because I got genuinely bit with a passion for learning about algorithms which led me to really investing myself in the question:

> **How do you choose the right algorithm and the right database for real-world data problems (especially in healthcare)?**

So this repo is my attempt to answer that in a way that’s technical but readable, and, most importantly, visual because charts > walls of text, always, forever.  

---

## 1. What did I compare

### Machine Learning
- **Random Forest (supervised)**  
  → good when you *have labels* and want predictions  
- **K-Means (unsupervised)**  
  → good when you *don’t have labels* and want to find structure  

### Databases
- **PostgreSQL (SQL / relational)**  
  → great for structured, relational data and complex queries  
- **MongoDB (NoSQL / document-based)**  
  → great for flexible schemas and massive scale  

---

## What I included in this repository

- `algorithm_code_samples.py`  
  → a (hopefully) runnable demo of Random Forest vs K-Means  
  → shows training time, accuracy, silhouette score, etc...  

- `database_code_samples.py`  
  → example PostgreSQL and MongoDB schemas + queries  
  → plus small comparison tables for scalability and queries

- `Comprehensive_Visualizations.png`  
  → charts comparing:
    - accuracy vs speed  
    - scalability  
    - query performance  
    - interpretability  

- `Detailed_Comparison_Table.png`  
  → side-by-side feature matrix for all four technologies  

---

## Main takeaways/findings (very plainly) (you learn more every day!)

### Random Forest is good when:
- you have labeled outcomes (diagnosis, risk, yes/no)  
- accuracy matters more than speed  
- you want feature importance as a starting point for interpretation  

### K-Means is good when:
- you *don’t* have labels  
- you’re exploring patterns (like patient groups)  
- you want something fast and easy to explain  

---

### PostgreSQL is good when:
- your data has clear relationships (patients → visits → labs)  
- consistency really matters  
- you’re doing heavy analytics with joins  

### MongoDB is good when:
- your data structure changes a lot  
- you’re writing tons of data (logs, sensors, events)  
- horizontal scaling is a must  

---

## Why this matters for health data

As I've come to learn, healthcare data is messy:
- can be structured (EHR tables)  
- mostly unstructured (notes, sensor data)  
- scales vary wildly 

So in practice:
- supervised + unsupervised ML often get used together  
- SQL + NoSQL often live in the same system  
- tool choice should depend on the problem, not the hype  

This project was, for me, my way of learning how to reason about those choices instead of just memorizing tools. It's about finding my "why".

---

## Tools I used

- Python (pandas, numpy, scikit-learn)  
- matplotlib / seaborn  
- PostgreSQL (SQL)  
- MongoDB (NoSQL)  

---

## How to run (if you feel so inclined)

If you want to run the demos locally:

```bash
pip install numpy pandas scikit-learn matplotlib seaborn
python algorithm_code_samples.py
python database_code_samples.py
