# Operations

 HTTP Method | Request URI | Description 
-----------------|-----------------------------------|--------------------
GET | /api/books | Retrieve collection of books, allows filtering with query string | 
POST | /api/books | Create new book, payload
GET | /api/books/{book_id} | Retrieve book with id {book_id}
PUT | /api/books/{book_id} | Change book with id {book_id}
DELETE | /api/books/{book_id} | Delete book with id {book_id}
PUT | /api/books/import?q={keywords} | Import books matching to keywords from google api



## [GET] /api/books
### QueryParams:
 - author
 - title
 - language
 - published_date__from
 - published_date__to

### Success code: 200
#### Response Body:
```javascript
[
    BookSchema
]
```

Example url with query parameters: ```https://bookapi.com/api/books?author=Tolkien&title=Hobbit&language=en&published_date__from=1900-01-01&published_date__to=2020-01-01```


## [POST] /api/books 
...
## [GET] /api/books/{book_id} 
...
## [PUT] /api/books/{book_id} 
...
## [DELETE] /api/books/{book_id} 
...
## [PUT] /api/books/import?q={keywords}
...


### Book Schema:
```javascript
{
  "id": string, 
  "author": string,
  "title": string,
  "isbn": string,
  "published_date": date,
  "page_count": int,
  "cover_url": url,
  "language": string
}
```