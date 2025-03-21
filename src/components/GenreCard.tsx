import React from "react";

const genres = [
  { label: "Adventure", image: "/images/adventure.svg", value: "Adventure", bg: "bg-red-100" },
  { label: "Fantasy", image: "/images/fantasy.svg", value: "Fantasy", bg: "bg-blue-100" },
  { label: "Mystery", image: "/images/mystery.svg", value: "Mystery", bg: "bg-green-100" },
  { label: "Science", image: "/images/science.svg", value: "Science", bg: "bg-purple-100" },
  { label: "History", image: "/images/history.svg", value: "History", bg: "bg-yellow-100" },
];

interface GenreCardProps {
  selectedGenre: string | null;
  setGenre: (genre: string) => void;
}

const GenreCard: React.FC<GenreCardProps> = ({ selectedGenre, setGenre }) => {
  return (
    <div className="grid grid-cols-3 gap-6 mt-6 md:grid-cols-3 md:grid-rows-2 justify-center">
      {genres.map((genre) => (
        <button
          key={genre.value}
          className={`flex flex-col items-center justify-center w-[300px] h-[200px] p-4 rounded-lg shadow-md ${genre.bg} transition 
            ${selectedGenre === genre.value ? "border-4 border-black" : "border border-gray-300"}`}
          onClick={() => setGenre(genre.value)}
        >
          {/* Centered Image */}
          <img 
            src={genre.image} 
            alt={genre.label} 
            className="w-[300px] h-[300px] object-contain mb-2" 
          />
          
          {/* Genre Label */}
          <span className="text-lg font-semibold text-center">{genre.label}</span>
        </button>
      ))}
    </div>
  );
};


export default GenreCard;
