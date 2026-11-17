import { beforeEach, describe, expect, it, vi } from "vitest";

import { api, normalizeApiUrl } from "./api";

describe("normalizeApiUrl", () => {
  it("adds the API prefix when the backend URL is the host root", () => {
    expect(normalizeApiUrl("https://backend.example.vercel.app", false)).toBe(
      "https://backend.example.vercel.app/api",
    );
  });

  describe("createOrder", () => {
    beforeEach(() => {
      vi.stubGlobal("fetch", vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ id: 1 }), {
          status: 201,
          headers: { "Content-Type": "application/json" },
        }),
      ));
    });

    it("preserves JSON content type alongside the idempotency key", async () => {
      await api.createOrder({ items: [] }, "test-idempotency-key-0001");
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining("/orders"),
        expect.objectContaining({
          headers: {
            "Content-Type": "application/json",
            "Idempotency-Key": "test-idempotency-key-0001",
          },
        }),
      );
    });
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
