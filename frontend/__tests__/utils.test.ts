import { formatTimestamp, truncate, generateId } from "@/utils";

describe("utils", () => {
  test("truncate shortens long strings", () => {
    expect(truncate("hello world", 5)).toBe("hello...");
    expect(truncate("hi", 5)).toBe("hi");
  });

  test("generateId returns unique strings", () => {
    const a = generateId();
    const b = generateId();
    expect(a).not.toBe(b);
  });

  test("formatTimestamp returns a time string", () => {
    const result = formatTimestamp(Date.now());
    expect(result).toMatch(/\d{1,2}:\d{2}/);
  });
});
