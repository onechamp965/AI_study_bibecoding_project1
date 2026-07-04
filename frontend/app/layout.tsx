import "./globals.css";

export const metadata = {
  title: "Sana Factory",
  description: "AI Chinese Shorts Factory",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
