import datetime
from typing import Optional, List

from app.db_manager import DBManager
from app.model.db import BookEntity


class BookRepository:
    INSERT_BOOK_QUERY = """
        INSERT INTO books (id, title, author, published_date, isbn, page_count, cover_url, language) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;
    """

    GET_ALL_BOOKS_QUERY = """
        SELECT * FROM books;
    """

    GET_BOOK_BY_ID_QUERY = """
        SELECT * FROM books WHERE id = %s;
    """

    UPDATE_BOOK_BY_ID_QUERY = """
        UPDATE books SET title = %s, author = %s, published_date = %s, isbn = %s, page_count = %s, cover_url = %s, 
            language = %s
        WHERE id = %s RETURNING *;
    """

    DELETE_BOOK_BY_ID_QUERY = """
        DELETE FROM books WHERE id = %s RETURNING *;
    """

    def __init__(self, db_manager: DBManager):
        self._db_manager = db_manager

    @staticmethod
    def map_to_entity(book_id, title, author, published_date, isbn, page_count, cover_url, language) -> BookEntity:
        return BookEntity(book_id=book_id, title=title, author=author, published_date=published_date, isbn=isbn,
                          page_count=page_count, cover_url=cover_url, language=language)

    def get_all_books(self) -> List[BookEntity]:
        with self._db_manager.session() as curr:
            curr.execute(self.GET_ALL_BOOKS_QUERY)
            results = curr.fetchall()

        return list(map(lambda book: self.map_to_entity(*book), results))

    def get_book_by_id(self, book_id: str) -> Optional[BookEntity]:
        with self._db_manager.session() as curr:
            curr.execute(self.GET_BOOK_BY_ID_QUERY, (book_id,))
            result = curr.fetchone()

        if result:
            return self.map_to_entity(*result)
        else:
            return None

    def insert_book(self, book: BookEntity) -> BookEntity:
        params = (book.id, book.title, book.author, book.published_date, book.isbn, book.page_count, book.cover_url, book.language)
        with self._db_manager.session() as curr:
            curr.execute(self.INSERT_BOOK_QUERY, params)
            result = curr.fetchone()
            self._db_manager.commit()

        return self.map_to_entity(*result)

    def update_book(self, book: BookEntity) -> Optional[BookEntity]:
        params = (book.title, book.author, book.published_date, book.isbn, book.page_count, book.cover_url,
                  book.language, book.id)
        with self._db_manager.session() as curr:
            curr.execute(self.UPDATE_BOOK_BY_ID_QUERY, params)
            result = curr.fetchone()
            self._db_manager.commit()

        if result:
            return self.map_to_entity(*result)
        else:
            return None

    def delete_book_by_id(self, book_id: str) -> Optional[BookEntity]:
        with self._db_manager.session() as curr:
            curr.execute(self.DELETE_BOOK_BY_ID_QUERY, (book_id,))
            result = curr.fetchone()

        if result:
            return self.map_to_entity(*result)
        else:
            return None

    def get_filtered_books(self, author: Optional[str] = None, title: Optional[str] = None,
                           language: Optional[str] = None, date_from: Optional[datetime.date] = None,
                           date_to: Optional[datetime.date] = None) -> List[BookEntity]:
        params = []
        query = 'SELECT * FROM books'
        where_clauses = []
        if author or title or language or date_from or date_to:
            query += ' WHERE '
            if author:
                params.append(author+'%')
                where_clauses.append("author LIKE %s")
            if title:
                params.append(title+'%')
                where_clauses.append("title LIKE %s")
            if language:
                params.append(language)
                where_clauses.append('language = %s')
            if date_from:
                params.append(date_from)
                where_clauses.append('published_date >= %s')
            if date_to:
                params.append(date_to)
                where_clauses.append('published_date <= %s')
            query += ' AND '.join(where_clauses) + ';'

        print(query, params)
        with self._db_manager.session() as curr:
            curr.execute(query, params)
            results = curr.fetchall()

        return list(map(lambda book: self.map_to_entity(*book), results))
