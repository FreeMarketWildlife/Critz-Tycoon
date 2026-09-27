import { safeGridPosition } from "./world.js";

export const GRID_VERSION = 1;

// Schema/save keys stay v1. Old coordinates already represent map-tile units,
// so changing the visual tile size does not multiply player coordinates.
// The caller must preserve raw pre-migration bytes before saving this result.
// This pure conversion never reads or writes storage and never alters money,
// inventory, story flags, tank data, posts or other nonposition progress.
export function migrateGridState(state) {
  if (!state || typeof state !== "object" || !state.player)
    throw new TypeError("A validated game state is required for grid migration.");
  if (state.gridVersion !== undefined && state.gridVersion !== GRID_VERSION)
    throw new RangeError(`Unsupported grid version: ${state.gridVersion}`);
  const migrated = structuredClone(state);
  const position = safeGridPosition(migrated.scene, migrated.player.x, migrated.player.y, migrated);
  migrated.player = { ...migrated.player, ...position };
  migrated.gridVersion = GRID_VERSION;
  return migrated;
}
