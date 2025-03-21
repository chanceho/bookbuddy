import { useState } from "react";
import { Book } from "@/types/book";

export const books: Book[] = [
  {
    id: "1",
    title: "The Adventures of Tom Sawyer",
    author: "Mark Twain",
    genre: "Adventure",
    ageGroup: "7-9",
    coverImage: "/images/action.svg",
  },
  {
    id: "2",
    title: "Harry Potter and the Sorcerer's Stone",
    author: "J.K. Rowling",
    genre: "Fantasy",
    ageGroup: "10-12",
    coverImage: "/images/mystery.svg",
  },
  {
    id: "3",
    title: "Charlotte's Web",
    author: "E.B. White",
    genre: "Classic",
    ageGroup: "6-8",
    coverImage: "/images/classic.svg",
  },
  {
    id: "4",
    title: "Percy Jackson & The Olympians: The Lightning Thief",
    author: "Rick Riordan",
    genre: "Fantasy",
    ageGroup: "10-12",
    coverImage: "/images/fantasy.svg",
  },
  {
    id: "5",
    title: "The Secret Garden",
    author: "Frances Hodgson Burnett",
    genre: "Classic",
    ageGroup: "9-12",
    coverImage: "/images/action.svg",
  },
];

export const getRandomBooks = (count: number): Book[] => {
  return books.sort(() => Math.random() - 0.5).slice(0, count);
};
