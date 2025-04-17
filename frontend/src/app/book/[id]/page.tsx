"use client";
import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import Image from "next/image";
import RatingBar from "@/components/RatingBar";
import { fetchBookDetails } from "@/services/api";
import { Book } from "@/types/book";

const BookDetail = () => {
  const router = useRouter();
  const { id } = useParams();
  const [book, setBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    const loadBook = async () => {
      try {
        setLoading(true);
        const bookData = await fetchBookDetails(id as string);
        setBook(bookData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load book');
      } finally {
        setLoading(false);
      }
    };

    loadBook();
  }, [id]);

  if (loading) {
    return <div className="text-center py-12">Loading book details...</div>;
  }

  if (error) {
    return (
      <div className="text-center py-12 text-red-500">
        <p>Error: {error}</p>
        <button 
          onClick={() => router.push('/')}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Return Home
        </button>
      </div>
    );
  }

  if (!book) {
    return <div className="text-center py-12">Book not found</div>;
  }

  return (
    <div className="flex flex-col items-center p-6">
      {/* Header and navigation */}
      <h1 className="text-5xl font-bold tracking-widest">BookBuddy</h1>
      <p className="text-3xl mt-2">Find the Perfect Book for Every Young Explorer</p>
      
      <button 
        onClick={() => router.push("/")} 
        className="text-2xl text-gray-500 mt-8 w-full hover:underline"
      >
        ← 🏠 Home
      </button>

      {/* Book details */}
      <div className="flex mt-10 w-10/12 max-w-4xl mx-auto gap-6">
        {/* Book cover and metadata */}
        <div className="w-1/3 bg-white border border-gray-300 rounded-lg p-4 text-center shadow-sm">
          <div className="flex justify-center">
            <img
              src={book.coverImage}
              alt={book.title}
              className="w-36 h-48 object-cover mb-2 rounded-lg shadow-md"
              onError={(e) => {
                (e.target as HTMLImageElement).src = '/book-placeholder.png';
              }}
            />
          </div>
          <h2 className="text-3xl font-bold mt-4">{book.title}</h2>
          <p className="text-xl font-bold text-gray-600">Age Group: {book.ageGroup}</p>
          <p className="text-xl font-bold text-gray-600">Genre: {book.genre}</p>
          <p className="text-xl font-bold text-gray-600">Goodreads Rating:</p>
          <RatingBar rating={book.rating}/>
        </div>

        {/* Book description */}
        <div className="w-2/3 bg-white border border-gray-300 rounded-lg p-6 text-center shadow-sm">
          <h2 className="text-3xl font-bold">{book.title}</h2>
          <p className="text-xl font-semibold text-gray-700">Author: {book.authors}</p>
          <h3 className="mt-4 text-2xl font-semibold">Summary</h3>
          <p className="text-xl text-gray-700">{book.description}</p>
        </div>
      </div>
    </div>
  );
};

export default BookDetail;