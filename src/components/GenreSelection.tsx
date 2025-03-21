"use client";
import React, { useState } from "react";
import GenreCard from "./GenreCard";

const genres = [
  { id: 1, name: "Adventure", image: "/images/adventure.svg" },
  { id: 2, name: "Fantasy", image: "/images/fantasy.svg" },
  { id: 3, name: "Science Fiction", image: "/images/scifi.svg" },
  { id: 4, name: "Mystery", image: "/images/mystery.svg" },
  { id: 5, name: "History", image: "/images/history.svg" },
];

const GenreSelection: React.FC = () => {
  const [selectedGenre, setSelectedGenre] = useState<number | null>(null);

  return (
    <div className="p-6 text-center">
      <h2 className="text-xl font-bold mb-4">Select Your Favorite Genre</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {genres.map((genre) => (
          <GenreCard
            key={genre.id}
            genre={genre.name}
            imageSrc={genre.image}
            selected={selectedGenre === genre.id}
            onSelect={() => setSelectedGenre(genre.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default GenreSelection;
