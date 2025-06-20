def few_shot_examples():
	example_scenarios = """
            Example Scenarios:

            1. Find the total number of albums by each artist.
            Query:
            SELECT a.Name AS Artist, COUNT(al.AlbumId) AS TotalAlbums
                FROM Artist a
                JOIN Album al ON a.ArtistId = al.ArtistId
                GROUP BY a.Name
                LIMIT 10;

            2. Find the most popular track based on the quantity sold.
            Query:
            SELECT t.Name AS Track, SUM(il.Quantity) AS TotalSales
                FROM Track t
                JOIN InvoiceLine il ON t.TrackId = il.TrackId
                GROUP BY t.Name
                ORDER BY TotalSales DESC
                LIMIT 1;

            3. Get the invoice details for a specific customer (e.g., CustomerId = 2).
            Query:
            SELECT i.InvoiceId, i.InvoiceDate, i.Total
                FROM Invoice i
                WHERE i.CustomerId = 2
                LIMIT 10;

            4. List all customers who live in a specific country (e.g., 'Germany').
            Query:
            SELECT c.CustomerId, c.FirstName, c.LastName
                FROM Customer c
                WHERE c.Country = 'Germany'
                LIMIT 10;

            5. Find all tracks in a specific genre (e.g., 'Rock').
            Query:
            SELECT t.Name AS Track
                FROM Track t
                JOIN Genre g ON t.GenreId = g.GenreId
                WHERE g.Name = 'Rock'
                LIMIT 10;

            Complex Example Scenarios:

            1. Find the total revenue generated by each artist, considering only the tracks sold after January 1, 2021.
            Additionally, provide the name of the artist, the total revenue, and the number of tracks that contributed to the revenue.
            Query:
            SELECT a.Name AS Artist,
                SUM(il.Quantity * il.UnitPrice) AS TotalRevenue,
                COUNT(t.TrackId) AS TotalTracksSold
            FROM Artist a
            JOIN Album al ON a.ArtistId = al.ArtistId
            JOIN Track t ON al.AlbumId = t.AlbumId
            JOIN InvoiceLine il ON t.TrackId = il.TrackId
            JOIN Invoice i ON il.InvoiceId = i.InvoiceId
            WHERE i.InvoiceDate > '2021-01-01'
            GROUP BY a.Name
            ORDER BY TotalRevenue DESC
            LIMIT 10;

            2. List all customers who have made a purchase of more than 3 tracks, with each track costing more than $1,
            and provide their email addresses, along with the total amount spent on those purchases.
            Query:
            SELECT c.Email, SUM(il.Quantity * il.UnitPrice) AS TotalSpent
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
            JOIN Track t ON il.TrackId = t.TrackId
            WHERE t.UnitPrice > 1
            GROUP BY c.Email
            HAVING COUNT(il.TrackId) > 3
            LIMIT 10;

            3. Find the most popular genre (by total sales) for each country,
            along with the total sales amount and the number of tracks sold, in descending order of sales.
            Query:
            SELECT c.Country, g.Name AS Genre,
                SUM(il.Quantity * il.UnitPrice) AS TotalSales,
                COUNT(il.TrackId) AS TotalTracksSold
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
            JOIN Track t ON il.TrackId = t.TrackId
            JOIN Genre g ON t.GenreId = g.GenreId
            GROUP BY c.Country, g.Name
            ORDER BY TotalSales DESC
            LIMIT 10;

            4. Get the details of customers who bought at least one track from 'AC/DC' or 'Accept',
            along with the total amount spent, and the number of unique albums they have purchased from.
            Query:
            SELECT c.CustomerId, c.FirstName, c.LastName, SUM(i.Total) AS TotalSpent, COUNT(DISTINCT al.AlbumId) AS UniqueAlbumsPurchased
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
            JOIN Track t ON il.TrackId = t.TrackId
            JOIN Album al ON t.AlbumId = al.AlbumId
            WHERE al.ArtistId IN (1, 2) -- AC/DC (ArtistId = 1) and Accept (ArtistId = 2)
            GROUP BY c.CustomerId, c.FirstName, c.LastName
            HAVING COUNT(DISTINCT al.AlbumId) > 0
            LIMIT 10;

            5. Retrieve the most recent purchase made by each customer who has spent more than $50
            on tracks from the 'Rock' genre, and list their name, the total amount spent,
            and the date of the most recent purchase.
            Query:
            SELECT c.FirstName, c.LastName, SUM(i.Total) AS TotalSpent, MAX(i.InvoiceDate) AS MostRecentPurchaseDate
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
            JOIN Track t ON il.TrackId = t.TrackId
            JOIN Genre g ON t.GenreId = g.GenreId
            WHERE g.Name = 'Rock'
            GROUP BY c.CustomerId, c.FirstName, c.LastName
            HAVING SUM(i.Total) > 50
            LIMIT 10;
        """
	return example_scenarios
