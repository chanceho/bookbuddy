import type { Metadata } from "next";
import { Unkempt } from "next/font/google";
import "@/styles/globals.css";

const unkempt = Unkempt({
  subsets: ["latin"],
  variable: "--font-unkempt",
  weight: "400",
});

export const metadata: Metadata = {
  title: "BookBuddy - Personalized Book Recommendations for Kids",
  description: "Discover the best books for kids with personalized recommendations based on age, genre, and preferences.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${unkempt.variable} font-sans`}
      >
        <main className="min-h-screen flex flex-col">
          {children}
          <footer className="mt-auto bg-gray-100 py-4 text-center">
            <img src="/images/footer.svg" className="mx-auto w-auto h-auto" />
          </footer>
        </main>
      </body>
    </html>
  );
}
