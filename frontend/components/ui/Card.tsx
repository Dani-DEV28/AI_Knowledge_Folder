interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export default function Card({ children, className = "" }: CardProps) {
  return (
    <div className={`bg-dark-700 border border-dark-600 rounded-lg p-4 ${className}`}>
      {children}
    </div>
  );
}
