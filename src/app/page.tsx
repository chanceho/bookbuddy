"use client";
import { useState } from "react";
import BookList from "@/components/BookList";
import AgeGroupCard from "@/components/AgeGroupCard";
import GenreCard from "@/components/GenreCard";
import Button from "@/components/Button";
import { books } from "../../services/books";
import { Book } from "@/types/book";

export default function Home() {
  const [selectedBooks, setSelectedBooks] = useState<string[]>([]);
  const [ageGroup, setAgeGroup] = useState<string | null>(null);
  const [genre, setGenre] = useState<string | null>(null);
  const [recommendedBooks, setRecommendedBooks] = useState<Book[]>([]);

  // Hardcoded book list
  const displayedBooks = books.slice(0, 5);

  const handleFindBooks = () => {
    if (selectedBooks.length === 3 && ageGroup && genre) {
      // Placeholder recommendation logic (replace with API call later)
      setRecommendedBooks(books.slice(5, 10));
    }
  };

  return (
    <div className="flex flex-col items-center p-6">
      <h1 className="text-5xl font-bold tracking-widest">BookBuddy</h1>
      <p className="text-3xl mt-2">Find the perfect book for every young explorer</p>

      {/* Step 1: Choose Books */}
      <h2 className="mt-10 text-4xl font-semibold tracking-widest">Choose 3 Favorite Books</h2>
      <BookList books={displayedBooks} selectedBooks={selectedBooks} setSelectedBooks={setSelectedBooks} />

      {/* Step 2: Choose Age Group */}
      <h2 className="mt-10 text-4xl font-semibold tracking-widest">Select Your Age Group</h2>
      <AgeGroupCard setAgeGroup={setAgeGroup} selectedAgeGroup={ageGroup} />

      {/* Step 3: Choose Genre */}
      <h2 className="mt-10 text-4xl font-semibold tracking-widest">Pick Your Favorite Genre</h2>
      <GenreCard setGenre={setGenre} selectedGenre={genre} />

      {/* Step 4: Find Books Button */}
      <Button className="mt-8" onClick={handleFindBooks} disabled={selectedBooks.length < 3 || !ageGroup || !genre}>
        Find Books
      </Button>

      {/* Display Recommended Books */}
      {recommendedBooks.length > 0 && (
        <div className="mt-6">
          <h2 className="text-4xl font-semibold tracking-widest">Recommended Books</h2>
          <BookList books={recommendedBooks} selectedBooks={[]} setSelectedBooks={() => {}}/>
        </div>
      )}
    </div>
  );
}
