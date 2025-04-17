import { useState } from "react";
import { Book } from "@/types/book";

export const books: Book[] = [
  {
    book_id: "1",
    title: "The Adventures of Tom Sawyer",
    authors: "Mark Twain",
    genre: "Adventure",
    ageGroup: "7-9",
    rating: 4.2,
    coverImage: "/images/tom.jpg",
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisi. Suspendisse potenti. Aenean euismod, magna at sagittis viverra, sapien urna fermentum justo, in scelerisque risus nunc nec justo.",
  },
  {
    book_id: "2",
    title: "Harry Potter and the Sorcerer's Stone",
    authors: "J.K. Rowling",
    genre: "Fantasy",
    ageGroup: "10-12",
    rating: 4.2,
    coverImage: "/images/harry_potter_sorcerer.jpg",
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisi. Suspendisse potenti. Aenean euismod, magna at sagittis viverra, sapien urna fermentum justo, in scelerisque risus nunc nec justo.",
  },
  {
    book_id: "3",
    title: "Charlotte's Web",
    authors: "E.B. White",
    genre: "Classic",
    ageGroup: "6-8",
    rating: 4.2,
    coverImage: "/images/charlotte_web.jpeg",
    description: "Book 3",
  },
  {
    book_id: "4",
    title: "Percy Jackson & The Olympians: The Lightning Thief",
    authors: "Rick Riordan",
    genre: "Fantasy",
    ageGroup: "10-12",
    rating: 4.2,
    coverImage: "/images/percy.jpg",
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisi. Suspendisse potenti. Aenean euismod, magna at sagittis viverra, sapien urna fermentum justo, in scelerisque risus nunc nec justo.",
  },
  {
    book_id: "5",
    title: "The Secret Garden",
    authors: "Frances Hodgson Burnett",
    genre: "Classic",
    ageGroup: "9-12",
    rating: 4.2,
    coverImage: "/images/secret_garden.webp",
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla facilisi. Suspendisse potenti. Aenean euismod, magna at sagittis viverra, sapien urna fermentum justo, in scelerisque risus nunc nec justo.",
  },
];

export const getRandomBooks = (count: number): Book[] => {
  return books.sort(() => Math.random() - 0.5).slice(0, count);
};
