import { Book } from "@/types/book";
import BookCard from "./BookCards";

interface BookListProps {
  books: Book[];
  selectedBooks: string[];
  setSelectedBooks?: (books: string[]) => void;
  isRecommendation?: boolean;
}

const BookList: React.FC<BookListProps> = ({ 
  books, 
  selectedBooks, 
  setSelectedBooks,
  isRecommendation = false 
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {books.map((book) => (
        <BookCard
          key={book.book_id}
          book={book}
          selectedBooks={selectedBooks}
          setSelectedBooks={setSelectedBooks}
          isRecommendation={isRecommendation}
        />
      ))}
    </div>
  );
};

export default BookList