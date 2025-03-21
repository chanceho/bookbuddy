import React, { useState } from "react";
import GenreCard from "./GenreCard";

const GenreSelection: React.FC = () => {
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);

  return (
    <div className="p-6 text-center">
      <h2 className="text-xl font-bold mb-4">Select Your Favorite Genre</h2>
      <GenreCard selectedGenre={selectedGenre} setGenre={setSelectedGenre} />
    </div>
  );
};

export default GenreSelection;