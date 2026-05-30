import type { Config } from "jest";

const config: Config = {
  testEnvironment: "jsdom",
  setupFilesAfterFramework: [],
  setupFiles: ["<rootDir>/jest.setup.ts"],
  moduleNameMapper: { "^@/(.*)$": "<rootDir>/$1" },
  transform: { "^.+\\.(ts|tsx)$": "ts-jest" },
};

export default config;
