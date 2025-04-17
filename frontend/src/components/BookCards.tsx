import React from "react";
import { Book } from "@/types/book";
import { useRouter } from "next/navigation";

interface BookCardProps {
  book: Book;
  selectedBooks: string[];
  setSelectedBooks?: (books: string[]) => void; // Make this optional
  isRecommendation?: boolean; // New prop to distinguish recommendation view
}

const BookCard: React.FC<BookCardProps> = ({ 
  book, 
  selectedBooks, 
  setSelectedBooks,
  isRecommendation = false 
}) => {
  const router = useRouter();
  const isSelected = selectedBooks.includes(book.book_id);
  const isDisabled = !isRecommendation && selectedBooks.length >= 3 && !isSelected;

  const handleClick = () => {
    if (isRecommendation) {
      // Navigate to book detail page in recommendation view
      router.push(`/book/${book.book_id}`);
    } else if (setSelectedBooks) {
      // Original selection logic for step 3
      if (isSelected) {
        setSelectedBooks(selectedBooks.filter((id) => id !== book.book_id));
      } else if (!isDisabled) {
        setSelectedBooks([...selectedBooks, book.book_id]);
      }
    }
  };

  return (
    <button
      className={`flex flex-col items-center p-4 rounded-lg shadow-md border 
        transition-all duration-300 ${isSelected ? "border-4 border-black" : "border-gray-300"} 
        ${isDisabled && !isSelected ? "opacity-50 cursor-not-allowed" : "hover:border-black"}`}
      onClick={handleClick}
      disabled={isDisabled && !isRecommendation}
    >
      <img src={book.coverImage} alt={book.title} className="w-36 h-48 object-cover mb-2" />
      <h3 className="text-lg font-semibold">{book.title}</h3>
      <p className="text-sm text-gray-500">{book.authors}</p>
    </button>
  );
};

export default BookCard