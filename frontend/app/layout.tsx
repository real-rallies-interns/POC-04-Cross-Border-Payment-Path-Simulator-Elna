import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Real Rails | Cross-Border Payment Path Simulator",
  description: "Real Rails Intelligence – PoC #04",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
        <script src="https://cdn.tailwindcss.com"></script>
        <script dangerouslySetInnerHTML={{
          __html: `
            tailwind.config = {
              theme: {
                extend: {
                  colors: {
                    obsidian: '#030712',
                    navy: '#0B1117',
                    slate800: '#1F2937',
                  }
                }
              }
            }
          `
        }} />
      </head>
      <body>{children}</body>
    </html>
  );
}