import React from "react";

const ageGroups = [
  { label: "0 - 5 years", image: "/images/0-5years.svg", value: "0-5", bg: "bg-yellow-100" },
  { label: "6 - 10 years", image: "/images/6-8years.svg", value: "6-10", bg: "bg-blue-100" },
  { label: "11 - 15 years", image: "/images/9-12years.svg", value: "11-15", bg: "bg-purple-100" },
  { label: "15+ years", image: "/images/13-16years.svg", value: "15+", bg: "bg-indigo-100" },
];

interface AgeGroupCardProps {
  selectedAgeGroup: string | null;
  setAgeGroup: (age: string) => void;
}

const AgeGroupCard: React.FC<AgeGroupCardProps> = ({ selectedAgeGroup, setAgeGroup }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-6">
      {ageGroups.map((group) => (
        <button
          key={group.value}
          className={`flex flex-col items-center justify-center w-[300px] h-[400px] p-6 rounded-lg shadow-md ${group.bg} transition 
            ${selectedAgeGroup === group.value ? "border-4 border-black" : "border border-gray-300"}`}
          onClick={() => setAgeGroup(group.value)}
        >
          {/* Centered Image */}
          <img 
            src={group.image} 
            alt={group.label} 
            className="w-[250px] h-[250px] object-contain mb-4" 
          />
          
          {/* Age Group Title */}
          <span className="text-xl font-semibold text-center">{group.label}</span>
        </button>
      ))}
    </div>
  );
};

export default AgeGroupCard;
