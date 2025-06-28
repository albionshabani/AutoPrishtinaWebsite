import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css"; // <-- THIS IS THE CRITICAL FIX FOR STYLING

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Auto Prishtina Import",
  description: "Certified pre-owned vehicles from South Korea.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}