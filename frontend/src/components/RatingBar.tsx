import { Star } from "lucide-react"; // You can use any star icon library

type RatingBarProps = {
  rating: number;
};

const RatingBar = ({ rating }: RatingBarProps) => {
  const filledStars = Math.floor(rating); // Round down to nearest integer
  const totalStars = 5;

  return (
    <div className="flex justify-center gap-1">
      {[...Array(totalStars)].map((_, index) => (
        <Star
          key={index}
          fill={index < filledStars ? "gold" : "none"}
          stroke="gold"
          className="w-6 h-6"
        />
      ))}
    </div>
  );
};

export default RatingBar;