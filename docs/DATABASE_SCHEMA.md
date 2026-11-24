\# Database Schema Documentation

\## Tennis Sports Analytics



\*\*Database Name:\*\* `tennis\_analytics`  

\*\*Database Engine:\*\* MySQL 8.0



\## 1. Overview



The database stores structured tennis reference information and doubles competitor rankings retrieved from SportRadar APIs.



It contains six tables:



1\. categories

2\. competitions

3\. complexes

4\. venues

5\. competitors

6\. competitor\_rankings



\## 2. Entity Relationships



```text

categories

&#x20;   |

&#x20;   | 1-to-many

&#x20;   |

competitions

&#x20;   |

&#x20;   | parent\_id (self-reference)

&#x20;   |

&#x20;   +----------------



complexes

&#x20;   |

&#x20;   | 1-to-many

&#x20;   |

venues



competitors

&#x20;   |

&#x20;   | 1-to-many

&#x20;   |

competitor\_rankings

```



\## 3. Table Structures



\### 3.1 categories



Stores competition categories.



| Column | Data Type | Constraint |

|---|---|---|

| category\_id | VARCHAR(50) | Primary Key |

| category\_name | VARCHAR(100) | NOT NULL |



\### 3.2 competitions



Stores tennis competition information.



| Column | Data Type | Constraint |

|---|---|---|

| competition\_id | VARCHAR(50) | Primary Key |

| competition\_name | VARCHAR(100) | NOT NULL |

| parent\_id | VARCHAR(50) | NULL allowed |

| type | VARCHAR(20) | NOT NULL |

| gender | VARCHAR(10) | NOT NULL |

| category\_id | VARCHAR(50) | Foreign Key |



Relationship:

\- `category\_id` references `categories.category\_id`.

\- `parent\_id` stores the parent competition identifier where available.



Indexes:

\- `idx\_competitions\_category`

\- `idx\_competitions\_parent`



\### 3.3 complexes



Stores sports complex information.



| Column | Data Type | Constraint |

|---|---|---|

| complex\_id | VARCHAR(50) | Primary Key |

| complex\_name | VARCHAR(100) | NOT NULL |



\### 3.4 venues



Stores venue information associated with complexes.



| Column | Data Type | Constraint |

|---|---|---|

| venue\_id | VARCHAR(50) | Primary Key |

| venue\_name | VARCHAR(100) | NOT NULL |

| city\_name | VARCHAR(100) | NOT NULL |

| country\_name | VARCHAR(100) | NOT NULL |

| country\_code | CHAR(3) | NOT NULL |

| timezone | VARCHAR(100) | NOT NULL |

| complex\_id | VARCHAR(50) | Foreign Key |



Relationship:

\- `complex\_id` references `complexes.complex\_id`.



Index:

\- `idx\_venues\_complex`



\### 3.5 competitors



Stores competitor details.



| Column | Data Type | Constraint |

|---|---|---|

| competitor\_id | VARCHAR(50) | Primary Key |

| name | VARCHAR(150) | NOT NULL |

| country | VARCHAR(100) | NULL allowed |

| country\_code | CHAR(3) | NULL allowed |

| abbreviation | VARCHAR(10) | NULL allowed |



\### 3.6 competitor\_rankings



Stores competitor ranking information.



| Column | Data Type | Constraint |

|---|---|---|

| rank\_id | INT | Primary Key, AUTO\_INCREMENT |

| competitor\_id | VARCHAR(50) | Foreign Key |

| competitor\_name | VARCHAR(150) | NOT NULL |

| country | VARCHAR(100) | NULL allowed |

| country\_code | CHAR(3) | NULL allowed |

| rank | INT | NOT NULL |

| movement | INT | NOT NULL, DEFAULT 0 |

| points | INT | NOT NULL, DEFAULT 0 |

| competitions\_played | INT | NOT NULL, DEFAULT 0 |

| ranking\_date | DATE | NULL allowed |



Relationship:

\- `competitor\_id` references `competitors.competitor\_id`.



Indexes:

\- `idx\_rankings\_rank`

\- `fk\_rankings\_competitor`



\## 4. Relationships Summary



| Parent Table | Child Table | Relationship |

|---|---|---|

| categories | competitions | One-to-Many |

| complexes | venues | One-to-Many |

| competitors | competitor\_rankings | One-to-Many |

| competitions | competitions | Parent-Child reference |



Foreign keys maintain referential integrity between related records.



\## 5. Database Indexing



Indexes are implemented on frequently queried relationship and ranking fields:



\- Competition category

\- Competition parent

\- Venue complex

\- Competitor ranking

\- Ranking competitor foreign key



These indexes support filtering, joins and analytical queries.



\## 6. Data Population



Data is retrieved through the following SportRadar API feeds:



| API Feed | Database Tables |

|---|---|

| Competitions API | categories, competitions |

| Complexes API | complexes, venues |

| Doubles Competitor Rankings API | competitors, competitor\_rankings |



\## 7. Verified Database Snapshot



As verified on November 24, 2026:



| Table | Records |

|---|---:|

| categories | 18 |

| competitions | 6,743 |

| complexes | 789 |

| venues | 4,200 |

| competitors | 1,000 |

| competitor\_rankings | 1,000 |

| \*\*Total\*\* | \*\*13,750\*\* |



\## 8. Database Backup



A JSON backup containing all six tables was created before removing sample data.



The cleanup operation uses transactions and rollback handling to protect database consistency.



\## 9. SQL Files



The `sql/` directory contains:



\- `schema.sql` — database table definitions and relationships.

\- `analytics\_queries.sql` — analytical SQL queries.

\- `load\_sample\_data.sql` — sample dataset for development and testing.



For the API-only production dataset, use the SportRadar synchronization script instead of loading sample data.

