import React from "react";
import { Book } from "@/types/book";
import BookCard from "./BookCards";

interface BookListProps {
  books: Book[];
  selectedBooks: string[];
  setSelectedBooks: (books: string[]) => void;
}

const BookList: React.FC<BookListProps> = ({ books, selectedBooks, setSelectedBooks }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mt-4">
      {books.map((book) => (
        <BookCard key={book.id} book={book} selectedBooks={selectedBooks} setSelectedBooks={setSelectedBooks} />
      ))}
    </div>
  );
};

export default BookList;
