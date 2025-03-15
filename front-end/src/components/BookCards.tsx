import React from "react";
import { Book } from "@/types/book";

interface BookCardProps {
  book: Book;
  selectedBooks: string[];
  setSelectedBooks: (books: string[]) => void;
}

const BookCard: React.FC<BookCardProps> = ({ book, selectedBooks, setSelectedBooks }) => {
  const isSelected = selectedBooks.includes(book.id);
  const isDisabled = selectedBooks.length >= 3 && !isSelected;

  const handleClick = () => {
    if (isSelected) {
      setSelectedBooks(selectedBooks.filter((id) => id !== book.id));
    } else if (!isDisabled) {
      setSelectedBooks([...selectedBooks, book.id]);
    }
  };

  return (
    <button
      className={`flex flex-col items-center p-4 rounded-lg shadow-md border 
        transition-all duration-300 ${isSelected ? "border-4 border-black" : "border-gray-300"} 
        ${isDisabled && !isSelected ? "opacity-50 cursor-not-allowed" : "hover:border-black"}`}
      onClick={handleClick}
      disabled={isDisabled}
    >
      <img src={book.coverImage} alt={book.title} className="w-24 h-32 object-cover mb-2" />
      <h3 className="text-lg font-semibold">{book.title}</h3>
      <p className="text-sm text-gray-500">{book.author}</p>
    </button>
  );
};

export default BookCard;
