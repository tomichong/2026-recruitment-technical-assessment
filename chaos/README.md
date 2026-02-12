> This question is relevant for **chaos backend**

# DevSoc Subcommittee Recruitment: Chaos Backend

***Complete as many questions as you can.***

## Question 1
You have been given a skeleton function `process_data` in the `data.rs` file.
Complete the parameters and body of the function so that given a JSON request of the form

```json
{
  "data": ["Hello", 1, 5, "World", "!"]
}
```

the handler returns the following JSON:
```json
{
  "string_len": 11,
  "int_sum": 6
}
```

Edit the `DataResponse` and `DataRequest` structs as you need.

## Question 2

### a)
Write SQL (Postgres) `CREATE` statements to create the following schema. Be sure to include foreign keys to appropriately model the relationships and, if appropriate, make relevant tables `CASCADE` upon deletion. You may enrich the tables with additional columns should you wish. To help you answer the question, a simple diagram is provided. 
![Database Schema](db_schema.png)

**Answer box:**
```sql
-- The tables which are referenced should be created first
CREATE TABLE Users (
  -- Can also be SERIAL type, but I use INTEGER as noted in the question
  id INTEGER PRIMARY KEY
);

-- for subsequent tables, i use lowercase names as per the image in the question
-- (which isnt consistent with the Users table, but i shall follow the image)
CREATE TABLE playlists (
  id INTEGER PRIMARY KEY,
  -- every playlist must be created by a user
  user_id INTEGER NOT NULL 
    REFERENCES Users(id) 
    ON DELETE CASCADE,
  -- eveery playlist must have a name
  name TEXT NOT NULL
);

CREATE TABLE songs (
  id INTEGER PRIMARY KEY,
  -- every song must have title, artist and duration
  title TEXT NOT NULL,
  artist TEXT NOT NULL,
  duration INTERVAL NOT NULL
);

CREATE TABLE playlist_songs (
  playlist_id INTEGER NOT NULL 
    REFERENCES playlists(id)
    ON DELETE CASCADE,
  song_id INTEGER NOT NULL 
    REFERENCES songs(id)
    ON DELETE CASCADE,
  PRIMARY KEY (playlist_id, song_id)
);
```

### b)
Using the above schema, write an SQL `SELECT` query to return all songs in a playlist in the following format, given the playlist id `676767`
```
| id  | playlist_id | title                                      | artist      | duration |
| --- | ----------- | ------------------------------------------ | ----------- | -------- |
| 4   | 676767      | Undone - The Sweater Song                  | Weezer      | 00:05:06 |
| 12  | 676767      | She Wants To Dance With Me - 2023 Remaster | Rick Astley | 00:03:18 |
| 53  | 676767      | Music                                      | underscores | 00:03:27 |
```

**Answer box:**
```sql
-- go to playlist_songs and look for matching playlist_id, then go to songs and get song infos  
SELECT 
  songs.id,
  playlist_songs.playlist.id,
  songs.title,
  songs.artist,
  songs.duration
FROM songs
JOIN playlist_songs
ON playlist_songs.song_id = songs.id
WHERE playlist_songs.playlist_id = 676767;
```