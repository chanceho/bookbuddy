interface Book {
    book_id: string;
    title: string;
    authors: string;
    genre: string;
    ageGroup: string;
    rating: number;
    coverImage: string;
    description: string;
  }
  
  export const fetchBookDetails = async (book_id: string): Promise<Book> => {
    try {
      const response = await fetch(`http://localhost:8000/book/${book_id}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching book details:', error);
      throw error;
    }
  };