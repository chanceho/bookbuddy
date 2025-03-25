"use client";
import { useState } from "react";
import BookList from "@/components/BookList";
import AgeGroupCard from "@/components/AgeGroupCard";
import GenreCard from "@/components/GenreCard";
import Button from "@/components/Button";
import { books } from "../../services/books";
import { Book } from "@/types/book";

export default function Home() {
  const [step, setStep] = useState(1);
  const [ageGroup, setAgeGroup] = useState<string | null>(null);
  const [genre, setGenre] = useState<string | null>(null);
  const [selectedBooks, setSelectedBooks] = useState<string[]>([]);
  const [recommendedBooks, setRecommendedBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(false);

  const handleFindBooks = () => {
    if (selectedBooks.length >= 3 && ageGroup && genre) {
      setRecommendedBooks(books.slice(5, 10)); // Placeholder recommendation logic
      setStep(4);
    }
  };

  const Breadcrumbs = () => (
    <div className="text-2xl text-gray-500 mt-8 w-full text-left">
      {["Choose Age", "Pick Genre", "Select Books", "Recommendations"].map((label, index) => (
        <span key={index} className={index + 1 === step ? "font-bold text-black" : ""}>
          {index > 0 && " > "}
          {label}
        </span>
      ))}
    </div>
  );

  return (
    <div className="flex flex-col items-center p-6">
      <h1 className="text-5xl font-bold tracking-widest">BookBuddy</h1>
      <p className="text-3xl mt-2">Find the perfect book for every young explorer</p>

      {/* Breadcrumb Navigation */}
      <Breadcrumbs />

      {/* Step 1: Choose Age Group */}
      {step === 1 && (
        <>
          <h2 className="mt-10 text-4xl font-semibold tracking-widest">What is your current age?</h2>
          <AgeGroupCard setAgeGroup={setAgeGroup} selectedAgeGroup={ageGroup} />
          <Button className="mt-8" onClick={() => setStep(2)} disabled={!ageGroup}>
            Next
          </Button>
        </>
      )}

      {/* Step 2: Choose Genre */}
      {step === 2 && (
        <>
          <h2 className="mt-10 text-4xl font-semibold tracking-widest">What do you want to read today?</h2>
          <GenreCard setGenre={setGenre} selectedGenre={genre} />
          <div className="mt-8 flex gap-4">
            <Button onClick={() => setStep(1)}>Back</Button>
            <Button onClick={() => setStep(3)} disabled={!genre}>
              Next
            </Button>
          </div>
        </>
      )}

      {/* Step 3: Pick Books */}
      {step === 3 && (
        <>
          <h2 className="mt-10 text-4xl font-semibold tracking-widest">What are the books that you have read?</h2>
          <BookList books={books.slice(0, 5)} selectedBooks={selectedBooks} setSelectedBooks={setSelectedBooks} />
          <div className="mt-8 flex gap-4">
            <Button onClick={() => setStep(2)}>Back</Button>
            <Button onClick={handleFindBooks} disabled={selectedBooks.length < 3}>
              Find Books
            </Button>
          </div>
        </>
      )}

      {/* Step 4: Show Recommended Books */}
      {step === 4 && (
        <>
          <h2 className="mt-10 text-4xl font-semibold tracking-widest">Here are our recommended books for you!</h2>
          <BookList books={books.slice(0, 5)} selectedBooks={selectedBooks} setSelectedBooks={setSelectedBooks} />
          <div className="mt-8">
            <Button onClick={() => setStep(3)}>Back</Button>
          </div>
        </>
      )}
    </div>
  );
}
