import { describe, expect, it } from "vitest";

import { normalizeApiUrl } from "./api";

describe("normalizeApiUrl", () => {
  it("adds the API prefix when the backend URL is the host root", () => {
    expect(normalizeApiUrl("https://backend.example.vercel.app", false)).toBe(
      "https://backend.example.vercel.app/api",
    );
  });

  it("does not duplicate the API prefix", () => {
    expect(normalizeApiUrl("https://backend.example.vercel.app/api/", false)).toBe(
      "https://backend.example.vercel.app/api",
    );
  });

  it("uses localhost only during development", () => {
    expect(normalizeApiUrl(undefined, true)).toBe("http://localhost:8000/api");
    expect(normalizeApiUrl(undefined, false)).toBe("");
  });
});
