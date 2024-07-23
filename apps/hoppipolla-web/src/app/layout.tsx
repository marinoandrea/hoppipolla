import type { Metadata } from "next";
import { Inter } from "next/font/google";

import Navbar from "@/components/navbar";
import Providers from "@/components/providers";

import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Hoppipolla Web UI",
  description: "Manage your policy and test networking",
  icons: [],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <Navbar />
          <main className="max-w-screen-xl mx-auto h-screen overflow-hidden border-x border-foreground">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
