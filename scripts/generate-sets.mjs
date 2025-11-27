// scripts/generate-sets.mjs
import { promises as fs } from "fs";
import path from "path";

const IMAGES_DIR = "images";
const OUTPUT_FILE = path.join(IMAGES_DIR, "sets.json");

// Allowed extensions
const exts = [".jpg", ".jpeg", ".png"];

function isImageFile(file) {
  const lower = file.toLowerCase();
  return exts.some(ext => lower.endsWith(ext));
}

async function main() {
  const files = await fs.readdir(IMAGES_DIR);

  // Keep only image files with _before / _after in the name
  const imageFiles = files.filter(isImageFile);

  const map = new Map(); // key: XXX -> { before, after }

  for (const file of imageFiles) {
    const lower = file.toLowerCase();
    const matchBefore = lower.match(/^(.*)_before\.(jpe?g|png)$/i);
    const matchAfter  = lower.match(/^(.*)_after\.(jpe?g|png)$/i);

    if (matchBefore) {
      const key = matchBefore[1]; // the XXX part
      const entry = map.get(key) || {};
      entry.before = path.join(IMAGES_DIR, file);
      map.set(key, entry);
    } else if (matchAfter) {
      const key = matchAfter[1];
      const entry = map.get(key) || {};
      entry.after = path.join(IMAGES_DIR, file);
      map.set(key, entry);
    }
  }

  // Build final array: only pairs that have both before + after
  const sets = Array.from(map.entries())
    .filter(([, v]) => v.before && v.after)
    .map(([key, v]) => ({
      key,
      before: v.before,
      after: v.after,
    }))
    .sort((a, b) => a.key.localeCompare(b.key));

  await fs.writeFile(OUTPUT_FILE, JSON.stringify(sets, null, 2) + "\n");
  console.log(`Wrote ${sets.length} image sets to ${OUTPUT_FILE}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
