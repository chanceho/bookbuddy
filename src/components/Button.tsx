import React from "react";

interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  className?: string;
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({ onClick, children, className, disabled }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`text-xl px-4 py-2 transition font-semibold 
        ${disabled ? "bg-gray-400 cursor-not-allowed" : "bg-[#7C6063] hover:bg-[#6B5255] text-white"} 
        ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;
