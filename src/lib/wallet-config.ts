import { getDefaultConfig } from "@rainbow-me/rainbowkit";
import { mainnet, polygon, arbitrum, base, bsc, optimism } from "wagmi/chains";

export const config = getDefaultConfig({
  appName: "Warima",
  projectId: "demo", // Replace with your WalletConnect project ID
  chains: [mainnet, polygon, arbitrum, base, bsc, optimism],
  ssr: false,
});
