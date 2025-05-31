Here are some sample questions you might ask based on the schema, along with the corresponding SQL queries:

---

### 1. **Question:**

_What are the albums available in the database?_

**SQL Query:**

```sql
SELECT Title FROM Album;
```

---

### 2. **Question:**

_What is the name of the artist for the album "For Those About To Rock We Salute You"?_

**SQL Query:**

```sql
SELECT a.Name
FROM Artist a
JOIN Album al ON a.ArtistId = al.ArtistId
WHERE al.Title = 'For Those About To Rock We Salute You';
```

---

### 3. **Question:**

_What is the contact information of the customer with CustomerId 1?_

**SQL Query:**

```sql
SELECT FirstName, LastName, Email, Phone, Address, City, Country
FROM Customer
WHERE CustomerId = 1;
```

---

### 4. **Question:**

_Which employee is responsible for customer support?_

**SQL Query:**

```sql
SELECT e.FirstName, e.LastName, e.Title
FROM Employee e
JOIN Customer c ON e.EmployeeId = c.SupportRepId;
```

---

### 5. **Question:**

_How much was the total for the invoice with InvoiceId 1?_

**SQL Query:**

```sql
SELECT Total
FROM Invoice
WHERE InvoiceId = 1;
```

---

### 6. **Question:**

_Which genre does the track "For Those About To Rock (We Salute You)" belong to?_

**SQL Query:**

```sql
SELECT g.Name AS Genre
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
WHERE t.Name = 'For Those About To Rock (We Salute You)';
```

---

### 7. **Question:**

_What is the total number of tracks in the "Music" playlist?_

**SQL Query:**

```sql
SELECT COUNT(pt.TrackId)
FROM PlaylistTrack pt
JOIN Playlist p ON pt.PlaylistId = p.PlaylistId
WHERE p.Name = 'Music';
```

---

### 8. **Question:**

_What is the unit price of the track "Balls to the Wall"?_

**SQL Query:**

```sql
SELECT UnitPrice
FROM Track
WHERE Name = 'Balls to the Wall';
```

---

### 9. **Question:**

_Which customers are from Germany?_

**SQL Query:**

```sql
SELECT FirstName, LastName, Email, City, Country
FROM Customer
WHERE Country = 'Germany';
```

---

### 10. **Question:**

_What are the names of the employees who report to "Andrew Adams"?_

**SQL Query:**

```sql
SELECT FirstName, LastName
FROM Employee
WHERE ReportsTo = (SELECT EmployeeId FROM Employee WHERE FirstName = 'Andrew' AND LastName = 'Adams');
```

---

### 11. **Question:**

_Which tracks are available in the playlist "Movies"?_

**SQL Query:**

```sql
SELECT t.Name
FROM PlaylistTrack pt
JOIN Playlist p ON pt.PlaylistId = p.PlaylistId
JOIN Track t ON pt.TrackId = t.TrackId
WHERE p.Name = 'Movies';
```

---

### 12. **Question:**

_What is the name of the media type for track 1?_

**SQL Query:**

```sql
SELECT m.Name AS MediaType
FROM MediaType m
JOIN Track t ON m.MediaTypeId = t.MediaTypeId
WHERE t.TrackId = 1;
```

---

Plot Based Questions:

1. Plot the most popular top 10 genre (by total sales) for each country, with their count
2. Plot the total number of tracks by genre.
3. Visualize the total invoice amount by country.
4. Visualize the number of tracks per album using a bar chart.
5. Create a bar chart of total sales (invoice total) per employee.
6. Plot the top 10 most expensive tracks with Track Name
