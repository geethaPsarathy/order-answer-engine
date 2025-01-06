import { NextConfig } from "next";
import dotenv from 'dotenv';

dotenv.config();  // Load .env variables into process.env

const isProd = process.env.NODE_ENV === 'production';
console.log('isProd:', isProd , process.env.NODE_ENV , process.env.LOCAL_URL );
const nextConfig: NextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: isProd
      ? process.env.PRODUCTION_URL
      : process.env.LOCAL_URL,
  },
  assetPrefix: process.env.NEXT_PUBLIC_ASSET_PREFIX || '',
};

export default nextConfig;