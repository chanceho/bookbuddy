"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import AgeGroupCard from "@/components/AgeGroupCard";
import GenreCard from "@/components/GenreCard";
import Button from "@/components/Button";
import { books } from "@/services/books";
import { Book } from "@/types/book";

export default function Home() {
  const [step, setStep] = useState(1);
  const [ageGroup, setAgeGroup] = useState<string | null>(null);
  const [genre, setGenre] = useState<string | null>(null);
  const [recommendedBooks, setRecommendedBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  
  const handleFindBooks = async () => {
    if (ageGroup && genre) {
      setLoading(true);
      try {
        const response = await fetch('https://bookbuddy-production-f4e6.up.railway.app/recommend_books', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ ageGroup, genre })
        });
  
        const data = await response.json();
  
        if (response.ok) {
          if (data.error && data.error === "No book found for given filters.") {
            setRecommendedBooks([]); // Set empty array to trigger "No recommendations" UI
          } else {
            // Handle both array response and { recommendations: [...] } format
            setRecommendedBooks(Array.isArray(data) ? data : data.recommendations || []);
          }
        } else {
          console.warn("API failed:", data.error || "Unknown error");
          setRecommendedBooks([]); // Set empty array to trigger "No recommendations" UI
        }
      } catch (error) {
        console.error('Recommendation error:', error);
        setRecommendedBooks([]); // Set empty array to trigger "No recommendations" UI
      } finally {
        setLoading(false);
        setStep(3);
      }
    }
  };
  

  const Breadcrumbs = () => (
    <div className="text-2xl text-gray-500 mt-8 w-full text-left">
      {["Choose Age", "Pick Genre", "Recommendations"].map((label, index) => (
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
      <p className="text-3xl mt-2">Find the Perfect Book for Every Young Explorer</p>

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
            <Button onClick={handleFindBooks} disabled={!genre}>
              Find Books
            </Button>
          </div>
        </>
      )}

      {/* Step 3: Show Recommended Books */}
      {step === 3 && (
        <>
          <h2 className="mt-10 text-4xl font-semibold tracking-widest">
            Here are our recommended books for you!
          </h2>
          {console.log('Displaying recommendations:', recommendedBooks)}

          {loading ? (
            <div className="mt-8 text-xl">Finding your perfect books...</div>
          ) : recommendedBooks.length > 0 ? (
            <div className="mt-8 w-full">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendedBooks.map((book) => (
                  <div 
                    key={book.book_id}
                    className="border rounded-lg p-4 cursor-pointer hover:shadow-lg transition-shadow"
                    onClick={(e) => {
                      window.open(`/book/${book.book_id}`, '_blank', 'noopener,noreferrer');
                    }}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        window.open(`/book/${book.book_id}`, '_blank', 'noopener,noreferrer');
                      }
                    }}
                    role="link"
                    tabIndex={0}
                  >
                    <div className="h-48 flex items-center justify-center mb-4">
                      <img src={book.coverImage} alt={book.title} className="w-36 h-48 object-cover mb-2"/>
                    </div>
                    <h3 className="text-xl text-center font-bold">{book.title}</h3>
                    <p className="text-gray-600 text-center">{book.authors}</p>
                  </div>
                ))}
              </div>
              <div className="mt-8 flex gap-4 justify-center">
                <Button onClick={() => setStep(2)}>Back</Button>
                <Button onClick={() => setStep(1)}>Start Over</Button>
              </div>
            </div>
          ) : (
            <div className="mt-8 text-xl">
              No recommendations found. Please try different selections.
              <div className="mt-4 flex gap-4 justify-center">
                <Button onClick={() => setStep(2)}>Back</Button>
                <Button onClick={() => setStep(1)}>Start Over</Button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
