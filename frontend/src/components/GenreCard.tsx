import React from "react";

const genres = [
  { label: "Fantasy", image: "/images/fantasy.svg", value: "Fantasy", bg: "bg-purple-100" },
  { label: "Romance", image: "/images/romance.svg", value: "Romance", bg: "bg-yellow-100" },
  { label: "Art/Photography", image: "/images/art.svg", value: "Art/Photography", bg: "bg-red-100" },
  { label: "Mistery/Thriller", image: "/images/mystery.svg", value: "Mistery/Thriller", bg: "bg-blue-100" },
  { label: "Classic", image: "/images/classic.svg", value: "Classic", bg: "bg-purple-100" },
  { label: "Science Fiction", image: "/images/science.svg", value: "Science Fiction", bg: "bg-green-100" },
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
          className={`flex flex-col items-center justify-center w-[400px] h-[300px] p-4 rounded-lg shadow-md ${genre.bg} transition 
            ${selectedGenre === genre.value ? "border-4 border-black" : "border border-gray-300"}`}
          onClick={() => setGenre(genre.value)}
        >
          {/* Centered Image */}
          <img 
            src={genre.image} 
            alt={genre.label} 
            className="w-[400px] h-[300px] object-contain mb-2" 
          />
          
          {/* Genre Label */}
          <span className="text-2xl font-bold text-center">{genre.label}</span>
        </button>
      ))}
    </div>
  );
};


export default GenreCard;
