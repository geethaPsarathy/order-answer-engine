import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/SideBar";
import { Toaster } from "sonner";
import ThemeProvider from "@/components/theme/Provider";
import { cn } from "@/lib/utils";

const montserrat = Montserrat({
  weight: ["300", "400", "500", "700"],
  subsets: ["latin"],
  display: "swap",
  fallback: ["Arial", "sans-serif"],
});

export const metadata: Metadata = {
  title: "Menu Decoder - Enhance Your Dining Experience",
  description:
    "Discover the best food and drink pairings, powered by AI and real-time data from Yelp and Reddit.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html className="h-full" lang="en">
      <body
        className={cn(
          "h-full bg-light-primary dark:bg-dark-primary text-light-text dark:text-dark-text",
          montserrat.className
        )}
        suppressHydrationWarning
      >
        <ThemeProvider>
          <div className="flex min-h-screen">
            {/* Sidebar */}
            <Sidebar />
            {/* Main Content */}
            <main className="flex-1 lg:pl-20 bg-light-primary dark:bg-dark-primary min-h-screen">
              <div className="max-w-screen-lg lg:px-8 px-4 mx-auto">{children}</div>
            </main>
          </div>
          {/* Toast Notifications */}
          <Toaster
            toastOptions={{
              unstyled: true,
              classNames: {
                toast:
                  "bg-white dark:bg-gray-800 dark:text-white/80 text-black rounded-lg p-4 flex items-center space-x-2",
              },
            }}
          />
        </ThemeProvider>
      </body>
    </html>
  );
}
