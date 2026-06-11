import type { Metadata } from "next";
import Link from "next/link";

import "./globals.css";

export const metadata: Metadata = {
  title: "Je-hye Wiki",
  description: "Personal knowledge RAG and interactive portfolio",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <main>
          <nav>
            <Link href="/portfolio">Portfolio</Link>
            <Link href="/wiki">Private Wiki</Link>
          </nav>
          {children}
        </main>
      </body>
    </html>
  );
}
